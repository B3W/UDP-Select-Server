'''
Testing module
'''
import signal
import udp_select_server

_ACCESS_PORT = 10001


def sigint_handler(signum, stack_frame):
    if signum == signal.SIGINT:
        udp_select_server.kill_server()


if __name__ == '__main__':
    # Setup Ctrl-C interrupt logic
    signal.signal(signal.SIGINT, sigint_handler)

    try:
        udp_select_server.start(_ACCESS_PORT)
    finally:
        # Restore original sigint handler
        signal.signal(signal.SIGINT, signal.default_int_handler)
