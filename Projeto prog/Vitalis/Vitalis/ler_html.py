def ler_html(nome: str) -> str:
    with open(f"html/{nome}.html", "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
        return conteudo