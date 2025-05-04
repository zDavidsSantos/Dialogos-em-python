import time
from datetime import datetime

def exibir_relogio(chamas_ativas):
    print("\nRelógio Cavaleiros do Zodíaco")
    print("================================")
    for i in range(12):
        if i < chamas_ativas:
            print(f"Hora {i+1}: 🔥")
        else:
            print(f"Hora {i+1}: ❌")
    print("================================\n")

def main():
    while True:
        agora = datetime.now()
        hora_atual = agora.hour % 12  # Ajusta para formato de 12 horas
        chamas_ativas = 12 - hora_atual

        exibir_relogio(chamas_ativas)
        print(f"Hora atual: {agora.strftime('%H:%M:%S')}")
        time.sleep(60)  # Atualiza a cada minuto

if __name__ == "__main__":
    main()