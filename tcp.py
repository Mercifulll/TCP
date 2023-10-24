import socket
import threading

# Функція, яка обробляє вхідні повідомлення для клієнта
def client_receive(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Клієнт отримав: " + data.decode('utf-8'))
        except Exception as e:
            print(str(e))
            break

# Функція, яка обробляє вхідні повідомлення для сервера
def server_receive(server_socket):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print("З'єднано з " + str(client_address))
            client_handler = threading.Thread(target=client_receive, args=(client_socket,))
            client_handler.start()
        except Exception as e:
            print(str(e))

# Створення серверного сокету
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8888))
server.listen(5)
print("Сервер готовий до прийому з'єднань")

# Створення клієнтського сокету
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8888))

# Запуск функцій для обробки вхідних повідомлень
server_receive_thread = threading.Thread(target=server_receive, args=(server,))
server_receive_thread.start()

while True:
    message = input("Введіть повідомлення: ")
    client.send(message.encode('utf-8'))

server.close()
client.close()