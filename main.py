import os
import dotenv
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.usuario_repo import UsuarioRepo
from routes.main_routes import router as main_router
from routes.usuario_routes import router as usuario_router
from util.auth import checar_autenticacao, checar_autorizacao
from util.exceptions import tratar_excecoes
from starlette.middleware.sessions import SessionMiddleware

UsuarioRepo.criar_tabela()
dotenv.load_dotenv()

app = FastAPI(dependencies=[Depends(checar_autorizacao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware("http")(checar_autenticacao)
tratar_excecoes(app)
app.add_middleware(SessionMiddleware, secret_key=os.getenv('JWT_SECRET'))
app.include_router(main_router)
app.include_router(usuario_router)
