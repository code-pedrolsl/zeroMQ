# IPs das suas instâncias AWS (substitua pelos IPs reais)
MACHINE_A = "3.227.138.6"   # producer / server / publisher     # server
MACHINE_B = "3.235.239.109"   # middle / client / subscriber    # peer1
MACHINE_C = "100.52.205.229"   # consumer final                 # peer2

PORT_1 = "5678"   # A → B  (client-server, pub-sub, pipeline etapa 1)
PORT_2 = "5679"   # B → C  (pipeline etapa 2)
PORT_3 = "5680"   # reserva
