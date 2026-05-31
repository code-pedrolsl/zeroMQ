"""
Baseado em taskwork.py (recebe) + tasksrc.py (envia)
É o estágio do meio: consumer/producer
Recebe do producer (Máquina A), processa e repassa para o consumer final (Máquina C)
"""
import zmq, time, pickle, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1, PORT_2, MACHINE_A

def middle(producer_ip=None):
    prod_ip = producer_ip or MACHINE_A

    context = zmq.Context()

    # PULL — recebe do producer (igual ao taskwork.py original)
    r = context.socket(zmq.PULL)             # create a pull socket
    r.connect(f"tcp://{prod_ip}:{PORT_1}")   # connect to task source (agora IP externo)
    print(f"[MIDDLE] Conectado ao producer em {prod_ip}:{PORT_1}")

    # PUSH — repassa para o consumer final (papel do tasksrc para o próximo estágio)
    p = context.socket(zmq.PUSH)
    p.bind(f"tcp://*:{PORT_2}")
    print(f"[MIDDLE] Repassando na porta {PORT_2}")

    while True:
        work     = pickle.loads(r.recv())    # receive work from a source
        origem   = work[0]
        workload = work[1]                   # mesma estrutura de tupla do original

        print(f"[MIDDLE] Recebeu {workload:03d} de {origem}")
        time.sleep(workload * 0.01)          # pretend to work

        task_out = ("middle-B", workload)    # encaminha identificando este estágio
        p.send(pickle.dumps(task_out))
        print(f"[MIDDLE] Repassou {workload:03d} para consumer-C")

if __name__ == "__main__":
    prod_ip = sys.argv[1] if len(sys.argv) > 1 else None
    middle(prod_ip)
