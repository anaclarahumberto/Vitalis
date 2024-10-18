NOME_COOKIE_AUTH = "token"


def adicionar_cookie_auth(response, token):
    response.set_cookie(
        key=NOME_COOKIE_AUTH, value=token, max_age=1800, httponly=True, samesite="lax"
    )
    return response


def excluir_cookie_auth(response):
    response.set_cookie(key=NOME_COOKIE_AUTH, value=" ", httponly=True, expires=0)
    return response



