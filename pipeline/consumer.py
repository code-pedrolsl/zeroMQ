"""
Baseado em taskwork.py
Mudanças: recebe do middle (Máquina B) via PORT_2, IP externo via argumento,
          adiciona estatísticas de workload recebido
"""
import zmq, time, pickle, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_2, MACHINE_B

def consumer(middle_ip=None):
    ip = middle_ip or MACHINE_B

    context = zmq.Context()
    r = context.socket(zmq.PULL)             # create a pull socket
    r.connect(f"tcp://{ip}:{PORT_2}")        # connect to task source (agora IP externo)

    print(f"[CONSUMER] Conectado ao middle em {ip}:{PORT_2}")

    total     = 0
    workloads = []

    while True:
        work     = pickle.loads(r.recv())    # receive work from a source
        origem   = work[0]
        workload = work[1]
        total   += 1
        workloads.append(workload)

        print(f"[CONSUMER] Recebeu {workload:03d} de {origem}")
        time.sleep(workload * 0.01)          # pretend to work

        if total % 10 == 0:
            med = sum(workloads[-10:]) / 10
            print(f"\n  [stats] {total} tarefas processadas | media ultimas 10: {med:.1f}\n")

if __name__ == "__main__":
    middle_ip = sys.argv[1] if len(sys.argv) > 1 else None
    consumer(middle_ip)
