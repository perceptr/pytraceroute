from tracerouter import Tracerouter
import sys


def main(args: list) -> None:
    help_output = '''
    Usage: python3 main.py <host> [options]
    Options:
        --help: show this help
        --timeout <timeout>: set timeout for each request
        --sequence-number <sequence_number>: set sequence number
        --packet_size <packet_size>: set packet size
        --request_count <request_count>: set request count
        --is_need_domains: show domains
        --interval <interval>: set interval between requests
        --debug: show debug info
        --port <port>: set port
        --protocol <protocol>: set protocol
        --custom_message <custom_message>: set custom message
        
    
    Example: 
        python3 main.py google.com --timeout=2 --sequence-number=30 
        --packet_size=40 --request_count=3 --is_need_domains=1 --interval=0 
        --debug=1 --port=443 --protocol=udp --custom_message=hello_world! 
    '''

    arguments = {
        "host": '',
        "timeout": 2,
        "sequence_number": 30,
        "packet_size": 40,
        "request_count": 3,
        "is_need_domains": False,
        "interval": 0,
        "debug": False,
        "port": 443,
        "protocol": 'udp',
        "custom_message": None,
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