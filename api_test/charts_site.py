from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Локальный сайт с интерактивными графиками из backend API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()

    site_root = Path(__file__).parent
    handler = partial(SimpleHTTPRequestHandler, directory=str(site_root))
    server = ThreadingHTTPServer((args.host, args.port), handler)

    print(f"Serving api_test at http://{args.host}:{args.port}/site/index.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
