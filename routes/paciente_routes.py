from datetime import date
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, UploadFile, File, status
import os
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/paciente")

templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("main/pages/login.html", {"request": request})