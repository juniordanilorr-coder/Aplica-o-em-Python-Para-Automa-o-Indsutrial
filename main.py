
import time
import serial

print("Programa iniciado")

from banco_dados import (
    cadastrar_usuario,
    adicionar_cartao_usuario,
    listar_usuarios,
    renomear_usuario,
    alterar_status,
    excluir_usuario
)

from autentificacao import verificar_cartao

PORTA = "COM11"
VELOCIDADE = 9600




def ler_uid(arduino):
    """Ativa o leitor, aguarda uma UID e pausa a leitura."""

    # Pausa e limpa possíveis leituras antigas
    arduino.write(b'P')
    time.sleep(0.1)
    arduino.reset_input_buffer()

    print("\nAproxime o cartão ou a tag do leitor...")

    # Libera a leitura no Arduino
    arduino.write(b'L')

    try:
        while True:
            linha = arduino.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if linha.startswith("UID:"):
                uid = linha[4:].strip().upper()
                print(f"\nUID identificada: {uid}")
                return uid
    finally:
        # Pausa o leitor após a leitura, inclusive em caso de erro
        arduino.write(b'P')


        
def cadastrar_com_rfid(arduino):
    nome = input("Digite o nome do usuário: ").strip()

    if not nome:
        print("O nome não pode ficar vazio.")
        return

    uid = ler_uid(arduino)
    sucesso, mensagem = cadastrar_usuario(nome, uid)

    print(mensagem)

def adicionar_tag_com_rfid(arduino):
    usuarios = listar_usuarios()

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    print("\n===== USUÁRIOS DISPONÍVEIS =====")
    ids_exibidos = set()

    for usuario in usuarios:
        id_usuario, nome, uid, ativo, data = usuario

        if id_usuario not in ids_exibidos:
            print(f"ID: {id_usuario} | Nome: {nome}")
            ids_exibidos.add(id_usuario)

    try:
        id_usuario = int(
            input("ID do usuário que receberá a nova tag: ").strip()
        )
    except ValueError:
        print("ID inválido.")
        return

    if id_usuario not in ids_exibidos:
        print("Usuário não encontrado.")
        return

    uid = ler_uid(arduino)

    sucesso, mensagem = adicionar_cartao_usuario(
        uid, id_usuario
    )

    print(mensagem)

def verificar_com_rfid(arduino):
    uid = ler_uid(arduino)
    resultado = verificar_cartao(uid)

    print(f"\nUID: {uid}")
    print(f"Usuário: {resultado['usuario'] or 'Não cadastrado'}")
    print(f"Resultado: {resultado['mensagem']}")


def mostrar_usuarios():
    usuarios = listar_usuarios()

    print("\n===== USUÁRIOS CADASTRADOS =====")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in usuarios:
        id_usuario, nome, uid, ativo, data = usuario
        status = "Ativo" if ativo == 1 else "Bloqueado"

        print(f"\nID: {id_usuario}")
        print(f"Nome: {nome}")
        print(f"UID: {uid}")
        print(f"Status: {status}")
        print(f"Cadastro: {data}")


def alterar_nome():
    uid = input("Digite a UID do cartão: ").strip().upper()
    novo_nome = input("Digite o novo nome: ").strip()

    if renomear_usuario(uid, novo_nome):
        print("Nome atualizado com sucesso.")
    else:
        print("UID não encontrada ou nome inválido.")


def mudar_status():
    uid = input("Digite a UID do cartão: ").strip().upper()

    print("1 - Bloquear")
    print("2 - Reativar")
    opcao = input("Escolha: ").strip()

    if opcao not in ("1", "2"):
        print("Opção inválida.")
        return

    ativo = 0 if opcao == "1" else 1

    if alterar_status(uid, ativo):
        print("Status atualizado com sucesso.")
    else:
        print("UID não encontrada.")


def remover_cadastro():
    uid = input("Digite a UID que deseja excluir: ").strip().upper()

    confirmacao = input(
        f"Confirma a exclusão do cadastro {uid}? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    if excluir_usuario(uid):
        print("Cadastro excluído com sucesso.")
    else:
        print("UID não encontrada.")



def iniciar_sistema():
    print("Entrou na função iniciar_sistema")

    try:
        with serial.Serial(PORTA, VELOCIDADE, timeout=1) as arduino:
            time.sleep(2)
            arduino.write(b'P')
            arduino.reset_input_buffer()

            while True:
                print("\n===== SISTEMA RFID =====")
                print("1 - Cadastrar usuário")
                print("2 - Verificar cartão")
                print("3 - Listar usuários")
                print("4 - Renomear usuário")
                print("5 - Bloquear ou reativar cartão")
                print("6 - Excluir cadastro")
                print("7 - Associar nova tag a usuário existente")
                print("0 - Encerrar")

                opcao = input("Escolha uma opção: ").strip()

                if opcao == "1":
                    cadastrar_com_rfid(arduino)
                elif opcao == "2":
                    verificar_com_rfid(arduino)
                elif opcao == "3":
                    mostrar_usuarios()
                elif opcao == "4":
                    alterar_nome()
                elif opcao == "5":
                    mudar_status()
                elif opcao == "6":
                    remover_cadastro()
                elif opcao == "7":
                    adicionar_tag_com_rfid(arduino)
                elif opcao == "0":
                    print("Sistema encerrado.")
                    break
                else:
                    print("Opção inválida.")

    except serial.SerialException as erro:
        print(f"Erro de comunicação: {erro}")
        print("Verifique a porta COM e feche o Monitor Serial.")

    except KeyboardInterrupt:
        print("\nSistema encerrado.")


iniciar_sistema()


