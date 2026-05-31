# ZeroMQ - Messaging Distribuído em AWS
### Tarefa: Client-Server, Pub-Sub, Producer-Consumer

## Estrutura do projeto

```
zeromq-final/
├── config.py                   IPs e portas das instâncias
├── client-server/
│   ├── server.py               Máquina A
│   └── client.py               Máquina B
├── pub-sub/
│   ├── publisher.py            Máquina A
│   └── subscriber.py           Máquina B (ou C)
└── pipeline/
    ├── producer.py             Máquina A  (estágio 1)
    ├── middle.py               Máquina B  (estágio 2 - consumer/producer)
    └── consumer.py             Máquina C  (estágio 3)
```

---

## Configuração inicial

Edite `config.py` com os IPs públicos das suas instâncias EC2:

```python
MACHINE_A = "SEU_IP_A"   # server / publisher / producer (Server)
MACHINE_B = "SEU_IP_B"   # client / subscriber / middle (Peer1)
MACHINE_C = "SEU_IP_C"   # consumer final (Peer2)

PORT_1 = "5678"
PORT_2 = "5679"
```

```bash
pip install pyzmq
```

---

## Funcionalidades adicionadas (comuns aos três padrões)

Os quatro comandos abaixo foram adicionados em todos os padrões de comunicação:

| Comando | Descrição |
|---|---|
| `UPPER` | Converte o texto para maiúsculas |
| `LOWER` | Converte o texto para minúsculas |
| `REVERSE` | Inverte a string |
| `COUNT` | Conta palavras e caracteres do texto |

---

## 1. Client-Server (padrão REQ/REP)

### O que foi feito

Separado em `server.py` e `client.py` rodando em máquinas distintas (original usava `multiprocessing` no mesmo arquivo com `localhost`). O servidor responde comandos no formato `COMANDO:texto`. 

### Como rodar

```bash
# Máquina A - inicie primeiro
python3 client-server/server.py

# Máquina B
python3 client-server/client.py <IP_MAQUINA_A>
```
---

## 2. Pub-Sub (padrão PUB/SUB)

### O que foi feito

Separado em `publisher.py` e `subscriber.py` em máquinas distintas (original usava `multiprocessing` com `localhost`). O publisher passou a publicar um tópico por comando: `TIME`, `UPPER`, `LOWER`, `REVERSE` e `COUNT`. O subscriber escolhe quais tópicos assinar via argumento.

### Como rodar

```bash
# Máquina A - inicie primeiro
python3 pub-sub/publisher.py

# Máquina B - assina todos os tópicos
python3 pub-sub/subscriber.py <IP_MAQUINA_A>

# Máquina B - assina apenas UPPER e REVERSE
python3 pub-sub/subscriber.py <IP_MAQUINA_A> UPPER REVERSE
```
---

## 3. Pipeline Producer  Middle  Consumer (padrão PUSH/PULL)

### O que foi feito

Pipeline de 3 estágios em 3 máquinas distintas (original tinha 2 estágios na mesma máquina). O `middle.py` é o estágio intermediário que age como consumer/producer: recebe a tarefa do producer, **aplica a transformação** (UPPER/LOWER/REVERSE/COUNT) e repassa o resultado ao consumer final.

```
Máquina A            Máquina B                    Máquina C
[producer] -5678   [middle]           -5679    [consumer]
envia cmd + texto   processa e transforma         exibe resultado + stats
```

### Como rodar

A ordem importa: middle e consumer devem estar prontos antes de o producer enviar.

```bash
# 1º - Máquina B
python3 pipeline/middle.py <IP_MAQUINA_A>

# 2º - Máquina C
python3 pipeline/consumer.py <IP_MAQUINA_B>

# 3º - Máquina A (por último)
python3 pipeline/producer.py
```
