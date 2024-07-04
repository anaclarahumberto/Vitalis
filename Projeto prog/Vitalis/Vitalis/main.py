from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from ler_html import ler_html

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

@app.get("/")
def get_root(request: Request):
    view_model = {
        "request": request
    }
    return templates.TemplateResponse("index.html", view_model)

@app.get("/notificacao")
def get_notificacao(request: Request):
    view_model = {"request": request}
    return templates.TemplateResponse("notificacao.html", view_model) 

@app.get("/configuracao")
def get_configuracao(request: Request):
    view_model = {"request": request}
    return templates.TemplateResponse("configuracao.html", view_model) 

@app.get("/tempogasto")
def get_tempogasto(request: Request):
    view_model = {"request": request}
    return templates.TemplateResponse("tempogasto.html", view_model) 

@app.get("/arquivados")
def get_arquivados(request: Request):
    view_model = {"request": request}
    return templates.TemplateResponse("arquivados.html", view_model) 


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)