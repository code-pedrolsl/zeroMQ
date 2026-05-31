"""
Baseado em zmq_pub-sub.py (função server)
Mudanças: separado em publisher.py, IP externo via config.py,
          adicionados tópicos TEMP e LOAD além do TIME original
"""
import zmq, time, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1

def publisher():
    context = zmq.Context()
    socket  = context.socket(zmq.PUB)        # create a publisher socket
    socket.bind(f"tcp://*:{PORT_1}")          # bind socket to the address

    print(f"[PUBLISHER] Porta {PORT_1} | Topicos: TIME, TEMP, LOAD")

    while True:
        time.sleep(3)                         # wait (original usa 5s, reduzido para demo)

        # Tópico original preservado
        t = "TIME " + time.asctime()
        socket.send(t.encode())               # publish the current time

        # Novos tópicos
        socket.send(f"TEMP {round(random.uniform(20.0, 45.0), 1)} C".encode())
        socket.send(f"LOAD {round(random.uniform(0.0, 100.0), 1)} %".encode())

if __name__ == "__main__":
    publisher()
