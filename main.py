from tracerouter import Tracerouter
import sys


def main(args: list) -> None:
    help_output = '''
    Usage: python3 main.py <host> [options]
    Options:
        -h, --help: show this help
        -H, --host: host to trace
        -t, --timeout: timeout for each request
        -s, --sequence-number: number of requests
        -p, --packet-size: size of packet
        -r, --request-count: number of requests
        -d, --debug: debug mode
        -n, --need-domains: need domains
        -i, --interval: interval between requests
        -P, --port: port
        -T, --protocol: protocol (tcp or udp)
        -m, --message: custom message
    
    Example: python3 main.py google.com -t=2 -s=30 -p=40 -r=3 -d=1 
             -n=1 -i=0 -P=443 -T=udp -m=hello_world
    '''

    arguments = {
        "host": '',
        'H': '',
        "timeout": 2,
        't': 2,
        "sequence_number": 30,
        's': 30,
        "packet_size": 40,
        'p': 40,
        "request_count": 3,
        'r': 3,
        "is_need_domains": False,
        'n': False,
        "interval": 0,
        'i': 0,
        "debug": False,
        'd': False,
        "port": 443,
        'P': 443,
        "protocol": 'udp',
        'T': 'udp',
        "custom_message": None,
        'm': None
    }

    if '-h' in args or '--help' in args:
        print(help_output)
        return

    for arg in args:
        if arg.startswith('--'):
            if '=' in arg:
                key, value = arg[2:].split('=')
                if key in arguments:
                    if key in ['is_need_domains', 'debug']:
                        arguments[key] = bool(int(value))
                    elif key in ['host', 'custom_message', 'protocol']:
                        arguments[key] = value
                    else:
                        arguments[key] = int(value)
                else:
                    print(f'Unknown argument: {key}')
                    return
        elif arg.startswith('-'):
            if '=' in arg:
                key, value = arg[1:].split('=')
                if key in arguments:
                    if key in ['n', 'd']:
                        arguments[key] = bool(int(value))
                    elif key in ['H', 'm', 'T']:
                        arguments[key] = value
                    else:
                        arguments[key] = int(value)
                else:
                    print(f'Unknown argument: {key}')
                    return

    if not arguments['host']:
        print('Host is required')
        return

    tr = Tracerouter(**arguments)
    tr.run()


if __name__ == "__main__":
    main(sys.argv)