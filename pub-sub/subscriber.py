import zmq, time, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1, MACHINE_A

def subscriber(pub_ip=None, topics=None):
    ip     = pub_ip or MACHINE_A
    topics = topics or ["TIME", "UPPER", "LOWER", "REVERSE", "COUNT"]

    context = zmq.Context()
    socket  = context.socket(zmq.SUB)
    socket.connect(f"tcp://{ip}:{PORT_1}")

    for t in topics:
        socket.setsockopt(zmq.SUBSCRIBE, t.encode())
        print(f"[SUBSCRIBER] Inscrito: {t}")

    print()
    counts = {t: 0 for t in topics}

    for i in range(20):
        msg   = socket.recv().decode()
        topic = msg.split()[0]
        body  = msg[len(topic)+1:]
        counts[topic] = counts.get(topic, 0) + 1
        ts = time.strftime("%H:%M:%S")
        print(f"[{ts}] [{topic}] {body}")

    print("\n Resumo ")
    for t, n in counts.items():
        print(f"  {t}: {n} mensagens recebidas")

if __name__ == "__main__":
    pub_ip = sys.argv[1] if len(sys.argv) > 1 else None
    topics = sys.argv[2:] if len(sys.argv) > 2 else None
    subscriber(pub_ip, topics)
