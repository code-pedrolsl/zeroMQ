import zmq, time, pickle, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1, PORT_2, MACHINE_A

def apply_command(cmd, text):
    if   cmd == "UPPER":   return text.upper()
    elif cmd == "LOWER":   return text.lower()
    elif cmd == "REVERSE": return text[::-1]
    elif cmd == "COUNT":   return f"{len(text.split())} palavras, {len(text)} chars"
    else:                  return text

def middle(producer_ip=None):
    prod_ip = producer_ip or MACHINE_A

    context = zmq.Context()

    r = context.socket(zmq.PULL)
    r.connect(f"tcp://{prod_ip}:{PORT_1}")
    print(f"[MIDDLE] Conectado ao producer em {prod_ip}:{PORT_1}")

    p = context.socket(zmq.PUSH)
    p.bind(f"tcp://*:{PORT_2}")
    print(f"[MIDDLE] Repassando resultados na porta {PORT_2}\n")

    while True:
        work     = pickle.loads(r.recv())
        origem   = work[0]
        workload = work[1]
        cmd      = work[2]
        text     = work[3]

        print(f"[MIDDLE] Recebeu de {origem} | cmd={cmd} | texto='{text[:30]}'")
        time.sleep(workload * 0.01)

        result = apply_command(cmd, text)

        task_out = ("middle-B", workload, cmd, result)
        p.send(pickle.dumps(task_out))
        print(f"[MIDDLE] Resultado [{cmd}]: '{result[:40]}'")

if __name__ == "__main__":
    prod_ip = sys.argv[1] if len(sys.argv) > 1 else None
    middle(prod_ip)
