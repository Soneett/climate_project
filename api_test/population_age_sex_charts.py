from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import requests


def fetch_population_pyramid(api_url: str, region_id: int, year: int | None) -> dict:
    params = {"region_id": region_id}
    if year is not None:
        params["year"] = year

    response = requests.get(f"{api_url.rstrip('/')}/analytics/population_pyramid", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def build_chart(payload: dict, output_path: Path):
    points = payload.get("points", [])
    if not points:
        raise ValueError("API вернул пустой набор данных по population_age_sex.")

    ages = [p["age_code"] for p in points]
    males = [-float(p["male"]) for p in points]
    females = [float(p["female"]) for p in points]

    fig, ax = plt.subplots(figsize=(12, 10))
    y = range(len(ages))

    ax.barh(y, males, color="#4A90E2", label="Мужчины")
    ax.barh(y, females, color="#E26A8D", label="Женщины")

    ax.set_yticks(list(y))
    ax.set_yticklabels(ages)
    ax.set_xlabel("Численность")
    ax.set_ylabel("Возраст")
    ax.set_title(f"Половозрастная структура: {payload['region_name']} ({payload['year']})")
    ax.legend()
    ax.axvline(0, color="black", linewidth=0.8)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Проверка данных population_age_sex через API")
    parser.add_argument("--api-url", default="http://127.0.0.1:8081", help="Базовый URL backend API")
    parser.add_argument("--region-id", type=int, required=True, help="ID региона")
    parser.add_argument("--year", type=int, default=None, help="Год")
    parser.add_argument("--output", default="api_test/artifacts/population_pyramid.png", help="Путь к PNG")

    args = parser.parse_args()

    payload = fetch_population_pyramid(args.api_url, args.region_id, args.year)
    build_chart(payload, Path(args.output))
    print(f"Chart saved to: {args.output}")


if __name__ == "__main__":
    main()
