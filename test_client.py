'''
Testing module
'''
import socket

_ACCESS_PORT = 10001
_NUM_SOCKETS = 5
_RECV_BUF_SIZE = 1024


if __name__ == '__main__':
    send_addr = ('localhost', _ACCESS_PORT)
    msgs = ['this is a', 'multipart message']
    sockets = []
    opt_value = 1

    # Create sockets
    for i in range(_NUM_SOCKETS):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET,
                        socket.SO_REUSEADDR,
                        opt_value)

        sockets.append(sock)

    # Send and receive echoes
    for msg in msgs:

        for s in sockets:
            s.sendto(msg.encode(), send_addr)
            print('%s sent \'%s\'' % (str(s.getsockname()), msg))

        for s in sockets:
            data, addr = s.recvfrom(_RECV_BUF_SIZE)
            print('%s received \'%s\'' % (str(s.getsockname()), data.decode()))

    # Close sockets
    for s in sockets:
        s.close()
