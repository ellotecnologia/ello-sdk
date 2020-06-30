# encoding: utf-8
""" Emulador de balança em rede
"""
import socket
import itertools

pesos = [0.750, 0.380, 0.485]
iterador_pesos = itertools.cycle(pesos)

HOST = '127.0.0.1'
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

def aguarda_conexao():
    while True:
        conn, addr = s.accept()
        print(addr, 'conectou')

        while True:
            try:
                data = conn.recv(1024)
            except socket.error:
                conn.close()
                break
            conn.send('{0}'.format(iterador_pesos.next()))
            conn.close()

        print('closing...')
        conn.close()

while True:
    try:
        aguarda_conexao()
    except socket.error:
        continue

# Ex. de configuracao do Ello.ini
# [Balanca]
# modelo=1
# porta=TCP:localhost:8000
# baud=9600
# intervalo=10
# arqlog= 
