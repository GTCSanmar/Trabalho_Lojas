import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 10000

totais = {
    "vendas": 0.0,
    "compras": 0.0,
}
lock = threading.Lock()

def handle_filial(conn, addr, id_filial):
    print(f"[+] Filial {id_filial} conectada: {addr}")
    total_vendas = 0.0
    total_compras = 0.0

    try:
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break

            linhas = data.strip().split("\n")
            for linha in linhas:
                if not linha:
                    continue
                tipo, valor = linha.split()
                valor = float(valor)
                with lock:
                    if tipo == "VENDA":
                        totais["vendas"] += valor
                        total_vendas += valor
                    elif tipo == "COMPRA":
                        totais["compras"] += valor
                        total_compras += valor
            # Confirma recebimento
            conn.sendall(b"OK\n")
    except:
        pass
    finally:
        conn.close()
        print(f"[-] Filial {id_filial} finalizou: Vendas R${total_vendas:.2f} | Compras R${total_compras:.2f}")

def main():
    print("[*] Servidor Central iniciado...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Aguardando conexões em {HOST}:{PORT}")

        id_filial = 1
        threads = []

        # Aceita 5 filiais
        while id_filial <= 5:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_filial, args=(conn, addr, id_filial))
            t.start()
            threads.append(t)
            id_filial += 1

        # Espera todas terminarem
        for t in threads:
            t.join()

        print("\n📊 Relatório Final Consolidado 📊")
        print(f"Total de VENDAS:  R${totais['vendas']:.2f}")
        print(f"Total de COMPRAS: R${totais['compras']:.2f}")
        print(f"Lucro Bruto:      R${totais['vendas'] - totais['compras']:.2f}")

if __name__ == "__main__":
    main()
