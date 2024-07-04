from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

@app.get("/")
def get_root(request: Request):
    view_model = {
        "request": request
    }
    return templates.TemplateResponse("index.html", view_model)

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)