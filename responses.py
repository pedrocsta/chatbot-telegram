def sample_response(input_text) -> str:
    user_message = str(input_text).lower()

    if user_message in ("oi", "ola", "olá"):
        return "Olá, tudo bem?"

    return "Não estou lhe entendendo, tente novamente."
