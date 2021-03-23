import socket
import argparse
import threading 
import time
import os

parser = argparse.ArgumentParser(description = "Multithread so o básico")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = 'localhost')
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 8080)
args = parser.parse_args()

print(f"Server rodando {args.host} na porta {args.port}")

socketPrincipal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketPrincipal.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try: 
	socketPrincipal.bind((args.host, args.port))
	socketPrincipal.listen(5)
except Exception as e:
	raise SystemExit(f"Não é possivel escutar: {args.host} na porta: {args.port}, por esse: {e}")


def clienteNovo(cliente, connection):
	ip = connection[0]
	port = connection[1]
	s = cliente.recv(5000)
	print(f"Conexao feita pelo: {ip} e porta: {port}")
	fileName=str(s)
	count=fileName.find("html")
	count+=4
	print(f"nome do arquivo {fileName[7:count]}")
	if(os.path.exists(fileName[7:count])):
		print(f"existe o arquivo {fileName[7:count]}")
		openFileName = open(fileName[7:count], 'r')
		kar = openFileName.read()
		openFileName="\r\nHTTP/1.1 200 OK\r\n"
		openFileName+="Server: ServidorPython"
		openFileName+="Content-Type: text/html\r\n"
		openFileName+="\r\n"
		openFileName+=kar
		cliente.sendall(openFileName.encode())
		print("html enviado")
	else:
		fileName = 't404.html'
		openFileName = open(fileName, 'r')
		kar = openFileName.read()
		openFileName="\r\nHTTP/1.1 404 OK\r\n"
		openFileName+="Server: ServidorPython"
		openFileName+="Content-Type: text/html\r\n"
		openFileName+="\r\n"
		openFileName+=kar
		cliente.sendall(openFileName.encode())
		print("html enviado")
	cliente.shutdown(0)

	


while True:
	try: 
		cliente, ip = socketPrincipal.accept()
		thread = threading.Thread(target=clienteNovo,args=(cliente, ip))
		thread.start()
	except KeyboardInterrupt:
		print(f"Server interrompido")      
	except Exception as e:
		print(f"Erro: {e}")
