
from banco_dados import consultar_usuario


def verificar_cartao(uid):
    usuario = consultar_usuario(uid)

    if usuario is None:
        return {
            "autorizado": False,
            "mensagem": "Cartão não cadastrado",
            "usuario": None
        }

    if usuario[3] == 0:
        return {
            "autorizado": False,
            "mensagem": "Cartão bloqueado",
            "usuario": usuario[1]
        }

    return {
        "autorizado": True,
        "mensagem": "Acesso autorizado",
        "usuario": usuario[1]
    }
