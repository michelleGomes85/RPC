
"""

# Gera uma chave privada
openssl genpkey -algorithm RSA -out certs/server.key

# Gera um certificado autoassinado
openssl req -new -x509 -key certs/server.key -out certs/server.crt -days 365 -config certs/openssl.cnf

-------------------------------------------------

Exemplo de preenchimento:

Country Name (2 letter code) [AU]: BR
State or Province Name (full name) [Some-State]: Minas Gerais
Locality Name (eg, city) []: Barbacena
Organization Name (eg, company) [Internet Widgits Pty Ltd]: RPC
Organizational Unit Name (eg, section) []: TI
Common Name (eg, server FQDN or YOUR name) []: localhost
Email Address []: 

"""

PATH_SERVER_CERTS = "certs/server.crt"
PATH_SERVER_KEY = "certs/server.key"