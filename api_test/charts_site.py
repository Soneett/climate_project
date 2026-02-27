from __future__ import annotations

import argparse
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


def create_app(site_dir: Path) -> FastAPI:
    app = FastAPI(title="API Test Charts Site")

    @app.get("/")
    async def root() -> RedirectResponse:
        return RedirectResponse(url="/site/index.html")

    app.mount("/site", StaticFiles(directory=site_dir), name="site")
    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Локальный сайт с интерактивными графиками из backend API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()

    site_dir = Path(__file__).parent / "site"
    app = create_app(site_dir)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
