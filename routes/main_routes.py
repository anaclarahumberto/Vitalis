from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, UploadFile, File, status
import os
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha
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
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

@router.get("/login", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("main/pages/conecte_se.html", {"request": request})

@router.post("/login")
async def post_login(request: Request):
    dados = dict(await request.form())
    usuario = UsuarioRepo.checar_credenciais(dados["email"], dados["senha"])
    if usuario is None:
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Seus dados estão incorretos. Confira-os")
        return response
    token = criar_token(usuario.id, usuario.nome, usuario.nome_perfil, usuario.email, usuario.perfil)
    # nome_perfil = None
    # match (usuario[2]):
    #     case 1: nome_perfil = "profissional"
    #     case 2: nome_perfil = "paciente"
    #     case _: nome_perfil = ""
    response = RedirectResponse(f"/usuario/feed", status_code=status.HTTP_303_SEE_OTHER)    
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=3600*24*365*10,
        httponly=True,
        samesite="lax"
    )
    return response

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

#validação

@router.get("/criar_conta", response_class=HTMLResponse)
async def get_criar_conta(request: Request):
    return templates.TemplateResponse("main/pages/criar_conta.html", {"request": request})

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

