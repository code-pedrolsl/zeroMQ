import zmq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1, MACHINE_A

def client(server_ip=None):
    ip = server_ip or MACHINE_A
    context = zmq.Context()
    socket  = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{PORT_1}")

    requests = [
        b"Hello world",
        b"UPPER:sistemas distribuidos",
        b"LOWER:ZEROMQ AWS",
        b"REVERSE:pipeline",
        b"COUNT:o rato roeu a roupa do rei",
    ]

    for req in requests:
        socket.send(req)
        message = socket.recv()
        print(message.decode())

    socket.send(b"STOP")
    print(socket.recv().decode())

if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else None
    client(ip)
