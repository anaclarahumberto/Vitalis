from datetime import date
from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form, UploadFile, File, status
import os
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, criar_token, obter_hash_senha
from util.templates import obter_jinja_templates

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
    return templates.TemplateResponse("main/pages/login.html", {"request": request})

@router.post("/login")
async def post_login(
    email: str = Form(...), 
    senha: str = Form(...)):
    UsuarioRepo.criar_tabela()
    usuario = UsuarioRepo.checar_credenciais(email, senha)
    if usuario is None:
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="mensagem_erro", value="Email ou senha incorretos", max_age=5)
        return response
    token = criar_token(usuario.nome, usuario.email, usuario.perfil)
    # nome_perfil = None
    # match (usuario[2]):
    #     case 1: nome_perfil = "profissional"
    #     case 2: nome_perfil = "paciente"
    #     case _: nome_perfil = ""
    response = RedirectResponse(f"/feed", status_code=status.HTTP_303_SEE_OTHER)    
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
async def post_cadastrar_paciente(
    nome: str = Form(...),
    data_nascimento: date = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...)):
    if senha != confsenha:
        return RedirectResponse("/cadastro_paciente", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(
        nome=nome, 
        data_nascimento=data_nascimento, 
        email=email, 
        cpf=cpf, 
        telefone=telefone, 
        senha=senha_hash, 
        perfil=2)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/conta_criada", status_code=status.HTTP_303_SEE_OTHER)

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
async def get_conta_criada(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/conta_criada.html", {"request": request})

@router.get("/sair")
async def get_sair():
    response = RedirectResponse("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value="",
        max_age=1,
        httponly=True,
        samesite="lax"
    )
    return response

@router.get("/feed", response_class=HTMLResponse)
async def get_root(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/index.html", {"request": request})

@router.get("/mensagens_principal", response_class=HTMLResponse)
async def get_mensagens(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/mensagens_principal.html", {"request": request})

@router.get("/notificacoes", response_class=HTMLResponse)
async def get_notificacoes(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/notificacoes.html", {"request": request}) 

@router.get("/configuracoes", response_class=HTMLResponse)
async def get_configuracoes(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/configuracoes.html", {"request": request}) 

@router.get("/tempogasto", response_class=HTMLResponse)
async def get_tempogasto(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/tempogasto.html", {"request": request}) 

@router.get("/arquivados", response_class=HTMLResponse)
async def get_arquivados(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/arquivados.html", {"request": request})

@router.get("/anuncios", response_class=HTMLResponse)
async def get_anuncios(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/anuncio.html", {"request": request})

@router.get("/anunciante", response_class=HTMLResponse)
async def get_anunciante(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/anunciante.html", {"request": request})

@router.get("/editar_perfil", response_class=HTMLResponse)
async def get_editar(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/editar_perfil.html", {"request": request}) 

@router.get("/cupons_ativos", response_class=HTMLResponse)
async def get_cuponsativos(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/cupons_ativos.html", {"request": request}) 

@router.get("/cupons_indisponiveis", response_class=HTMLResponse)
async def get_cuponsindisponiveis(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/cupons_indisponiveis.html", {"request": request}) 

@router.get("/feedback", response_class=HTMLResponse)
async def get_feedback(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/feedback.html", {"request": request})

@router.get("/perfil", response_class=HTMLResponse)
async def get_perfil(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/perfil.html", {"request": request})

@router.get("/entrarMaroquio", response_class=HTMLResponse)
async def get_perfil(request: Request):
    return templates.TemplateResponse("main/pages/entrar.html", {"request": request})

@router.get("/plano", response_class=HTMLResponse)
async def get_root(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/plano.html", {"request": request})

@router.get("/daily1", response_class=HTMLResponse)
async def get_daily(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/daily1.html", {"request": request})

@router.get("/daily2", response_class=HTMLResponse)
async def get_daily(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/daily2.html", {"request": request})

@router.get("/daily3", response_class=HTMLResponse)
async def get_daily(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/daily3.html", {"request": request})

@router.get("/daily4", response_class=HTMLResponse)
async def get_daily(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/daily4.html", {"request": request})

@router.get("/daily5", response_class=HTMLResponse)
async def get_daily(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/daily5.html", {"request": request})

@router.get("/anunciante_escolha", response_class=HTMLResponse)
async def get_escolha(request: Request, usuario: str = Depends(verificar_login)):
    return templates.TemplateResponse("main/pages/anunciante_escolha.html", {"request": request})

