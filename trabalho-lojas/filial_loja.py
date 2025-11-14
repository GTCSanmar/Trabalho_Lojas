import socket
import random
import time

HOST = "127.0.0.1"
PORT = 10000

def simular_filial(id_filial):
    print(f"🏬 Filial {id_filial} iniciando operações...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        for i in range(1500):
            tipo = random.choice(["VENDA", "COMPRA"])
            valor = round(random.uniform(10, 500), 2)
            msg = f"{tipo} {valor}\n"
            s.sendall(msg.encode("utf-8"))
            # Aguarda confirmação do servidor
            s.recv(1024)
            # Delay pequeno para simular tempo real
            time.sleep(random.uniform(0.01, 0.05))

    print(f"✅ Filial {id_filial} concluiu as 1500 operações.")

if __name__ == "__main__":
    # Para simular 5 filiais, basta abrir 5 terminais e rodar:
    # python filial_loja.py
    import sys
    if len(sys.argv) > 1:
        id_filial = sys.argv[1]
    else:
        id_filial = random.randint(1, 99)
    simular_filial(id_filial)
