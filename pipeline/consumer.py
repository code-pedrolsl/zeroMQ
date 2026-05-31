"""
Baseado em taskwork.py
Recebe do middle o resultado já processado (UPPER/LOWER/REVERSE/COUNT)
e exibe com estatísticas por comando
"""
import zmq, time, pickle, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_2, MACHINE_B

def consumer(middle_ip=None):
    ip = middle_ip or MACHINE_B

    context = zmq.Context()
    r = context.socket(zmq.PULL)             # create a pull socket
    r.connect(f"tcp://{ip}:{PORT_2}")        # connect to task source (IP externo)

    print(f"[CONSUMER] Conectado ao middle em {ip}:{PORT_2}\n")

    total  = 0
    stats  = {}   # contagem por comando

    while True:
        work     = pickle.loads(r.recv())    # receive work from a source
        origem   = work[0]
        workload = work[1]
        cmd      = work[2]
        result   = work[3]
        total   += 1
        stats[cmd] = stats.get(cmd, 0) + 1

        print(f"[CONSUMER] #{total:03d} | de={origem} | [{cmd}] → '{result[:50]}'")
        time.sleep(workload * 0.01)          # pretend to work

        if total % 10 == 0:
            print(f"\n  [stats] {total} tarefas recebidas")
            for k, v in stats.items():
                print(f"    {k}: {v}")
            print()

if __name__ == "__main__":
    middle_ip = sys.argv[1] if len(sys.argv) > 1 else None
    consumer(middle_ip)
