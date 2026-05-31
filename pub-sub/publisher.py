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
    socket  = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{PORT_1}")

    print(f"[PUBLISHER] Porta {PORT_1} | Topicos: TIME, UPPER, LOWER, REVERSE, COUNT")

    while True:
        time.sleep(3)

        t = "TIME " + time.asctime()
        socket.send(t.encode())

        text = random.choice(MESSAGES)
        socket.send(f"UPPER {text.upper()}".encode())
        socket.send(f"LOWER {text.lower()}".encode())
        socket.send(f"REVERSE {text[::-1]}".encode())
        socket.send(f"COUNT {text} | {len(text.split())} palavras, {len(text)} chars".encode())

if __name__ == "__main__":
    publisher()
