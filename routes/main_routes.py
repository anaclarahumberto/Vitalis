from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})


@router.get("/notificacoes", response_class=HTMLResponse)
async def get_notificacoes(request: Request):
    return templates.TemplateResponse("pages/notificacoes.html", {"request": request}) 

@router.get("/configuracoes", response_class=HTMLResponse)
async def get_configuracoes(request: Request):
    return templates.TemplateResponse("pages/configuracoes.html", {"request": request}) 

@router.get("/configuracoes/tempogasto", response_class=HTMLResponse)
async def get_tempogasto(request: Request):
    return templates.TemplateResponse("pages/tempogasto.html", {"request": request}) 

@router.get("/configuracoes/arquivados", response_class=HTMLResponse)
async def get_arquivados(request: Request):
    return templates.TemplateResponse("pages/arquivados.html", {"request": request}) 

@router.get("/perfil", response_class=HTMLResponse)
async def get_perfil(request: Request):
    return templates.TemplateResponse("pages/perfil.html", {"request": request}) 