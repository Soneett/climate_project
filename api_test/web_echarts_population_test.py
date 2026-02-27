from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright


def fetch_population_pyramid(api_url: str, region_id: int, year: int | None) -> dict:
    params = {"region_id": region_id}
    if year is not None:
        params["year"] = year
    response = requests.get(f"{api_url.rstrip('/')}/analytics/population_pyramid", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def build_option(payload: dict) -> dict:
    points = payload.get("points", [])
    categories = [p["age_code"] for p in points]
    male = [-float(p["male"]) for p in points]
    female = [float(p["female"]) for p in points]
    year = payload.get("year")

    return {
        "title": {"text": f"Половозрастная структура: {payload.get('region_name')} ({year})", "left": "center"},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": """function (params) {
                return params.map(p => `${p.seriesName}: ${Math.abs(p.value)}`).join('<br/>');
            }""",
        },
        "legend": {"data": ["Мужчины", "Женщины"], "top": 35},
        "grid": {"left": "5%", "right": "5%", "top": 80, "bottom": 30, "containLabel": True},
        "xAxis": {
            "type": "value",
            "axisLabel": {"formatter": "{value}"},
        },
        "yAxis": {
            "type": "category",
            "data": categories,
        },
        "series": [
            {"name": "Мужчины", "type": "bar", "stack": "Total", "data": male, "itemStyle": {"color": "#5B8DEF"}},
            {"name": "Женщины", "type": "bar", "stack": "Total", "data": female, "itemStyle": {"color": "#F472B6"}},
        ],
    }


def render_and_capture(option: dict, output_all: Path, output_filtered: Path):
    html = """
    <html><head><meta charset='utf-8' /><script src='https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js'></script></head>
    <body><div id='chart' style='width: 1280px; height: 720px;'></div>
    <script>
      const option = __OPTION__;
      if (option.tooltip && typeof option.tooltip.formatter === 'string' && option.tooltip.formatter.startsWith('function')) {
        option.tooltip.formatter = eval('(' + option.tooltip.formatter + ')');
      }
      const chart = echarts.init(document.getElementById('chart'));
      chart.setOption(option);
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

        page.evaluate("window.chart.dispatchAction({type:'legendUnSelect', name:'Женщины'})")
        page.wait_for_timeout(700)
        page.screenshot(path=str(output_filtered), full_page=True)
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Проверка отрисовки population_age_sex в браузере (ECharts)")
    parser.add_argument("--api-url", default="http://127.0.0.1:8081")
    parser.add_argument("--region-id", type=int, required=True)
    parser.add_argument("--year", type=int, default=None)
    parser.add_argument("--output-all", default="api_test/artifacts/population_echarts_all.png")
    parser.add_argument("--output-filtered", default="api_test/artifacts/population_echarts_filtered.png")
    args = parser.parse_args()

    payload = fetch_population_pyramid(args.api_url, args.region_id, args.year)
    if not payload.get("points"):
        raise ValueError("Пустые данные population_pyramid.")

    option = build_option(payload)
    output_all = Path(args.output_all)
    output_filtered = Path(args.output_filtered)
    output_all.parent.mkdir(parents=True, exist_ok=True)

    render_and_capture(option, output_all, output_filtered)
    print(f"Saved: {output_all}")
    print(f"Saved: {output_filtered}")


if __name__ == "__main__":
    main()
