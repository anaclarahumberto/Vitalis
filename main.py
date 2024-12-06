import os
import dotenv
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.curtida_repo import CurtidaRepo
from repositories.publicacao_repo import PublicacaoRepo
from repositories.seguidor_repo import SeguidorRepo
from repositories.usuario_repo import UsuarioRepo
from routes.main_routes import router as main_router
from routes.usuario_routes import router as usuario_router
from util.auth import checar_autenticacao, checar_autorizacao
from util.exceptions import tratar_excecoes
from starlette.middleware.sessions import SessionMiddleware

UsuarioRepo.criar_tabela()
PublicacaoRepo.criar_tabela()
SeguidorRepo.criar_tabela()
CurtidaRepo.criar_tabela()
dotenv.load_dotenv()

app = FastAPI(dependencies=[Depends(checar_autorizacao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware("http")(checar_autenticacao)
tratar_excecoes(app)
app.include_router(main_router)
app.include_router(usuario_router)
