from datetime import date, datetime, timedelta
import json
import uuid
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, UploadFile, File, status
import os
from models.usuario_model import Usuario
from repositories.usuario_temp_repo import UsuarioTempRepo
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha
from util.cadastro import *
from util.cookies import *
from util.mensagens import adicionar_mensagem_erro
from util.templates import obter_jinja_templates
from util.validators import *

router = APIRouter()

templates = obter_jinja_templates("templates")

def verificar_login(request: Request):
    if not request.cookies.get(NOME_COOKIE_AUTH):
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Usuário não está logado",
            headers={"Location": "/"},
        )

# @router.get("/")
# async def get_root(request: Request):
#     usuario = request.state.usuario if hasattr(request.state, "usuario") else None
#     
#     if not usuario or not usuario.email:
#         return templates.TemplateResponse("pages/entrar.html", {"request": request})
#     if usuario.perfil == 1:
#         return RedirectResponse("/aluno", status_code=status.HTTP_303_SEE_OTHER)
#     if usuario.perfil == 2:
#         return RedirectResponse("/professor", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    request.session.clear()
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

    token = criar_token(usuario.id, usuario.nome, usuario.nome_perfil, usuario.email)

    if request.cookies.get(NOME_COOKIE_EMAIL_TEMP):
        response.delete_cookie(NOME_COOKIE_EMAIL_TEMP)

    request.session['usuario_autenticado'] = {
        "id": usuario.id,
        "nome": usuario.nome,
        "nome_perfil": usuario.nome_perfil,
    }

    response = RedirectResponse(f"/usuario/feed", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=1800,
        httponly=True,
        samesite="lax",
    )
    return response



@router.get("/cadastro", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    dados_usuario = request.session.get('usuario', '')
    return templates.TemplateResponse("main/pages/cadastre_se.html", {"request": request, 
        "dados_usuario": dados_usuario})

@router.post("/cadastrar")
async def post_cadastrar_paciente(request: Request):
    dados = dict(await request.form())
    senha = dados.pop("senha", None)
    conf_senha = dados.pop("conf_senha", None)
    usuario =  Usuario(**dados)
    request.session['usuario'] = {
        "nome": usuario.nome,
        "email": usuario.email,
        "nome_perfil": usuario.nome_perfil
    }
    response = RedirectResponse(f"/cadastro", status_code=status.HTTP_303_SEE_OTHER)
    if not is_email(dados["email"]):
        adicionar_mensagem_erro(response, "Esse não é um email valido. Confira-o")
        return response
    if not UsuarioRepo.is_email_unique(dados["email"]):
        adicionar_mensagem_erro(response, "Outra conta está usando o mesmo email.")
        return response
    if not is_matching_fields(senha, conf_senha):
        adicionar_mensagem_erro(response, "As senhas não coincidem.")
        return response
    if not is_password(senha):
        adicionar_mensagem_erro(response, "As senhas devem ter no mínimo 6 caracteres, letras maiúsculas e minúsculas, números e caracteres especiais."),
        return response
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
    senha_hash = obter_hash_senha(senha)
    usuario.senha = senha_hash
    UsuarioTempRepo.inserir_dados(usuario)
    response = RedirectResponse("/adicionar_nascimento", status_code=status.HTTP_303_SEE_OTHER)
    return response

@router.get("/adicionar_nascimento", response_class=HTMLResponse)
async def get_criar_conta(request: Request):
    return templates.TemplateResponse("main/pages/adicionar_nascimento.html", {"request": request})

@router.post("/salvar_nascimento")
async def post_cadastrar_aniversario(request: Request):

    dados = dict(await request.form())
    
    try:
        dia = int(dados["dia"])
        mes = int(dados["mes"])
        ano = int(dados["ano"])

        data_aniversario = datetime(ano, mes, dia)
        data_hoje = datetime.today()
        data_minima = data_hoje.replace(year=data_hoje.year - 13)
        if not is_date_less_than(data_aniversario, data_minima):
            response = RedirectResponse(f"/adicionar_nascimento", status_code=status.HTTP_303_SEE_OTHER)  
            adicionar_mensagem_erro(response, "A idade mínima para se cadastrar é de 13 anos"),
            return response
        usuario = request.session.get('usuario', '')
        email = usuario['email']
        usuario = UsuarioTempRepo.obter_dados(email)
        usuario.data_nascimento = data_aniversario
        UsuarioRepo.inserir(usuario)
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    
    except (ValueError, KeyError):
        response = RedirectResponse(f"/adicionar_nascimento", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Data de nascimento inválida. Verifique os campos.")
        return response
    
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from starlette import status

app = FastAPI()

@router.get("/escolher_categoria_perfil", response_class=HTMLResponse)
async def get_criar_conta(request: Request):
    return templates.TemplateResponse("main/pages/escolher_categoria_perfil.html", {"request": request})

@app.post("/salvar_perfil")
async def escolher_perfil(request: Request, perfil: int = Form(...)):
    try:
        usuario = request.session.get('usuario', '')
        email = usuario.get('email')
        
        if not email:
            return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
        
        UsuarioRepo.inserir_categoria_perfil(email, perfil)
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        response = RedirectResponse("/escolher_categoria_perfil", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Erro ao selecionar perfil. Tente novamente.")
        return response

@router.get("/adicionar_registro_profissional", response_class=HTMLResponse)
async def get_criar_conta(request: Request):
    return templates.TemplateResponse("main/pages/adicionar_registro_profissional.html", {"request": request})

@router.post("/cadastrar_profissional")
async def post_cadastrar_profissional(
    nome: str = Form(...),
    data_nascimento: date = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...),
    registro_profissional: UploadFile = File(...)
):
    if senha != confsenha:
        return RedirectResponse("/cadastro_profissional", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(
        nome=nome, 
        data_nascimento=data_nascimento, 
        email=email, 
        cpf=cpf, 
        telefone=telefone, 
        senha=senha_hash, 
        perfil=1,
        registro_profissional=True
    )
    UsuarioRepo.inserir(usuario)
    usuario_id = UsuarioRepo.obter_id_por_email(email)
    if usuario_id is None:
        return RedirectResponse("/cadastro_profissional", status_code=status.HTTP_303_SEE_OTHER)
    nome_arquivo = f"{usuario_id}_rp.pdf" 
    file_location = os.path.join("static/documentos", nome_arquivo)
    with open(file_location, "wb") as file:
        file.write(await registro_profissional.read())
    return RedirectResponse("/conta_criada", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/cadastrar_paciente")
async def post_cadastrar_paciente(request: Request):
    dados = dict(await request.form())
    erros = {}
    #atualizações do maroquio
    if is_matching_fields(dados["senha"], "senha", "Senha", dados["confirmacao_senha"], "Confirmação de Senha", erros):
        dados.pop("confirmacao_senha")
    is_person_fullname(dados["nome"], "nome", "Nome", erros)
    is_size_between(dados["nome"], "nome", "Nome", erros)
    data_minima = datetime.now() - timedelta(days=365 *130)
    data_maxima = datetime.now() + timedelta(days=365 *18)
    is_date_between(dados["data_nascimento"], "data_nascimento", "Data de Nascimento", data_minima, data_maxima, erros)
    is_email(dados["email"], "email", "E-mail", erros)
    is_size_between(dados["telefone"], "telefone", "Telefone", erros)
    is_password(dados["senha"], "senha", "Senha", erros)

    if erros:
        response = templates.TemplatesResponse("pages/cadastrar_paciente.html", {"request": request, "dados": dados, "erros": erros},)
        adicionar_mensagem_erro(response, "Há erros no formulário. Corrija-os e tente novamente")
        return response
    senha_hash = obter_hash_senha(dados["senha"])
    dados["senha"] = senha_hash
    usuario = Usuario(**dados)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/conta_criada", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_profissional", response_class=HTMLResponse)
async def get_cadastro_profissional(request: Request):
    return templates.TemplateResponse("main/pages/cadastro_profissional.html", {"request": request})

@router.get("/cadastro_paciente", response_class=HTMLResponse)
async def get_cadastro_paciente(request: Request):
    return templates.TemplateResponse("main/pages/cadastro_paciente.html", {"request": request})

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

