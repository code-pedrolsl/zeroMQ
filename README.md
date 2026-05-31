# ZeroMQ – Messaging Distribuído em AWS
### Tarefa: Client-Server, Pub-Sub, Producer-Consumer

Baseado nos exemplos de Tanenbaum & vanSteen (2025). Os três padrões de comunicação foram adaptados para execução em **máquinas AWS distintas**, com novas funcionalidades e um pipeline de 3 processos encadeados.

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

Edite `config.py` com os IPs públicos das suas instâncias EC2 antes de rodar qualquer coisa:

```python
MACHINE_A = "SEU_IP_A"   # server / publisher / producer
MACHINE_B = "SEU_IP_B"   # client / subscriber / middle
MACHINE_C = "SEU_IP_C"   # consumer final

PORT_1 = "5678"   # usado por client-server, pub-sub e pipeline etapa A→B
PORT_2 = "5679"   # usado pelo pipeline etapa B→C
```

As portas 5678 e 5679 devem estar abertas no **Security Group** de cada instância que recebe conexões. Instale a dependência em todas as máquinas:

```bash
pip install pyzmq
```

---

## 1. Client-Server (padrão REQ/REP)

### O que foi feito

O código original (`zmq_client-server.py`) rodava `server` e `client` como processos no mesmo arquivo usando `multiprocessing`, conectando via `localhost`. Foi separado em dois arquivos independentes que se comunicam via IP externo.

### Funcionalidades adicionadas

O servidor original apenas adicionava `*` ao final de qualquer mensagem recebida. Foi adicionado suporte a múltiplos comandos usando o protocolo `COMANDO:texto`:

| Comando | Descrição |
|---|---|
| `UPPER:texto` | Converte o texto para maiúsculas |
| `LOWER:texto` | Converte o texto para minúsculas |
| `REVERSE:texto` | Inverte a string |
| `COUNT:texto` | Conta palavras e caracteres |
| Sem `:` | Comportamento original preservado (adiciona `*`) |

O servidor também exibe um log com timestamp de cada requisição recebida e imprime estatísticas de uso ao encerrar.

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
...
=== Estatisticas ===
  DEFAULT: 1 requisicoes
  UPPER: 1 requisicoes
  LOWER: 1 requisicoes

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

O código original (`zmq_pub-sub.py`) rodava publisher e subscriber no mesmo arquivo via `multiprocessing`, publicando apenas um tópico (`TIME`) e conectando via `localhost`. Foi separado em dois arquivos que se comunicam via IP externo.

### Funcionalidades adicionadas

O publisher original publicava apenas o tópico `TIME` (hora atual). Foram adicionados dois novos tópicos publicados a cada ciclo:

| Tópico | Descrição |
|---|---|
| `TIME` | Hora atual do sistema (original preservado) |
| `TEMP` | Temperatura simulada em °C |
| `LOAD` | Carga de CPU simulada em % |

O subscriber passou a aceitar como argumento quais tópicos deseja assinar. Se nenhum for informado, assina todos.

### Como rodar

```bash
# Máquina A — inicie primeiro
python pub-sub/publisher.py

# Máquina B — assina todos os tópicos
python pub-sub/subscriber.py <IP_MAQUINA_A>

# Máquina B — assina apenas TIME e TEMP
python pub-sub/subscriber.py <IP_MAQUINA_A> TIME TEMP
```

### Exemplo de saída

```
# publisher (Máquina A)
[PUBLISHER] Porta 5678 | Topicos: TIME, TEMP, LOAD

# subscriber (Máquina B)
[SUBSCRIBER] Inscrito: TIME
[SUBSCRIBER] Inscrito: TEMP
[SUBSCRIBER] Inscrito: LOAD
TIME Sun May 31 10:33:00 2026
TEMP 37.4 C
LOAD 62.1 %
TIME Sun May 31 10:33:03 2026
...
```

---

## 3. Pipeline Producer → Middle → Consumer (padrão PUSH/PULL)

### O que foi feito

O código original tinha dois arquivos separados: `tasksrc.py` (producer) e `taskwork.py` (worker), ambos rodando na mesma máquina com IPs hardcoded em `constPipe.py`. O `constPipe.py` foi substituído pelo `config.py` centralizado.

O pipeline foi expandido para **3 estágios em 3 máquinas distintas**:

```
Máquina A          Máquina B               Máquina C
[producer] -5678→ [middle]        -5679→  [consumer]
  gera tarefas    consumer/producer        resultado final
```

### Funcionalidades adicionadas

O pipeline original tinha apenas producer → worker (2 estágios). Foi adicionado um estágio intermediário (`middle.py`) que funciona simultaneamente como consumer e producer, atendendo ao requisito `producer → consumer/producer → consumer`.

O `middle.py` recebe cada tarefa do producer, simula processamento (`time.sleep`), e encaminha para o consumer final identificando a origem como `middle-B`. O consumer final exibe estatísticas de workload a cada 10 tarefas recebidas.

A estrutura de dados entre os estágios é a mesma tupla `(origem, workload)` do código original.

### Como rodar

A ordem de inicialização importa: o middle e o consumer devem estar prontos antes de o producer começar a enviar.

```bash
# 1º — Máquina B (inicie primeiro)
python pipeline/middle.py <IP_MAQUINA_A>

# 2º — Máquina C
python pipeline/consumer.py <IP_MAQUINA_B>

# 3º — Máquina A (inicie por último)
python pipeline/producer.py
```

### Exemplo de saída

```
# producer (Máquina A)
[PRODUCER] Gerando tarefas na porta 5678 ...
[PRODUCER] Enviando workload 043
[PRODUCER] Enviando workload 017
...

# middle (Máquina B)
[MIDDLE] Conectado ao producer em <IP_A>:5678
[MIDDLE] Repassando na porta 5679
[MIDDLE] Recebeu 043 de producer-A
[MIDDLE] Repassou 043 para consumer-C
...

# consumer (Máquina C)
[CONSUMER] Conectado ao middle em <IP_B>:5679
[CONSUMER] Recebeu 043 de middle-B
[CONSUMER] Recebeu 017 de middle-B
...
  [stats] 10 tarefas processadas | media ultimas 10: 54.3
```
