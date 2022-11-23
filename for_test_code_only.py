# !/usr/bin/env python
# -*- coding: utf-8 -*-
from tracerouter import Tracerouter
import socket

if __name__ == "__main__":
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #     print('conneting to google.com')
    #     sock.connect(('google.com', 443))
    #     print('connected')
    #     sock.send(b'hello, world!')
    #     print('wait')
    #     data = sock.recv(1024)
    #     print(data)

    tr = Tracerouter("google.com", timeout=2, sequence_number=30, packet_size=40, request_count=3, debug=False, is_need_domains=True)
    tr.run()
