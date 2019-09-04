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
Module defining a UDP echo server which uses 'select' instead of multithreading
for concurrent connections
'''
import select
import socket

_BIND_IP = ''  # Bind to all interfaces
_RECV_BUF_SIZE = 1024  # Max size of received data in bytes
_SELECT_TIMEOUT = 5.0  # Timeout (in sec.) for select to return control
done = False


def kill_server():
    global done
    done = True


def __mainloop(server, inputs, outputs):
    opt_value = 1  # Set the socket options

    # Dict of message queues for data to send {socket:(data,addr)}
    msg_queues = {}

    # Start mainloop
    while inputs and not done:
        # Multiplex with select
        readable, writable, exceptional = select.select(inputs,
                                                        outputs,
                                                        inputs,
                                                        _SELECT_TIMEOUT)

        # Socket has data to read
        for s in readable:
            if s is server:
                # Data is ready to be read from UDP server socket
                data, addr = s.recvfrom(_RECV_BUF_SIZE)
                print('Received: \'%s\' from: \'%s\'' % (data, addr[0]))

                # Create socket for sending data
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET,
                                socket.SO_REUSEADDR,
                                opt_value)

                # Add socket to output channel
                outputs.append(sock)

                # Add item to message queue
                msg_queues[sock] = (data, addr)

        # Socket has data to write
        for s in writable:
            send_data = msg_queues[s][0]  # Get data to send
            send_addr = msg_queues[s][1]  # Get addr to send data to
            print('Sending: \'%s\' to: \'%s\'' % (send_data, send_addr[0]))

            # Send data over socket
            s.sendto(send_data, send_addr)

            # Close socket
            try:
                outputs.remove(s)
            except ValueError:
                pass

            s.close()

            # Delete message queue
            del msg_queues[s]

        # Socket experienced exceptional condition
        for s in exceptional:
            # Remove socket from input/output channel
            try:
                inputs.remove(s)
            except ValueError:
                pass

            try:
                outputs.remove(s)
            except ValueError:
                pass

            # Close socket and delete message queue
            s.close()

            try:
                del msg_queues[s]
            except KeyError:
                pass


def start(port):
    server_addr = (_BIND_IP, port)  # Address to listen at
    opt_value = 1  # Set the socket options

    # Initialize server socket with appropriate options
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, opt_value)

    # Bind to listen to appropriate address
    server.bind(server_addr)

    # Lists containing sockets for 'select' to operate on
    inputs = [server]   # Sockets to read
    outputs = []        # Sockets to write

    __mainloop(server, inputs, outputs)

    print('\nServer Closed')
