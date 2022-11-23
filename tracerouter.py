import socket as sock
import logging
import time


# (+) Поддержка IPv4.
# (+) Работа через ICMP
# (+) Вывод таблицы трассировки с временем ответа.
# (+) Посылать N запросов (по умолчанию N=3).
# (+) Задание интервала времени между запросами.
#           (между 1 и 2 запросом, между 2 и 3 запросом и т.д.)
# (+) Задание таймаута ожидания.
# (+) Задание максимального TTL.
# (+) Задание размера пакета (по умолчанию 40).

# (+) Работа через TCP SYN + указание порта.
# (+) Указание промежуточных IP.
# (+) Разрешать хопы в DNS-имя: (по умолчанию - нет).
# (+) debug-режим. Режим сокетов: выводить логи
# (?) Задание source address:
# ( ) Задание payload пакета.


class Tracerouter:
    def __init__(self, host: str, timeout: int = 2,
                 sequence_number: int = 30, packet_size: int = 40,
                 request_count: int = 3, is_need_domains=False,
                 interval=0, debug=False, port=443, protocol='udp',
                 custom_message=None):
        self.host = host
        self.sequence_number = sequence_number
        self.timeout = timeout
        self.port = port
        self.pack_size = packet_size
        self.request_count = request_count
        self.protocol = protocol
        self.is_need_domains = is_need_domains
        self.interval = interval
        self.debug = debug
        self.custom_message = custom_message

        if protocol not in ['udp', 'tcp']:
            raise Exception(f'Unknown protocol: {protocol}')

    def __print_log(self, message: str) -> None:
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug(message)

    def __get_host_name(self, send_socket, recv_socket, connect_func) -> str:
        connect_func(send_socket)
        self.__print_log('Trying to get host name')
        try:
            _, curr_addr = recv_socket.recvfrom(512)
            if self.is_need_domains:
                try:
                    curr_name = sock.gethostbyaddr(curr_addr[0])[0]
                    self.__print_log(f'Got host name: {curr_name}')
                    return curr_name
                except sock.error:
                    self.__print_log(f'Can\'t get host name')
                    return '* * *'
        except sock.timeout:
            self.__print_log('Timeout')
            return '* * *'

    def __send_recv_packet(self, send_socket: sock, recv_socket: sock,
                           connect_func: sock.create_connection) -> str:
        self.__print_log(f'Send packet to {self.host}')
        connect_func(send_socket)
        curr_addr = '* * *'
        try:
            _, curr_addr = recv_socket.recvfrom(512)
            self.__print_log(f'Recv packet from {curr_addr}')
            curr_addr = curr_addr[0]
        except sock.timeout as e:
            self.__print_log(f'Timeout on recv packet')
            pass

        return curr_addr

    def __ping(self, ttl: int, send_socket: sock, recv_socket: sock,
               connect_func: sock.create_connection) -> (str, str):
        recv_socket.settimeout(self.timeout)
        send_socket.setsockopt(sock.SOL_IP, sock.IP_TTL, ttl)

        delays = []
        curr_addr = None
        for _ in range(self.request_count):
            start = time.time()

            curr_addr_tmp = self.__send_recv_packet(send_socket,
                                                    recv_socket,
                                                    connect_func)
            if curr_addr_tmp != '* * *':
                curr_addr = curr_addr_tmp
                delay = str(round((time.time() - start) * 1000, 3))
                delays.append(delay)
                self.__print_log(f'Get delay {delay} ms')
            else:
                self.__print_log(f'delay is None')
                delays.append("*")
        return curr_addr, delays

    def __run_with_protocol(self, send_socket_tuple: tuple,
                            connect_func: sock.create_connection):
        number = 0
        found_addr = set()
        with sock.socket(*send_socket_tuple) as send_socket:
            with sock.socket(sock.AF_INET, sock.SOCK_RAW,
                             sock.getprotobyname("icmp")) as recv_socket:
                for ttl in range(1, self.sequence_number + 1):
                    self.__print_log(
                        f'Send packet to {self.host} with ttl {ttl}')

                    curr_addr, delays = self.__ping(
                        ttl, send_socket, recv_socket, connect_func)

                    if curr_addr in found_addr and curr_addr is not None:
                        continue

                    number += 1

                    if curr_addr is None:
                        print(f"{number}\t* * *")
                    else:
                        domain = ''
                        if self.is_need_domains:
                            domain = self.__get_host_name(send_socket, recv_socket, connect_func)

                        print(f"{number}\t{curr_addr} {domain} | "
                              f"{' '.join([f'{delay} ms' for delay in delays])}")

                    if curr_addr == self.host:
                        break

                    time.sleep(self.interval)

    def run(self):
        if self.protocol == 'udp':
            self.__print_log('Run with udp protocol')
            send_socket_tuple = sock.AF_INET, sock.SOCK_DGRAM, sock.getprotobyname("udp")
            connect_func = lambda send_socket: send_socket.sendto(
                b"0" * self.pack_size if self.custom_message is None
                else self.custom_message.encode(),
                (self.host, self.port)
            )
        elif self.protocol == 'tcp':
            self.__print_log('Run with tcp protocol')
            send_socket_tuple = sock.AF_INET, sock.SOCK_STREAM
            connect_func = lambda send_socket: send_socket.connect((self.host, self.port))
        else:
            raise Exception('Wrong protocol')

        self.__run_with_protocol(send_socket_tuple, connect_func)
