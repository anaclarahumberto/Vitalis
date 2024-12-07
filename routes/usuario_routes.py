import base64
from datetime import date, datetime, timedelta
import locale
import random
from typing import List
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import APIRouter, Form
import os

import jwt
from pydantic import BaseModel
from models.publicacao_model import Publicacao
from models.usuario_model import Usuario
from repositories.curtida_repo import CurtidaRepo
from repositories.publicacao_repo import PublicacaoRepo
from repositories.seguidor_repo import SeguidorRepo
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

def obter_publicacoes_feed(usuario_logado_id: int):
    usuarios_seguidos = SeguidorRepo.obter_seguindo(usuario_logado_id)
    
    publicacoes_feed = []
    
    for usuario_id in usuarios_seguidos:
        usuario = UsuarioRepo.obter_dados_perfil_seguido(usuario_id)
        
        foto_perfil = usuario.foto_perfil if hasattr(usuario, 'foto_perfil') else None
        
        usuario_foto = f"/static/img/{usuario.id}.jpeg" if foto_perfil else "/static/img/usuario.jpg"
        
        publicacoes = PublicacaoRepo.obter_publicacoes_por_usuario(usuario_id)
        
        for publicacao in publicacoes:
            publicacao['usuario_nome'] = usuario.nome_perfil
            publicacao['usuario_foto'] = usuario_foto
            publicacao['usuario_id'] = usuario.id 
            publicacao["curtido"] = CurtidaRepo.verificar_curtida(publicacao["id_publicacao"], usuario_logado_id)
            publicacoes_feed.append(publicacao)

    
    return sorted(publicacoes_feed, key=lambda x: x['data_criacao'], reverse=True)

def obter_stories_feed(usuario_logado_id: int):
    usuarios_seguidos = SeguidorRepo.obter_seguindo(usuario_logado_id)

    stories_feed = []

    for usuario_id in usuarios_seguidos:
        usuario = UsuarioRepo.obter_dados_perfil_seguido(usuario_id)
        
        foto_perfil = usuario.foto_perfil if hasattr(usuario, 'foto_perfil') else None
        
        usuario_foto = f"/static/img/{usuario.id}.jpeg" if foto_perfil else "/static/img/usuario.jpg"
        
        story = {
            'usuario_nome': usuario.nome_perfil,
            'usuario_foto': usuario_foto
        }
        
        stories_feed.append(story)


    return stories_feed

@router.get("/feed", response_class=HTMLResponse)
async def get_root(request: Request):
    stories = obter_stories_feed(request.state.usuario.id)
    publicacoes = obter_publicacoes_feed(request.state.usuario.id)
    random.shuffle(publicacoes)
    return templates.TemplateResponse("main/pages/index.html", {"request": request, "publicacoes": publicacoes, "stories": stories,})

@router.post("/curtir_publicacao")
async def curtir_publicacao(request: Request):
    body = await request.json()
    id_publicacao = body.get("id_publicacao")
    id_usuario = body.get("id_usuario")
    sucesso = CurtidaRepo.curtir_publicacao(id_publicacao, id_usuario)
    if sucesso:
        return JSONResponse({"status": "sucesso"})
    return JSONResponse({"status": "erro"})

@router.post("/descurtir_publicacao")
async def descurtir_publicacao(request: Request):
    body = await request.json()
    id_publicacao = body.get("id_publicacao")
    id_usuario = body.get("id_usuario")

    sucesso = CurtidaRepo.remover_curtida_publicacao(id_publicacao, id_usuario)
    if sucesso:
        return JSONResponse({"status": "sucesso"})
    return JSONResponse({"status": "erro"})

@router.get("/pesquisar_perfil", response_model=List[Usuario])
async def pesquisar_perfil_endpoint(nome_perfil: str = Query(..., min_length=3)):
    usuarios = UsuarioRepo.pesquisar_perfil(nome_perfil)
    return usuarios

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


@router.get("/plano", response_class=HTMLResponse)
async def get_plano(request: Request):
    return templates.TemplateResponse("main/pages/plano.html", {"request": request})

@router.get("/fazer_upgrade_plano", response_class=HTMLResponse)
async def get_fazer_upgrade_plano(request: Request):
    print(request.state.usuario.email)
    UsuarioRepo.fazer_upgrade_plano(2, request.state.usuario.email)
    return templates.TemplateResponse("main/pages/plano_notificacao.html", {"request": request})

@router.get("/tela_cancelar_plano", response_class=HTMLResponse)
async def get_cancelar_plano(request: Request):
    return templates.TemplateResponse("main/pages/tela_cancelar_plano.html", {"request": request})

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
    publicacoes = PublicacaoRepo.obter_publicacoes_por_usuario(request.state.usuario.id)
    numero_publicacoes = PublicacaoRepo.obter_numero_publicacoes(request.state.usuario.id)
    numero_seguidores = SeguidorRepo.obter_numero_seguidores(request.state.usuario.id)
    numero_seguindo = SeguidorRepo.obter_numero_seguindo(request.state.usuario.id)
    dados_perfil = UsuarioRepo.obter_dados_perfil(request.state.usuario.id)

    return templates.TemplateResponse("main/pages/perfil.html", {
        "request": request,
        "dados_perfil": dados_perfil,
        "publicacoes": publicacoes,
        'numero_publicacoes': numero_publicacoes,
        'numero_seguidores': numero_seguidores,
        'numero_seguindo': numero_seguindo,
    })

@router.get("/editar_perfil", response_class=HTMLResponse)
async def get_editar(request: Request):
    dados_perfil = UsuarioRepo.obter_dados_perfil(request.state.usuario.id)
    return templates.TemplateResponse("main/pages/editar_perfil.html", {"request": request, "dados_perfil": dados_perfil,}) 

@router.post("/atualizar_perfil")
async def editar_perfil(request: Request):
    dados_usuario = UsuarioRepo.obter_dados_perfil(request.state.usuario.id)
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
    if dados["telefone"] != dados_usuario.telefone:
        if not is_phone_number(dados["telefone"]):
            adicionar_mensagem_erro(response, "Esse não é um telefone valido. Confira-o")
            return response
        if not UsuarioRepo.is_phone_unique(dados["telefone"]):
            adicionar_mensagem_erro(response, "Outra conta está usando o mesmo telefone.")
            return response
        
    foto_perfil = request.state.usuario.foto_perfil
    if not foto_perfil:
        foto_perfil = bool(foto_perfil_blob)

    # Atualiza os dados do usuário
    atualizacao_sucesso = UsuarioRepo.atualizar_dados_perfil(
        foto_perfil = foto_perfil,
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

@router.get("/visitar_perfil", response_class=HTMLResponse)
async def get_visitar_perfil(request: Request, usuario_id: int):
    perfil_visitado = UsuarioRepo.obter_dados_perfil_visitado(usuario_id)
    publicacoes = PublicacaoRepo.obter_publicacoes_por_usuario(usuario_id)
    numero_publicacoes = PublicacaoRepo.obter_numero_publicacoes(usuario_id)
    numero_seguidores = SeguidorRepo.obter_numero_seguidores(usuario_id)
    numero_seguindo = SeguidorRepo.obter_numero_seguindo(usuario_id)

    return templates.TemplateResponse("main/pages/visitar_perfil.html", {
        "request": request,
        "perfil_visitado": perfil_visitado,
        "publicacoes": publicacoes,
        'numero_publicacoes': numero_publicacoes,
        'numero_seguidores': numero_seguidores,
        'numero_seguindo': numero_seguindo,
    })

class SeguirRequest(BaseModel):
    seguidor_id: int
    seguido_id: int

@router.get("/verificar_seguindo")
async def verificar_seguindo(request: Request):
    id_usuario_seguidor = request.state.usuario.id  
    id_usuario_seguido = int(request.query_params["id_usuario_seguido"])  
    
    try:
        is_seguidor = SeguidorRepo.verificar_seguindo(id_usuario_seguidor, id_usuario_seguido)
        return {"is_seguidor": is_seguidor}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@router.post("/seguir_usuario")
async def seguir_usuario(request: SeguirRequest):
    try:
        sucesso = SeguidorRepo.seguir_usuario(request.seguidor_id, request.seguido_id)
        if sucesso:
            return {"status": "sucesso", "message": "Você agora segue este usuário."}
        else:
            raise HTTPException(status_code=400, detail="Não foi possível seguir o usuário.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
    
@router.post("/deixar_de_seguir")
async def deixar_de_seguir(request: SeguirRequest):
    try:
        sucesso = SeguidorRepo.deixar_de_seguir(request.seguidor_id, request.seguido_id)
        if sucesso:
            return {"status": "sucesso", "message": "Você deixou de seguir este usuário."}
        else:
            raise HTTPException(status_code=400, detail="Não foi possível deixar de seguir o usuário.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


@router.get("/entrarMaroquio", response_class=HTMLResponse)
async def get_perfil(request: Request):
    return templates.TemplateResponse("main/pages/entrar.html", {"request": request})

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

@router.get("/tela_cancelar_plano_efetivo", response_class=HTMLResponse)
async def get_cancelou_plano(request: Request):
    return templates.TemplateResponse("main/pages/tela_cancelar_plano_efetivo.html", {"request": request})

@router.get("/tela_cancelar_plano", response_class=HTMLResponse)
async def get_cancelar_plano(request: Request):
    return templates.TemplateResponse("main/pages/tela_cancelar_plano_.html", {"request": request})


@router.get("/plano_mantido", response_class=HTMLResponse)
async def get_manter_plano(request: Request):
    return templates.TemplateResponse("main/pages/plano_mantido.html", {"request": request})

@router.get("/plano_2", response_class=HTMLResponse)
async def get_conta_criada_com_sucesso(request: Request):
    return templates.TemplateResponse("main/pages/plano_2.html", {"request": request})