# ZeroMQ – Messaging Distribuído em AWS
### Tarefa: Client-Server, Pub-Sub, Producer-Consumer

Baseado nos exemplos de Tanenbaum & vanSteen (2025). Os três padrões de comunicação foram adaptados para execução em **máquinas AWS distintas**, com as funcionalidades UPPER, LOWER, REVERSE e COUNT adicionadas em todos os padrões, e pipeline de 3 processos encadeados.

---

## Estrutura do projeto

```
zeromq-final/
├── config.py                  ← IPs e portas das instâncias (edite aqui)
├── client-server/
│   ├── server.py              → Máquina A
│   └── client.py              → Máquina B
├── pub-sub/
│   ├── publisher.py           → Máquina A
│   └── subscriber.py          → Máquina B (ou C)
└── pipeline/
    ├── producer.py            → Máquina A  (estágio 1)
    ├── middle.py              → Máquina B  (estágio 2 — consumer/producer)
    └── consumer.py            → Máquina C  (estágio 3)
```

---

## Configuração inicial

Edite `config.py` com os IPs públicos das suas instâncias EC2:

```python
MACHINE_A = "SEU_IP_A"   # server / publisher / producer
MACHINE_B = "SEU_IP_B"   # client / subscriber / middle
MACHINE_C = "SEU_IP_C"   # consumer final

PORT_1 = "5678"   # client-server, pub-sub e pipeline etapa A→B
PORT_2 = "5679"   # pipeline etapa B→C
```

Abra as portas 5678 e 5679 no **Security Group** de cada instância que recebe conexões. Instale a dependência em todas as máquinas:

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

Separado em `server.py` e `client.py` rodando em máquinas distintas (original usava `multiprocessing` no mesmo arquivo com `localhost`). O servidor responde comandos no formato `COMANDO:texto`. Sem `:`, mantém o comportamento original (adiciona `*`).

### Como rodar

```bash
# Máquina A — inicie primeiro
python client-server/server.py

# Máquina B
python client-server/client.py <IP_MAQUINA_A>
```

### Exemplo de saída

```
# server (Máquina A)
[SERVER] Porta 5678 | Comandos: UPPER, LOWER, REVERSE, COUNT, STOP
[10:32:01] Recebido: 'Hello world'
[10:32:01] Recebido: 'UPPER:sistemas distribuidos'
[10:32:01] Recebido: 'LOWER:ZEROMQ AWS'
[10:32:01] Recebido: 'REVERSE:pipeline'
[10:32:01] Recebido: 'COUNT:o rato roeu a roupa do rei'

=== Estatisticas ===
  DEFAULT: 1 requisicoes
  UPPER: 1 requisicoes
  LOWER: 1 requisicoes
  REVERSE: 1 requisicoes
  COUNT: 1 requisicoes

# client (Máquina B)
Hello world*
SISTEMAS DISTRIBUIDOS
zeromq aws
enilepip
5 palavras, 34 chars
```

---

## 2. Pub-Sub (padrão PUB/SUB)

### O que foi feito

Separado em `publisher.py` e `subscriber.py` em máquinas distintas (original usava `multiprocessing` com `localhost`). O publisher passou a publicar um tópico por comando: `TIME`, `UPPER`, `LOWER`, `REVERSE` e `COUNT`. O subscriber escolhe quais tópicos assinar via argumento.

### Como rodar

```bash
# Máquina A — inicie primeiro
python pub-sub/publisher.py

# Máquina B — assina todos os tópicos
python pub-sub/subscriber.py <IP_MAQUINA_A>

# Máquina B — assina apenas UPPER e REVERSE
python pub-sub/subscriber.py <IP_MAQUINA_A> UPPER REVERSE
```

### Exemplo de saída

```
# publisher (Máquina A)
[PUBLISHER] Porta 5678 | Topicos: TIME, UPPER, LOWER, REVERSE, COUNT

# subscriber (Máquina B)
[SUBSCRIBER] Inscrito: TIME
[SUBSCRIBER] Inscrito: UPPER
[SUBSCRIBER] Inscrito: LOWER
[SUBSCRIBER] Inscrito: REVERSE
[SUBSCRIBER] Inscrito: COUNT

[10:33:00] [TIME] Sun May 31 10:33:00 2026
[10:33:00] [UPPER] HELLO FROM MACHINE A
[10:33:00] [LOWER] hello from machine a
[10:33:00] [REVERSE] a enihcam morf olleh
[10:33:00] [COUNT] hello from machine a | 4 palavras, 19 chars
...

=== Resumo ===
  TIME: 4 mensagens recebidas
  UPPER: 4 mensagens recebidas
  LOWER: 4 mensagens recebidas
  REVERSE: 4 mensagens recebidas
  COUNT: 4 mensagens recebidas
```

---

## 3. Pipeline Producer → Middle → Consumer (padrão PUSH/PULL)

### O que foi feito

Pipeline de 3 estágios em 3 máquinas distintas (original tinha 2 estágios na mesma máquina). O `middle.py` é o estágio intermediário que age como consumer/producer: recebe a tarefa do producer, **aplica a transformação** (UPPER/LOWER/REVERSE/COUNT) e repassa o resultado ao consumer final.

```
Máquina A            Máquina B                    Máquina C
[producer] -5678→   [middle]           -5679→    [consumer]
envia cmd + texto   processa e transforma         exibe resultado + stats
```

### Como rodar

A ordem importa: middle e consumer devem estar prontos antes de o producer enviar.

```bash
# 1º — Máquina B
python pipeline/middle.py <IP_MAQUINA_A>

# 2º — Máquina C
python pipeline/consumer.py <IP_MAQUINA_B>

# 3º — Máquina A (por último)
python pipeline/producer.py
```

### Exemplo de saída

```
# producer (Máquina A)
[PRODUCER] Tarefa 001 | cmd=UPPER | texto='hello from producer on machine a'
[PRODUCER] Tarefa 002 | cmd=REVERSE | texto='sistemas distribuidos zeromq'
...

# middle (Máquina B)
[MIDDLE] Recebeu de producer-A | cmd=UPPER | texto='hello from producer on machine a'
[MIDDLE] Resultado [UPPER]: 'HELLO FROM PRODUCER ON MACHINE A'
[MIDDLE] Recebeu de producer-A | cmd=REVERSE | texto='sistemas distribuidos zeromq'
[MIDDLE] Resultado [REVERSE]: 'qmqoreZ sodiubirtsid sametsIs'
...

# consumer (Máquina C)
[CONSUMER] #001 | de=middle-B | [UPPER] → 'HELLO FROM PRODUCER ON MACHINE A'
[CONSUMER] #002 | de=middle-B | [REVERSE] → 'qmqoreZ sodiubirtsid sametsIs'
...
  [stats] 10 tarefas recebidas
    UPPER: 3
    REVERSE: 2
    LOWER: 3
    COUNT: 2
```
