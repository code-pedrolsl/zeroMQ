"""
Baseado em zmq_client-server.py
Mudanças: separado em client.py, conecta em IP externo via argumento (não localhost)
"""
import zmq, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import PORT_1, MACHINE_A

def client(server_ip=None):
    ip = server_ip or MACHINE_A
    context = zmq.Context()
    socket  = context.socket(zmq.REQ)        # create request socket
    socket.connect(f"tcp://{ip}:{PORT_1}")    # connect (agora IP externo)

    requests = [
        b"Hello world",                       # compatibilidade com o original
        b"UPPER:sistemas distribuidos",
        b"LOWER:ZEROMQ AWS",
        b"REVERSE:pipeline",
        b"COUNT:o rato roeu a roupa do rei",
    ]

    for req in requests:
        socket.send(req)                      # send message
        message = socket.recv()               # block until response
        print(message.decode())               # print result

    socket.send(b"STOP")                      # tell server to stop
    print(socket.recv().decode())

if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else None
    client(ip)
