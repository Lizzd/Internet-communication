import socket


def send_tcp_message(client, message):
    try:
        message += '\0'
        message = message.encode('ascii')
        client.send(message)
    except socket.timeout:
        print('tcp_timeout')
    finally:
        print(f"===  ===")
        print(f"send_tcp_message: {message} to {client}")


def send_udp_message(socket, addr, message):
    try:
        message += '\0'
        message = message.encode('ascii')
        socket.sendto(message, addr)
    except socket.timeout:
        print('timeout')
    finally:
        print(f"===  ===")
        print(f"send_udp_message: {message} to {addr}")


def list_to_str(list):
    if type(list) == str:
        return list
    return ','.join(list)


def recv_decorator(message):
    print(f"===  ===")
    print(f"recv_decorator client: {message}")
    message = message.decode('ascii')
    if "\x00" in message:
        message = message[:-1]
    message = message.split(' ')
    return message


def recv_decorator_multi(messages):
    print(f"===  ===")
    print(f"recv_decorator client: {messages}")
    messages = messages.decode('ascii')
    if "\x00" in messages:
        messages = messages[:-1]
    messages = messages.split('\0')
    messages_list = [message.split(' ') for message in messages]
    return messages_list
