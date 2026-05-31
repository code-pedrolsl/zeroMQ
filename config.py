# IPs das suas instâncias AWS (substitua pelos IPs reais)
MACHINE_A = "SEU_IP_A"   # producer / server / publisher
MACHINE_B = "SEU_IP_B"   # middle / client / subscriber
MACHINE_C = "SEU_IP_C"   # consumer final

PORT_1 = "5678"   # A → B  (client-server, pub-sub, pipeline etapa 1)
PORT_2 = "5679"   # B → C  (pipeline etapa 2)
PORT_3 = "5680"   # reserva
