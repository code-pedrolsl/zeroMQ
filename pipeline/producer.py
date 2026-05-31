import zmq, time, pickle, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1

COMMANDS = ["UPPER", "LOWER", "REVERSE", "COUNT"]

TEXTS = [
    "hello from producer on machine a",
    "sistemas distribuidos zeromq",
    "pipeline com tres estagios",
    "processamento distribuido na aws",
    "producer consumer pattern",
]

def producer():
    context = zmq.Context()
    socket  = context.socket(zmq.PUSH)
    socket.bind(f"tcp://*:{PORT_1}")

    print(f"[PRODUCER] Gerando tarefas na porta {PORT_1} ...")
    time.sleep(1)

    for i in range(50):
        cmd      = random.choice(COMMANDS)
        text     = random.choice(TEXTS)
        workload = random.randint(1, 100)
        task     = ("producer-A", workload, cmd, text)
        print(f"[PRODUCER] Tarefa {i+1:03d} | cmd={cmd} | texto='{text[:30]}...'")
        socket.send(pickle.dumps(task))
        time.sleep(0.2)

    print("[PRODUCER] Concluido.")

if __name__ == "__main__":
    producer()
