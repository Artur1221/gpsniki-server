import socket
import time

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#s.bind(("", 6700))

#s.listen(100)

#sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#sc.bind(("", 8080))

#sc.listen(100)

count = 0

login_bytes = bytes([0x23, 0x41, 0x4c, 0x23, 0x31, 0x0d, 0x0a])

while True:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	s.bind(("", 6700))

	s.listen(100)
	conn, addr = s.accept()
	data = conn.recv(2**20)

	login_bytes = bytes([0x23, 0x41, 0x4c, 0x23, 0x31, 0x0d, 0x0a])

	conn.send(login_bytes)

	data = conn.recv(2**20)

	if data:
		#connc, addrc = sc.accept()

		#datac = connc.recv(2**20)

		print(count)

		print(bytes.fromhex(data.hex(" ")).decode('ascii'))
		print(data.hex(" "))

		with open('server_output.txt', 'a') as output:
			output.write(bytes.fromhex(data.hex(" ")).decode('ascii'))
		pkg_amt = len(bytes.fromhex(data.hex(" ")).decode('ascii').split('|')) - 1

		print(bytes([0x23, 0x41, 0x42, 0x23, 0x37, 0x0d, 0x0a]))

		conn.send(bytes([0x23, 0x41, 0x42, 0x23, 0x30 + pkg_amt, 0x0d, 0x0a]))

		#conn.sendall(data)

		count += 1
	else:
		print('No data')

	conn.close()
	s.close()

	sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	sc.bind(("", 8080))

	sc.listen(100)

	connc, addrc = sc.accept()

	#datac = connc.recv(2**20)

	#print(datac)

	connc.send(data)

	connc.close()



