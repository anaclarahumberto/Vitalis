from datetime import date, datetime, timedelta
import json
import uuid
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, UploadFile, File, status
import os
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha
from util.cadastro import *
from util.cookies import *
from util.mensagens import adicionar_mensagem_erro
from util.templates import obter_jinja_templates
from util.validators import *

router = APIRouter()

templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

@router.get("/login", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    email_temp = request.cookies.get('email_temp', '')
    return templates.TemplateResponse("main/pages/conecte_se.html", {"request": request, "email_temp": email_temp})

from datetime import timedelta

from datetime import datetime, timedelta, timezone

@router.post("/login")
async def post_login(request: Request, response: Response): 
    dados = dict(await request.form())
    
    usuario = UsuarioRepo.checar_credenciais(dados["email"], dados["senha"])
    
    if usuario is None:
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_cookie(response, NOME_COOKIE_EMAIL_TEMP, dados["email"], 180)
        adicionar_mensagem_erro(response, "Seus dados estão incorretos. Confira-os")
        return response

    token = criar_token(usuario.id, usuario.nome, usuario.nome_perfil, usuario.email, usuario.foto_perfil, usuario.tipo_perfil)

    if request.cookies.get(NOME_COOKIE_EMAIL_TEMP):
        response.delete_cookie(NOME_COOKIE_EMAIL_TEMP)

    response = RedirectResponse(f"/usuario/feed", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=1800,
        httponly=True,
        samesite="lax",
    )
    return response

@router.get("/criar_conta", response_class=HTMLResponse)
async def get_criar_conta(request: Request):
    return templates.TemplateResponse("main/pages/criar_conta.html", {"request": request})

@router.post("/escolher_perfil")
async def escolher_perfil(request: Request, tipo_perfil: int = Form(...)):
    return templates.TemplateResponse("main/pages/cadastre_se.html", {"request": request, "tipo_perfil": tipo_perfil})

@router.get("/cadastro", response_class=HTMLResponse)
async def get_criar_conta(request: Request, tipo_perfil: int = None):
    return templates.TemplateResponse("main/pages/cadastre_se.html", {"request": request, "tipo_perfil": tipo_perfil})

@router.post("/cadastrar")
async def post_cadastrar_paciente(request: Request, registro_profissional: UploadFile = File(None)):
    dados = dict(await request.form())
    data_nascimento = datetime.strptime(dados.get("data_nascimento"), "%d/%m/%Y").date()
    print(data_nascimento)
    dados["data_nascimento"] = data_nascimento
    response = RedirectResponse(f"/cadastro?tipo_perfil={dados['tipo_perfil']}", status_code=status.HTTP_303_SEE_OTHER)
    if not is_password(dados["senha"]):
        adicionar_mensagem_erro(response, "As senhas devem ter no mínimo 6 caracteres, letras maiúsculas e minúsculas, números e caracteres especiais."),
        return response
    if not is_matching_fields(dados["senha"], dados["conf_senha"]):
        adicionar_mensagem_erro(response, "As senhas não coincidem.")
        return response
    else : dados.pop("conf_senha")
    if not is_person_fullname(dados["nome"]):
        adicionar_mensagem_erro(response, "Os nomes devem conter um primeiro nome e um sobrenome."),
        return response
    if not is_only_letters_or_space(dados["nome"]):
        adicionar_mensagem_erro(response, "Os nomes devem conter apenas letras e espaços."),
        return response
    if not is_own_name(dados["nome"]):
        adicionar_mensagem_erro(response, "Esse não é um nome próprio valido. Confira-o."),
        return response
    if not is_user_name(dados["nome_perfil"]):
        adicionar_mensagem_erro(response, "Os nomes de usuário só podem usar letras, números, sublinhados e pontos."),
        return response
    if not UsuarioRepo.is_username_unique(dados["nome_perfil"]):
        adicionar_mensagem_erro(response, "Esse nome de usuário não está disponível. Tente outro nome..")
        return response
    if not is_email(dados["email"]):
        adicionar_mensagem_erro(response, "Esse não é um email valido. Confira-o")
        return response
    if not UsuarioRepo.is_email_unique(dados["email"]):
        adicionar_mensagem_erro(response, "Outra conta está usando o mesmo email.")
        return response
    data_minima = date.today() - timedelta(days=13*365)
    if not is_date_greater_than(dados["data_nascimento"], data_minima):
        adicionar_mensagem_erro(response, "Você deve ter mais de 13 anos para se cadastrar."),
        return response
    if not is_cpf(dados["cpf"]):
        adicionar_mensagem_erro(response, "Esse não é um cpf valido. Confira-o")
        return response
    if not UsuarioRepo.is_cpf_unique(dados["cpf"]):
        adicionar_mensagem_erro(response, "Outra conta está usando o mesmo cpf.")
        return response
    if not is_phone_number(dados["telefone"]):
        adicionar_mensagem_erro(response, "Esse não é um telefone valido. Confira-o")
        return response
    if not UsuarioRepo.is_phone_unique(dados["telefone"]):
        adicionar_mensagem_erro(response, "Outra conta está usando o mesmo telefone.")
        return response
    senha_hash = obter_hash_senha(dados["senha"])
    dados["senha"] = senha_hash
    usuario = Usuario(**dados)
    if(usuario.tipo_perfil == 2): usuario.registro_profissional = True
    else: usuario.registro_profissional = False
    UsuarioRepo.inserir(usuario)
    if registro_profissional:
        nome_arquivo = f"{usuario.nome}_rp.pdf" 
        file_location = os.path.join("static/documentos", nome_arquivo)
        with open(file_location, "wb") as file:
            file.write(await registro_profissional.read())
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    return response

@router.get("/esqueci_a_senha", response_class=HTMLResponse)
async def get_esqueci_a_senha(request: Request):
    return templates.TemplateResponse("main/pages/esqueci_a_senha.html", {"request": request})

@router.post("/senha_redefinada", response_class=HTMLResponse)
async def post_senha_redefinida(request: Request):
    return templates.TemplateResponse("main/pages/senha_redefinida.html", {"request": request})

# @router.post("/entrar", response_class=HTMLResponse)
# async def post_entrar(request: Request, usuario: str = Depends(verificar_login)):
#     return templates.TemplateResponse("main/pages/index.html", {"request": request})

@router.get("/conta_criada", response_class=HTMLResponse)
async def get_conta_criada(request: Request):
    return templates.TemplateResponse("main/pages/conta_criada.html", {"request": request})

@router.get("/sair")
async def get_sair(request: Request):
    request.state.usuario = None
    response = RedirectResponse("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value="",
        max_age=1,
        httponly=True,
        samesite="lax"
    )
    return response

