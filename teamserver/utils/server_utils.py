import os
import socket
from datetime import datetime


def send_tcp_message(client, message, logger=None):
    try:
        message += '\0'
        message = message.encode('ascii')
        client.send(message)
    except socket.timeout:
        print('tcp_timeout')
    finally:
        if logger is not None:
            logger.info(f"===  ===")
            logger.info(f"send_tcp_message: {message} ===================>>>>>> to {client}")
        print(f"===  ===")
        print(f"send_tcp_message: {message} ===================>>>>>> to {client}")


def send_udp_message(socket, addr, message, logger=None):
    try:
        message += '\0'
        message = message.encode('ascii')
        socket.sendto(message, addr)
    except socket.timeout:
        print('timeout')
    finally:
        if logger is not None:
            logger.info(f"===  ===")
            logger.info(f"send_tcp_message: {message} ===================>>>>>> to {addr}")
        print(f"===  ===")
        print(f"send_udp_message: {message} ===================>>>>>> to {addr}")


def list_to_str(list, delimiter=','):
    list = [str(element) for element in list]
    return delimiter.join(list)


def recv_decorator(message, thread_nr, seq_nr, logger=None):
    if logger is not None:
        logger.info(f"=== thread nr: {thread_nr}, seq_nr: {seq_nr} ===")
        logger.info(f"recv_decorator server: {message}")

    print(f"=== thread nr: {thread_nr}, seq_nr: {seq_nr} ===")
    print(f"recv_decorator server: {message}")
    message = message.decode('ascii')
    if "\0" in message:
        message = message[:-1]
    return message.split(' ')


def recv_decorator_gameserver(message, logger=None):
    if logger is not None:
        logger.info(f"===  ===")
        logger.info(f"recv_decorator gameserver: {message}")

    print(f"===  ===")
    print(f"recv_decorator gameserver: {message}")
    messages = message.decode('ascii')
    if "\0" in messages:
        messages = messages[:-1]
    messages = messages.split('\0')
    messages_list = [message.split(' ') for message in messages]
    return messages_list


def get_log_file_name():
    log_dir_path = 'log_file'
    os.makedirs(log_dir_path, exist_ok=True)
    return os.path.join(log_dir_path, datetime.now().strftime("%d_%m_%Y_%H%M%S")) + '.log'
