# MIT License
#
# Copyright (c) 2019 Weston Berg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
