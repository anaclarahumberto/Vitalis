NOME_COOKIE_AUTH = "jwt-token"
NOME_COOKIE_EMAIL_TEMP = "email_temp"
NOME_COOKIE_NOME_TEMP = "nome_temp"
NOME_COOKIE_NOME_PERFIL_TEMP = "nome_perfil_temp"
NOME_COOKIE_ID_TEMP = "id_temp"


def adicionar_cookie(response, key, value, max_age):
    response.set_cookie(
        key=key, 
        value=value, 
        max_age=max_age, 
        httponly=True, 
        samesite="lax"
    )
    return response



