def adicionar_mensagem(response, mensagem, tipo):
    response.set_cookie(
        key=f"mensagem_{tipo}",
        value=mensagem,
        max_age=3,
        httponly=True,
        samesite="strict",
    )


def adicionar_mensagem_sucesso(response, mensagem):
    adicionar_mensagem(response, mensagem, "sucesso")


def adicionar_mensagem_aviso(response, mensagem):
    adicionar_mensagem(response, mensagem, "aviso")


def adicionar_mensagem_erro(response, mensagem):
    adicionar_mensagem(response, mensagem, "erro")
