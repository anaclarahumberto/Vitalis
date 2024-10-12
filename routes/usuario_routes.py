import base64
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Form
import os

import jwt
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from routes.main_routes import verificar_login
from util.templates import obter_jinja_templates

router = APIRouter()

templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("main/pages/login.html", {"request": request})

@router.get("/feed", response_class=HTMLResponse)
async def get_root(request: Request, usuario: str = Depends(verificar_login)):
    print(request.state.usuario)
    dados_perfil = UsuarioRepo.obter_dados_perfil("camila01@gmail.com")
    
    if dados_perfil is None:
        return RedirectResponse("/erro", status_code=303)

    if dados_perfil is None:
        return RedirectResponse("/erro", status_code=303)
    return templates.TemplateResponse("main/pages/index.html", {"request": request, "dados_perfil": dados_perfil})

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
    request.state.usuario = UsuarioRepo.obter_dados_perfil(request.state.usuario.email)
    return templates.TemplateResponse("main/pages/editar_perfil.html", {"request": request}) 

@router.post("/atualizar_perfil")
async def editar_perfil(
    request: Request,
    nome: str = Form(...),
    nome_perfil: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    bio_perfil: str = Form(...),
    categoria: str = Form(None),
    genero: str = Form(...),
    foto_perfil_blob: str = Form(...),
    email_atual: str = Form(None),
):

    # Atualiza os dados do usuário
    atualizacao_sucesso = UsuarioRepo.atualizar_dados_perfil(
        nome=nome,
        nome_perfil=nome_perfil,
        email=email,
        telefone=telefone,
        bio_perfil=bio_perfil,
        categoria=categoria,
        genero=genero,
        email_atual=email_atual,
    )
    
    if not atualizacao_sucesso:
        return RedirectResponse("/erro", status_code=303)
    
    if foto_perfil_blob:
        header, base64_data = foto_perfil_blob.split(",", 1)
        usuario_id = UsuarioRepo.obter_id_por_email(email_atual)
        nome_arquivo = f"{usuario_id}.jpeg"  # Nome do arquivo
        caminho_arquivo = os.path.join("static/img", nome_arquivo)
        with open(caminho_arquivo, "wb") as file:
            file.write(base64.b64decode(base64_data))
    
    return RedirectResponse("/perfil", status_code=303)



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
    request.state.usuario = UsuarioRepo.obter_dados_perfil(request.state.usuario.email)
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



