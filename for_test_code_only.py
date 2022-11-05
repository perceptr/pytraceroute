from tracerouter import Tracerouter

if __name__ == "__main__":
    tr = Tracerouter("habrahabr.ru", timeout=2, sequence_number=30, packet_size=40, request_count=3)
    tr.run()
