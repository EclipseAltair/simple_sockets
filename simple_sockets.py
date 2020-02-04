'''
TCP - port
IP - ip-address
socket - IP+TCP - 127.0.0.1:8000
'''
import socket
from views import *


URLS = {
	'/': index,
	'/blog': blog
}


def parse_requset(request):
	parsed = request.split(' ')
	method = parsed[0]
	url = parsed[1]
	return (method, url) 


def generate_headers(method, url):
	if not method == 'GET':
		return ('HTTP/1.1 405 Method not allowed\n\n', 405)

	if not urls in URLS:
		return ('HTTP/1.1. 404 Not found\n\n', 404)

	return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(code, url):
	if code == 404:
		return '<h1>404</h1><p>Not found</p>'
	elif code == 405:
		return '<h1>405</h1><p>Method not allowed</p>'
	return URLS[url]()


def generate_response(request):
	method, url = parse_request(request)
	headers, code = generate_headers(method, url)
	body = generate_content(code, url)
	return (headers + body).encode()


def run():
	'''
	AF - Address Family
	AF_INET  - IPv4
	AF_INET6  - IPv6
	SOCK_STREAM - TCP
	SOL - SOcket Level
	SO_REUSEADDR - переиспользвование адреса
	'''
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# принимает запрос
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# переиспользует адрес (1 = True)
	server_socket.bind(('localhost', 5000))		# связывает, ждет данные по этим данным
	server_socket.listen()		# слуашет порт на наличие входящих пакетов

	while True:
		client_socket, addr = server_socket.accept()	# получает от клиента (кортеж)
		request = client_socket.recv(1024)		# получил, кол-во байт в пакете
		print(request)
		print()
		print(addr)

		response = generate_response(request.decode('utf-8'))

		client_socket.sendall(response)		# возвращает клиенту
		client_socket.close()

if __name__ == '__main__':
	run()