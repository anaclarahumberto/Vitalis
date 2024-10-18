from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.mensagens import adicionar_mensagem_erro


templates = Jinja2Templates(directory="templates")


def tratar_excecoes(app: FastAPI):

    @app.exception_handler(401)
    async def unauthorized_exception_handler(request, exc):
        return_url = f"/login?return_url={request.url.path}"
        response = RedirectResponse(f"{return_url}")
        adicionar_mensagem_erro(
            response,
            f"Você precisa estar autenticado para acessar a página do endereço {request.url.path}.",
        )
        return response

    @app.exception_handler(403)
    async def forbidden_exception_handler(request, exc):
        usuarioAutenticadoDto = request.state.usuario
        return_url = f"/login?return_url={request.url.path}"
        response = RedirectResponse(f"{return_url}")
        adicionar_mensagem_erro(
            response,
            f"Você está logado como {usuarioAutenticadoDto.nome} e seu perfil de usuário não tem permissão para acessar a página do endereço {request.url.path}. Entre com as credenciais de um perfil compatível.",
        )
        return response

    @app.exception_handler(404)
    async def not_found_exception_handler(request, exc):
        return templates.TemplateResponse(
            "shared/pages/404.html", {"request": request}, status_code=404
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        dados = {
            "request": request, 
            "detail": f"Erro na requisição HTTP:<br>{type(exc).__name__}: {exc}",
            "status_code": exc.status_code
        }
        return templates.TemplateResponse(
            "shared/pages/error.html", dados)

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        dados = {
            "request": request,
            "detail": f"Erro interno do servidor.<br>{type(exc).__name__}: {exc}",
            "status_code": 500
        }
        return templates.TemplateResponse("shared/pages/error.html", dados)
