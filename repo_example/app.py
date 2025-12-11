from fastapi import FastAPI
from routers import orbits_router

app = FastAPI(title="Orbit Catalog Backend Service")


@app.get("/", response_model=str)
async def read_root():
    return "Orbit Catalog Backend Service"


app.include_router(orbits_router)


if __name__ == "__main__":  # для отладки
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
