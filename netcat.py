import os
import subprocess
import locale
import shlex
import argparse
import sys
import textwrap
import threading
import socket

def execure(cmd):
    cmd = cmd.split()

    if not cmd:
        return
    
    if os.name == "nt":
        shell = True
    else:
        shell = False

    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, shell=shell)

    if locale.getdefaultlocale() == ('ja_JP', 'cp932'):
        return output.decode('cp932')
    else:
        return output.decode()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='BHP Net Tool',
        epilog=textwrap.dedent(
            '''
            Example:
                netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
                netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload file
                netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
                echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
                netcat.py -t 192.168.1.108 -p 5555 # connect to server
            '''
        )
    )

    parser.add_argument('-c', '--command' action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192/168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')

    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()

class NetCat:
    