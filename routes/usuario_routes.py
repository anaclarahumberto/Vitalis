import base64
from datetime import date, datetime, timedelta
import locale
import uuid
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import APIRouter, Form
import os

import jwt
from models.publicacao_model import Publicacao
from models.usuario_model import Usuario
from repositories.publicacao_repo import PublicacaoRepo
from repositories.usuario_repo import UsuarioRepo
from util.mensagens import adicionar_mensagem_erro
from util.templates import obter_jinja_templates
from util.validators import *

router = APIRouter(prefix="/usuario")

templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("main/pages/login.html", {"request": request})

@router.get("/definir_perfil", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("main/pages/definir_perfil.html", {"request": request})

@router.post("/finalizar_perfil")
async def finalizar_perfil(
    request: Request,
    nome_perfil: str = Form(...),
    foto_perfil_blob: str = Form(...),
):
    
    atualizacao_sucesso = UsuarioRepo.inserir_dados_perfil(
        nome_perfil=nome_perfil,
        foto_perfil=True,
        id=request.state.usuario.id,
    )
    
    if not atualizacao_sucesso:
        return RedirectResponse("/erro", status_code=303)
    
    if foto_perfil_blob:
        header, base64_data = foto_perfil_blob.split(",", 1)
        nome_arquivo = f"{request.state.usuario.id}.jpeg"  # Nome do arquivo
        caminho_arquivo = os.path.join("static/img", nome_arquivo)
        with open(caminho_arquivo, "wb") as file:
            file.write(base64.b64decode(base64_data))
    
    return RedirectResponse("/feed", status_code=303)

@router.get("/feed", response_class=HTMLResponse)
async def get_root(request: Request):
    request.state.usuario = UsuarioRepo.obter_dados_perfil(request.state.usuario.id)
    print(request.state.usuario)
    return templates.TemplateResponse("main/pages/index.html", {"request": request})

@router.post("/compartilhar_publicacao")
async def post_compartilhar_publicação(
    request: Request,
    texto_pub: str = Form(...),
    imagem: UploadFile = File(None)
):

    dados = {
        "texto_pub": texto_pub,
        "imagem": None  
    }

    if imagem:
        # Lê os dados da imagem
        imagem_data = await imagem.read()

        # Gera um nome de arquivo único
        nome_arquivo = f"{uuid.uuid4()}.jpeg"
        caminho_arquivo = os.path.join("static/img/publicacoes", nome_arquivo)

        try:
            # Salvar a imagem no servidor
            with open(caminho_arquivo, "wb") as file:
                file.write(imagem_data)
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
            return {"error": "Erro ao salvar a imagem."}
        
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        
        data_criacao = datetime.now()

        publicacao = Publicacao(
            descricao = texto_pub,
            imagem = nome_arquivo,
            id_usuario = request.state.usuario.id,
            data_criacao = f"{data_criacao.day} de {meses[data_criacao.month]} de {data_criacao.year}"
        )

        PublicacaoRepo.inserir(publicacao)

    return JSONResponse({"message": "Publicação compartilhada com sucesso!"}, status_code=200)


@router.get("/mensagens_principal", response_class=HTMLResponse)
async def get_mensagens(request: Request):
    return templates.TemplateResponse("main/pages/mensagens_principal.html", {"request": request})

@router.get("/notificacoes", response_class=HTMLResponse)
async def get_notificacoes(request: Request):
    return templates.TemplateResponse("main/pages/notificacoes.html", {"request": request}) 

@router.get("/configuracoes", response_class=HTMLResponse)
async def get_configuracoes(request: Request):
    return templates.TemplateResponse("main/pages/configuracoes.html", {"request": request}) 

@router.get("/tempogasto", response_class=HTMLResponse)
async def get_tempogasto(request: Request):
    return templates.TemplateResponse("main/pages/tempogasto.html", {"request": request}) 

@router.get("/arquivados", response_class=HTMLResponse)
async def get_arquivados(request: Request):
    return templates.TemplateResponse("main/pages/arquivados.html", {"request": request})

@router.get("/anuncios", response_class=HTMLResponse)
async def get_anuncios(request: Request):
    return templates.TemplateResponse("main/pages/anuncio.html", {"request": request})

@router.get("/anunciante", response_class=HTMLResponse)
async def get_anunciante(request: Request):
    return templates.TemplateResponse("main/pages/anunciante.html", {"request": request})

@router.get("/editar_perfil", response_class=HTMLResponse)
async def get_editar(request: Request):
    request.state.usuario = UsuarioRepo.obter_dados_perfil(request.state.usuario.id)
    return templates.TemplateResponse("main/pages/editar_perfil.html", {"request": request}) 

@router.post("/atualizar_perfil")
async def editar_perfil(request: Request):
    request.state.usuario = UsuarioRepo.obter_dados_perfil(request.state.usuario.id)
    dados = dict(await request.form())
    foto_perfil_blob = dados["foto_perfil_blob"]
    dados.pop("foto_perfil_blob")
    response = RedirectResponse(f"/usuario/editar_perfil", status_code=status.HTTP_303_SEE_OTHER)
    if not is_person_fullname(dados["nome"]):
        adicionar_mensagem_erro(response, "Os nomes devem conter um primeiro nome e um sobrenome."),
        return response
    if not is_only_letters_or_space(dados["nome"]):
        adicionar_mensagem_erro(response, "Os nomes devem conter apenas letras e espaços."),
        return response
    if not is_own_name(dados["nome"]):
        adicionar_mensagem_erro(response, "Esse não é um nome próprio valido. Confira-o."),
        return response
    if dados["nome_perfil"] != request.state.usuario.nome_perfil:
        if not is_user_name(dados["nome_perfil"]):
            adicionar_mensagem_erro(response, "Os nomes de usuário só podem usar letras, números, sublinhados e pontos."),
            return response
        if not UsuarioRepo.is_username_unique(dados["nome_perfil"]):
            adicionar_mensagem_erro(response, "Esse nome de usuário não está disponível. Tente outro nome..")
            return response
    if dados["telefone"] != request.state.usuario.telefone:
        if not is_phone_number(dados["telefone"]):
            adicionar_mensagem_erro(response, "Esse não é um telefone valido. Confira-o")
            return response
        if not UsuarioRepo.is_phone_unique(dados["telefone"]):
            adicionar_mensagem_erro(response, "Outra conta está usando o mesmo telefone.")
            return response

    # Atualiza os dados do usuário
    atualizacao_sucesso = UsuarioRepo.atualizar_dados_perfil(
        foto_perfil = True,
        nome=dados["nome"],
        nome_perfil=dados["nome_perfil"],
        telefone=dados["telefone"],
        bio_perfil=dados["bio_perfil"],
        categoria= None,
        genero=dados["genero"],
        id=request.state.usuario.id,
    )
    
    if not atualizacao_sucesso:
        return RedirectResponse("/erro", status_code=303)
    
    if foto_perfil_blob:
        header, base64_data = foto_perfil_blob.split(",", 1)
        nome_arquivo = f"{request.state.usuario.id}.jpeg"  # Nome do arquivo
        caminho_arquivo = os.path.join("static/img", nome_arquivo)
        with open(caminho_arquivo, "wb") as file:
            file.write(base64.b64decode(base64_data))
    
    return RedirectResponse("/usuario/perfil", status_code=303)



@router.get("/cupons_ativos", response_class=HTMLResponse)
async def get_cuponsativos(request: Request):
    return templates.TemplateResponse("main/pages/cupons_ativos.html", {"request": request}) 

@router.get("/cupons_indisponiveis", response_class=HTMLResponse)
async def get_cuponsindisponiveis(request: Request):
    return templates.TemplateResponse("main/pages/cupons_indisponiveis.html", {"request": request}) 

@router.get("/feedback", response_class=HTMLResponse)
async def get_feedback(request: Request):
    return templates.TemplateResponse("main/pages/feedback.html", {"request": request})

@router.get("/perfil", response_class=HTMLResponse)
async def get_perfil(request: Request):
    usuario = UsuarioRepo.obter_dados_perfil(request.state.usuario.id)
    
    publicacoes = PublicacaoRepo.obter_publicacoes_por_usuario(request.state.usuario.id)

    return templates.TemplateResponse("main/pages/perfil.html", {
        "request": request,
        "usuario": usuario,
        "publicacoes": publicacoes
    })


@router.get("/entrarMaroquio", response_class=HTMLResponse)
async def get_perfil(request: Request):
    return templates.TemplateResponse("main/pages/entrar.html", {"request": request})

@router.get("/plano", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/plano.html", {"request": request})

@router.get("/daily1", response_class=HTMLResponse)
async def get_daily(request: Request):
    return templates.TemplateResponse("main/pages/daily1.html", {"request": request})

@router.get("/daily2", response_class=HTMLResponse)
async def get_daily(request: Request):
    return templates.TemplateResponse("main/pages/daily2.html", {"request": request})

@router.get("/daily3", response_class=HTMLResponse)
async def get_daily(request: Request):
    return templates.TemplateResponse("main/pages/daily3.html", {"request": request})

@router.get("/daily4", response_class=HTMLResponse)
async def get_daily(request: Request):
    return templates.TemplateResponse("main/pages/daily4.html", {"request": request})

@router.get("/daily5", response_class=HTMLResponse)
async def get_daily(request: Request):
    return templates.TemplateResponse("main/pages/daily5.html", {"request": request})

@router.get("/anunciante_escolha", response_class=HTMLResponse)
async def get_escolha(request: Request):
    return templates.TemplateResponse("main/pages/anunciante_escolha.html", {"request": request})



