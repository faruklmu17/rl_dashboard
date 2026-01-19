import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
METRICS_FILE = Path("metrics.json")
INDEX_FILE = Path("index.html")

@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_FILE.read_text()

@app.get("/details")
def details():
    html_file = Path(__file__).parent / "rl_cartpole_details.html"
    return HTMLResponse(content=html_file.read_text())

@app.get("/metrics")
def metrics():
    if not METRICS_FILE.exists():
        return JSONResponse({"status": "waiting"})
    return JSONResponse(json.loads(METRICS_FILE.read_text()))

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="."), name="static")
