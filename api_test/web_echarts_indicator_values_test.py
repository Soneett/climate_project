from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright


def fetch_chart_data(api_url: str, region_id: int, indicator_ids: list[int]) -> dict:
    query = [("region_id", str(region_id))] + [("indicator_ids", str(i)) for i in indicator_ids]
    response = requests.get(f"{api_url.rstrip('/')}/analytics/chart_data", params=query, timeout=30)
    response.raise_for_status()
    return response.json()


def build_line_option(payload: dict) -> dict:
    years = sorted({point["year"] for series in payload.get("series", []) for point in series.get("points", [])})

    by_year = {}
    for y in years:
        by_year[y] = {}

    legend = []
    series_out = []
    for series in payload.get("series", []):
        name = series["indicator_name"]
        legend.append(name)
        points_map = {p["year"]: p["value"] for p in series.get("points", [])}
        data = [points_map.get(y) for y in years]
        series_out.append({"name": name, "type": "line", "smooth": True, "data": data})

    return {
        "title": {"text": f"Индикаторы региона: {payload.get('region_name')}", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": legend, "top": 35},
        "xAxis": {"type": "category", "data": [str(y) for y in years]},
        "yAxis": {"type": "value"},
        "series": series_out,
    }


def render_and_capture(option: dict, output_all: Path, output_filtered: Path):
    html = """
    <html><head><meta charset='utf-8' /><script src='https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js'></script></head>
    <body><div id='chart' style='width: 1280px; height: 720px;'></div>
    <script>
      const chart = echarts.init(document.getElementById('chart'));
      chart.setOption(__OPTION__);
      window.chart = chart;
    </script>
    </body></html>
    """.replace("__OPTION__", json.dumps(option, ensure_ascii=False))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1320, "height": 780})
        page.set_content(html, wait_until="networkidle")
        page.wait_for_timeout(1200)
        page.screenshot(path=str(output_all), full_page=True)

        if option.get("legend", {}).get("data"):
            first = option["legend"]["data"][0]
            page.evaluate("(name) => window.chart.dispatchAction({type:'legendUnSelect', name})", first)
            page.wait_for_timeout(700)
        page.screenshot(path=str(output_filtered), full_page=True)
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Проверка отрисовки chart_data (indicator_values) в браузере (ECharts)")
    parser.add_argument("--api-url", default="http://127.0.0.1:8081")
    parser.add_argument("--region-id", type=int, required=True)
    parser.add_argument("--indicator-ids", type=int, nargs="+", required=True)
    parser.add_argument("--output-all", default="api_test/artifacts/indicator_values_line_all.png")
    parser.add_argument("--output-filtered", default="api_test/artifacts/indicator_values_line_filtered.png")
    args = parser.parse_args()

    payload = fetch_chart_data(args.api_url, args.region_id, args.indicator_ids)
    if not payload.get("series"):
        raise ValueError("Пустые данные chart_data.")

    option = build_line_option(payload)
    output_all = Path(args.output_all)
    output_filtered = Path(args.output_filtered)
    output_all.parent.mkdir(parents=True, exist_ok=True)

    render_and_capture(option, output_all, output_filtered)
    print(f"Saved: {output_all}")
    print(f"Saved: {output_filtered}")


if __name__ == "__main__":
    main()
