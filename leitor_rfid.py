
import serial
import time

PORTA = "COM11"
VELOCIDADE = 9600

try:
    arduino = serial.Serial(
        PORTA,
        VELOCIDADE,
        timeout=2
    )

    time.sleep(2)

    print("Sistema RFID iniciado!")
    print("Aproxime um cartão ou uma tag.\n")

    while True:
        linha = arduino.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if linha.startswith("UID:"):
            uid = linha[4:].strip().upper()

            print(f"UID identificada: {uid}")

except serial.SerialException as erro:
    print(f"Erro de comunicação: {erro}")
    print("Verifique a porta COM e se ela está livre.")

except KeyboardInterrupt:
    print("\nSistema encerrado.")

finally:
    if "arduino" in locals() and arduino.is_open:
        arduino.close()
