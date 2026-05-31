"""
Baseado em tasksrc.py
Mudanças: usa config.py em vez de constPipe.py, IP externo,
          envia tupla (origem, workload) como o original espera
"""
import zmq, time, pickle, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1

def producer():
    context = zmq.Context()
    socket  = context.socket(zmq.PUSH)       # create a push socket
    socket.bind(f"tcp://*:{PORT_1}")          # bind socket to address

    print(f"[PRODUCER] Gerando tarefas na porta {PORT_1} ...")
    time.sleep(1)

    for i in range(50):                       # 50 workloads
        workload = random.randint(1, 100)     # compute workload
        task     = ("producer-A", workload)   # tupla (origem, workload) como o original usa
        print(f"[PRODUCER] Enviando workload {workload:03d}")
        socket.send(pickle.dumps(task))       # send workload

    print("[PRODUCER] Concluido.")

if __name__ == "__main__":
    producer()
