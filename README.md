# 🖧 Projeto RPC Distribuído

**RPC (Remote Procedure Call)** é um protocolo que permite a execução de funções remotas como se fossem chamadas locais. Ele possibilita a comunicação entre diferentes processos em redes distribuídas, permitindo que um cliente invoque métodos de um servidor remoto sem precisar lidar diretamente com os detalhes de rede.

No contexto deste projeto, foi implementado um sistema RPC distribuído, onde diferentes servidores podem executar funções e um servidor de nomes atua como intermediário para localizar os serviços disponíveis.

## 🌐 Arquitetura do Projeto

O projeto é dividido entre servidores, onde cada servidor pode ser executado em uma porta e IP diferente. Há também um **servidor de nomes**, que age como um intermediário, registrando os serviços disponíveis e encaminhando as chamadas para os servidores corretos.

### Componentes principais:
- **Servidores RPC**: Responsáveis por fornecer serviços remotos. Cada servidor pode rodar em um IP e porta diferentes.
- **Servidor de Nomes**: Mantém um registro dos servidores e seus respectivos serviços, permitindo que os clientes descubram onde cada serviço está localizado.
- **Cliente**: Envia requisições para o servidor de nomes para localizar um serviço e depois faz chamadas para os servidores correspondentes.

## 📌 Como funciona o projeto?

Este projeto implementa um sistema **RPC (Remote Procedure Call)** distribuído, no qual um cliente pode chamar funções remotamente como se fossem locais. O sistema é composto por três principais componentes:

- **Servidor de Nomes (Name Server)**
- **Servidores RPC (RPC Servers)**
- **Cliente RPC (RPC Client)**
  
Cada um desses componentes desempenha um papel fundamental na comunicação distribuída.

### **🖥️ 1. Servidor de Nomes (Name Server)**

O servidor de nomes funciona como um intermediário entre o cliente e os servidores RPC. Sua principal função é manter um registro dos serviços disponíveis e informar ao cliente onde encontrar um determinado serviço.
  - Cada **servidor RPC** registra suas operações no servidor de nomes, informando o IP e porta em que estão rodando.
  - O **cliente RPC** consulta o servidor de nomes para descobrir onde um determinado serviço está disponível.
  - Isso permite que os serviços possam ser distribuídos entre múltiplos servidores, tornando o sistema mais flexível e escalável.
  
### **🔌 2. Servidores RPC (RPC Servers)**
  
Os servidores RPC são responsáveis por expor funções que podem ser chamadas remotamente. Cada servidor pode rodar em um IP e porta diferente, permitindo distribuir a carga entre vários servidores.

  - Estes servidores são registrados no servidor de nomes, com suas operações.
  - O servidor RPC escuta requisições na porta e IP onde foi configurado e responde às chamadas do cliente.
  - Cada servidor RPC gera um **arquivo de log** para registrar todas as operações realizadas.
  
### **📡 3. Cliente RPC (RPC Client)**
  
O cliente RPC é responsável por fazer chamadas para os serviços remotos. Ele segue os seguintes passos:

  1. Consulta o Servidor de Nomes para encontrar o IP e a porta do serviço desejado.
  2. Se conecta ao Servidor RPC correspondente.
  3. Envia a requisição RPC com os parâmetros necessários.
  4. Recebe a resposta do servidor RPC e finaliza a chamada.
     
Esse processo permite que o cliente chame funções remotas sem precisar saber a localização exata do serviço, tornando o sistema dinâmico e flexível.

## 📝 Registro de Logs

Cada servidor RPC gera um arquivo de log contendo informações detalhadas sobre todas as requisições recebidas. Esse log inclui:

- **Data e horário** da requisição
- **Endereço IP** do cliente que fez a chamada
- **Nome da operação executada**
- **Tempo de execução** da requisição (em milissegundos)
  
Os logs seguem o formato:

```
AAAA-MM-DD HH:MM:SS, IP_CLIENTE, OPERAÇÃO, TEMPO_EXECUÇÃO ms
```

Exemplo de log gerado:

```
2025-02-03 11:54:16, 127.0.0.1, SUB, 0.365155 ms
```

Esses registros permitem monitorar o histórico de requisições, ajudando na depuração e otimização do sistema.

### 📂 Extração de IPs únicos

Até mesmo existe um **script shell** de exemplo para extrair os IPs únicos  que fizeram requisições ao servidor, do arquivo de log gerado, está na pasta abaixo:

```
log/shellScript.ch
```

## 🔒 Configuração de SSL

Para adicionar segurança às comunicações RPC, utilizamos **SSL/TLS** para criptografar os dados. Para isso, precisamos gerar um certificado e uma chave privada:

### Atualizar o arquivo `openssl.cnf`
Antes de gerar as chaves de acesso, é necessário configurar o arquivo `openssl.cnf` com as informações adequadas, na pasta `certs/`

### Gerar as chaves de acesso
Execute os seguintes comandos:

```sh
# Gera uma chave privada
openssl genpkey -algorithm RSA -out certs/server.key

# Gera um certificado autoassinado
openssl req -new -x509 -key certs/server.key -out certs/server.crt -days 365 -config certs/openssl.cnf
```

Exemplo de preenchimento durante a geração do certificado:
```
Country Name (2 letter code) [AU]: BR
State or Province Name (full name) [Some-State]: Minas Gerais
Locality Name (eg, city) []: Barbacena
Organization Name (eg, company) [Internet Widgits Pty Ltd]: RPC
Organizational Unit Name (eg, section) []: TI
Common Name (eg, server FQDN or YOUR name) []: localhost
Email Address []: 
```

As chaves geradas serão armazenadas nos seguintes caminhos:
```
PATH_SERVER_CERTS = "certs/server.crt"
PATH_SERVER_KEY = "certs/server.key"
```

## 🎯 Conclusão

Este projeto demonstra o funcionamento de um sistema RPC distribuído com múltiplos servidores e um intermediário para gerenciar as chamadas. A adição de SSL garante uma comunicação segura entre os componentes. Além disso, os arquivos de log permitem um monitoramento eficiente das operações realizadas pelos servidores RPC.

