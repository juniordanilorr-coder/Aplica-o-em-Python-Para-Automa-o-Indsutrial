# Sistema de Controle de Acesso RFID

Projeto acadêmico desenvolvido no curso de Técnico em Automação Industrial, utilizando Arduino, Python e banco de dados SQLite.

O sistema realiza o cadastro e a identificação de usuários por meio de cartões e tags RFID, permitindo controlar a autorização de acesso de cada dispositivo cadastrado.

## Objetivo do projeto

Desenvolver um sistema de identificação e controle de acesso que integre hardware e software, utilizando um leitor RFID conectado a um Arduino e uma aplicação desktop desenvolvida em Python.

O projeto tem como cenário inicial uma simulação de controle de acesso ao um parque, podendo ser adaptado para outros ambientes.

## Tecnologias utilizadas

- **Python:** desenvolvimento da aplicação e gerenciamento das operações.
- **Arduino:** comunicação com o leitor RFID e aquisição das identificações.
- **MFRC522:** módulo responsável pela leitura dos cartões e tags RFID.
- **SQLite:** armazenamento dos usuários e dispositivos cadastrados.
- **Git e GitHub:** versionamento e gerenciamento do código-fonte.
- **Visual Studio Code:** ambiente de desenvolvimento.

## Componentes de hardware

- Arduino Uno.
- Módulo leitor RFID-RC522.
- Cartões RFID.
- Tags RFID tipo chaveiro.
- Cabos de conexão.

## Funcionalidades implementadas

- Cadastro de usuários associado a uma tag RFID.
- Associação de várias tags a um mesmo usuário.
- Identificação de cartões e tags cadastrados.
- Autenticação e verificação de autorização.
- Listagem dos usuários e dispositivos cadastrados.
- Alteração do nome de um usuário.
- Bloqueio e reativação individual de cartões ou tags.
- Exclusão de dispositivos cadastrados.
- Exclusão do usuário quando seu último dispositivo é removido.
- Controle da leitura RFID por comandos enviados pelo Python ao Arduino.

## Estrutura do banco de dados

O sistema utiliza SQLite e possui duas tabelas principais:

**usuarios:** armazena as informações das pessoas cadastradas, incluindo identificador, código e nome.

**dispositivos_rfid:** armazena os cartões e tags associados aos usuários, incluindo código do dispositivo, UID, status e data de cadastro.

Cada dispositivo possui uma UID única e um status independente. Dessa forma, uma pessoa pode possuir mais de uma tag, sem precisar criar vários cadastros.

## Comunicação entre Arduino e Python

A comunicação ocorre pela porta serial, utilizando velocidade de 9600 baud.

O Python envia comandos ao Arduino para controlar a leitura:

- `L`: libera a leitura de uma tag RFID.
- `P`: pausa a leitura RFID.

Quando uma tag é identificada, o Arduino envia sua UID ao Python, que realiza a consulta no banco de dados e executa a operação correspondente.

## Organização dos arquivos

- `main.py`: menu principal e gerenciamento das operações.
- `banco_dados.py`: criação e gerenciamento do banco SQLite.
- `autentificacao.py`: regras de autenticação dos dispositivos.
- `leitor_rfid.py`: módulo relacionado à leitura RFID.

## Como executar o projeto

### 1. Requisitos

- Python instalado.
- Arduino IDE instalado.
- Bibliotecas `pyserial` e `MFRC522`.
- Arduino Uno e módulo RFID-RC522.

### 2. Instalar a dependência Python

No terminal:

```bash
pip install pyserial
```

### 3. Preparar o Arduino

Carregue o código do leitor RFID na placa Arduino utilizando a Arduino IDE.

### 4. Configurar a porta serial

No arquivo `main.py`, configure a porta COM correspondente ao Arduino:

```python
PORTA = "COM11"
```

Altere o valor conforme a porta utilizada no computador.

### 5. Inicializar o banco de dados

Na pasta do projeto, execute:

```bash
python banco_dados.py
```

### 6. Executar o sistema

```bash
python main.py
```

## Desenvolvimento futuro

- Desenvolvimento de uma interface gráfica para gerenciamento do sistema.
- Implementação de histórico de acessos.
- Ampliação das funcionalidades de gerenciamento.
- Melhorias na apresentação e visualização das informações.

## Status do projeto

Em desenvolvimento.

Projeto acadêmico desenvolvido como atividade prática do curso de Técnico em Automação Industrial.
