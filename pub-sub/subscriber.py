"""
Baseado em zmq_pub-sub.py (função client)
Mudanças: separado em subscriber.py, conecta em IP externo via argumento,
          permite escolher tópicos (original só tinha TIME)
"""
import zmq, time, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1, MACHINE_A

def subscriber(pub_ip=None, topics=None):
    ip     = pub_ip or MACHINE_A
    topics = topics or ["TIME", "TEMP", "LOAD"]

    context = zmq.Context()
    socket  = context.socket(zmq.SUB)        # create a subscriber socket
    socket.connect(f"tcp://{ip}:{PORT_1}")    # connect to the server (agora IP externo)

    for t in topics:
        socket.setsockopt(zmq.SUBSCRIBE, t.encode())  # subscribe
        print(f"[SUBSCRIBER] Inscrito: {t}")

    for i in range(15):                       # 15 iterações (original usa 5, aumentado para ver todos os tópicos)
        msg = socket.recv()                   # receive a message
        print(msg.decode())                   # print the result

if __name__ == "__main__":
    pub_ip = sys.argv[1] if len(sys.argv) > 1 else None
    topics = sys.argv[2:] if len(sys.argv) > 2 else None
    subscriber(pub_ip, topics)
