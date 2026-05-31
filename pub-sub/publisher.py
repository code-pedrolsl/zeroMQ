"""
Baseado em zmq_pub-sub.py (função server)
Mudanças: separado em publisher.py, IP externo via config.py,
          publisher envia mensagens com comandos UPPER/LOWER/REVERSE/COUNT
          para que o subscriber processe ao receber
"""
import zmq, time, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1

MESSAGES = [
    "hello from machine a",
    "Sistemas Distribuidos com ZeroMQ",
    "pub sub pattern running on AWS",
    "mensagem de teste do publisher",
    "ZeroMQ is fast and reliable",
]

def publisher():
    context = zmq.Context()
    socket  = context.socket(zmq.PUB)        # create a publisher socket
    socket.bind(f"tcp://*:{PORT_1}")          # bind socket to the address

    print(f"[PUBLISHER] Porta {PORT_1} | Topicos: TIME, UPPER, LOWER, REVERSE, COUNT")

    while True:
        time.sleep(3)                         # wait (original usa 5s)

        # Tópico original preservado
        t = "TIME " + time.asctime()
        socket.send(t.encode())               # publish the current time

        # Novos tópicos: cada um envia uma mensagem com a transformação aplicada
        text = random.choice(MESSAGES)
        socket.send(f"UPPER {text.upper()}".encode())
        socket.send(f"LOWER {text.lower()}".encode())
        socket.send(f"REVERSE {text[::-1]}".encode())
        socket.send(f"COUNT {text} | {len(text.split())} palavras, {len(text)} chars".encode())

if __name__ == "__main__":
    publisher()
