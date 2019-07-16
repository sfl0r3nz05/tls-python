# tls-python
tls-python contains some examples of client-server based on TLS

How to use the examples:
1. Clone the repository
2. python client/server host:port certificates_dir
   e.g.: python3 server02_tlslite_handshake.py localhost:443 ./tests
3. Comment, client01../server01... have included the dir, so the command it will be:
   e.g.: python3 server01_ssl.py localhost:443