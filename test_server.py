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
import signal
from time import sleep
import udp_select_server

_ACCESS_PORT = 10001
done = False


def sigint_handler(signum, stack_frame):
    global done

    if signum == signal.SIGINT:
        udp_select_server.kill_server()
        done = True


if __name__ == '__main__':
    # Setup Ctrl-C interrupt logic
    signal.signal(signal.SIGINT, sigint_handler)

    try:
        udp_select_server.start(_ACCESS_PORT)

        while not done:
            sleep(1.0)

    finally:
        # Restore original sigint handler
        signal.signal(signal.SIGINT, signal.default_int_handler)

    print('\nServer Closed')
