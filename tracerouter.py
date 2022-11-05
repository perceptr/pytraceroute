import socket as sock
import time

# (+) Поддержка IPv4.
# Работа через ICMP + указание SEQ.
# (+) Вывод таблицы трассировки с временем ответа.
# (+) Посылать N запросов (по умолчанию N=3).
# Задание интервала времени между запросами.
# (+) Задание таймаута ожидания.
# (+) Задание максимального TTL.
# (+) Задание размера пакета (по умолчанию 40).


class Tracerouter:
    def __init__(self, host: str, timeout: int = 2,
                 sequence_number: int = 30, packet_size: int = 40,
                 request_count: int = 3):
        self.host = host
        self.ttl = 1
        self.sequence_number = sequence_number
        self.timeout = timeout
        self.port = 33434
        self.pack_size = packet_size
        self.request_count = request_count

    def __get_host_name(self, send_socket: sock,
                        recv_socket: sock) -> (str, str):
        send_socket.sendto(b"", (self.host, self.port))
        curr_addr = None
        curr_name = None
        try:
            _, curr_addr = recv_socket.recvfrom(512)
            curr_addr = curr_addr[0]
            try:
                curr_name = sock.gethostbyaddr(curr_addr)[0]
            except sock.error:
                curr_name = curr_addr
        except sock.error as e:
            pass
        if curr_addr is not None:
            curr_host = f"{curr_name} ({curr_addr})"
        else:
            curr_host = "* * *"

        return curr_addr, curr_host

    def run(self):
        for ttl in range(1, self.sequence_number + 1):
            with sock.socket(sock.AF_INET, sock.SOCK_RAW, sock.getprotobyname("icmp")) as recv_socket:
                with sock.socket(sock.AF_INET, sock.SOCK_DGRAM, sock.getprotobyname("udp")) as send_socket:
                    self.ttl = ttl
                    recv_socket.settimeout(self.timeout)
                    send_socket.setsockopt(sock.SOL_IP, sock.IP_TTL, self.ttl)

                    delays = []
                    curr_addr, curr_host = None, None
                    for _ in range(self.request_count):
                        start = time.time()
                        curr_addr, curr_host = self.__get_host_name(send_socket, recv_socket)
                        if curr_host == "* * *":
                            break
                        delays.append((time.time() - start) * 1000)

                    print(f"{self.ttl}\t{curr_host} "
                          f"{' '.join([f'{round(delay, 3)} ms' for delay in delays])}")

                    if curr_addr == self.host:
                        break
