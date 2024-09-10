import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    with open("radar.html", "r") as htm:
        app.indexhtml = htm.read()
    with open("control.html", "r") as htm:
        app.controlhtml = htm.read()
    with open("radar.svg", "r") as svg:
        app.radarsvg = svg.read()
    app.radar = {
        "size":
            {
                "x": 1000,
                "y": 1000
            },
        "targets": [
            # {
            #     "id": 0,
            #     "position": {
            #         "x": 0,
            #         "y": 0
            #     },
            #     "size": 5
            # }
        ]
    }


@app.get("/")
async def root():
    return HTMLResponse(content=app.indexhtml, status_code=200)


@app.get("/control")
async def control():
    return HTMLResponse(content=app.controlhtml, status_code=200)


@app.get("/radar.svg")
async def radarsvg():
    return HTMLResponse(content=app.radarsvg, status_code=200)


@app.get("/info")
async def info():
    return app.radar


@app.get("/add_target")
async def add_target(pos_x: int = 0, pos_y: int = 0, size: int = 5):
    id = 0

    if len(app.radar["targets"]) > 0:
        id = app.radar["targets"][-1]["id"] + 1

    app.radar["targets"].append(
        {
            "id": id,
            "position": {
                "x": pos_x,
                "y": pos_y
            },
            "size": size
        }
    )
    return "ok"


@app.get("/remove_target")
async def root(id: int):
    for i in range(len(app.radar["targets"])):
        if app.radar["targets"][i]["id"] == id:
            app.radar["targets"].pop(i)
            return "removed"

    return "not found"


if __name__ == "__main__":
    uvicorn.run("radar:app", port=9812, log_level="info")
