import zmq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1
from datetime import datetime

def server():
    context = zmq.Context()
    socket  = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT_1}")

    print(f"[SERVER] Porta {PORT_1} | Comandos: UPPER, LOWER, REVERSE, COUNT, STOP")
    stats = {}

    while True:
        message = socket.recv()
        payload = message.decode().strip()
        ts      = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] Recebido: {payload!r}")

        if "STOP" in payload:
            socket.send(b"Server encerrando.")
            break

        if ":" in payload:
            cmd, text = payload.split(":", 1)
            cmd = cmd.upper()
            stats[cmd] = stats.get(cmd, 0) + 1
            if   cmd == "UPPER":   reply = text.upper()
            elif cmd == "LOWER":   reply = text.lower()
            elif cmd == "REVERSE": reply = text[::-1]
            elif cmd == "COUNT":   reply = f"{len(text.split())} palavras, {len(text)} chars"
            else:                  reply = f"Comando desconhecido: {cmd}"
        else:
            reply = payload + '*'
            stats["DEFAULT"] = stats.get("DEFAULT", 0) + 1

        socket.send(reply.encode())

    print("\n Estatisticas ")
    for k, v in stats.items():
        print(f"  {k}: {v} requisicoes")

if __name__ == "__main__":
    server()
