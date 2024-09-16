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

@router.get("/configuracoes/anuncios", response_class=HTMLResponse)
async def get_anuncio(request: Request):
    return templates.TemplateResponse("pages/anuncio.html", {"request": request})

@router.get("/configuracoes/anuncios/anunciante", response_class=HTMLResponse)
async def get_anunciante(request: Request):
    return templates.TemplateResponse("pages/anunciante.html", {"request": request})

@router.get("/configuracoes/editar_perfil", response_class=HTMLResponse)
async def get_editar(request: Request):
    return templates.TemplateResponse("pages/editar_perfil.html", {"request": request}) 

@router.get("/cupons", response_class=HTMLResponse)
async def get_cupons(request: Request):
    return templates.TemplateResponse("pages/cupons.html", {"request": request}) 

@router.get("/configuracoes/feedback", response_class=HTMLResponse)
async def get_feedback(request: Request):
    return templates.TemplateResponse("pages/feedback.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.get("/criar_conta", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("pages/criar_conta.html", {"request": request})

@router.get("/criar_conta/cadastro_profissional", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("pages/cadastro_profissional.html", {"request": request})

@router.get("/criar_conta/cadastro_paciente", response_class=HTMLResponse)
async def get_bem_vindo(request: Request):
    return templates.TemplateResponse("pages/cadastro_paciente.html", {"request": request})

@router.get("/loguin/esqueci_a_senha", response_class=HTMLResponse)
async def get_esqueci_a_senha(request: Request):
    return templates.TemplateResponse("pages/esqueci_a_senha.html", {"request": request})

@router.post("/loguin/esqueci_a_senha/senha_redefinada", response_class=HTMLResponse)
async def post_senha_redefinida(request: Request):
    return templates.TemplateResponse("pages/senha_redefinida.html", {"request": request})

@router.post("/entrar", response_class=HTMLResponse)
async def post_entrar(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})

@router.post("/conta_criada", response_class=HTMLResponse)
async def post_conta_criada(request: Request):
    # Aqui você pode processar os dados do formulário se necessário
    return templates.TemplateResponse("pages/conta_criada.html", {"request": request})