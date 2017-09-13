import socket
import sys
import select
import utils


class BasicClient(object):

    def __init__(self, name, address, port):
        self.address = address
        self.port = int(port)
        self.name = name
        self.socket = socket.socket()
        self.server_msg = ""
        try: 
            self.socket.connect((self.address, self.port))  # can't duplicate connect!
        except:
            print(utils.CLIENT_CANNOT_CONNECT.format(self.address, self.port))
            sys.exit()
        self.socket_lst = [self.socket, sys.stdin]
        self.socket.send(name.ljust(utils.MESSAGE_LENGTH))
        sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX); sys.stdout.flush()

    def start(self):
        while True:
            sockets_read, sockets_write, sockets_error = select.select(self.socket_lst, [], [], 0)
            for socket in sockets_read:
                # case 1: from stdin
                if socket is sys.stdin:
                    msg = sys.stdin.readline()
                    msg = msg.ljust(utils.MESSAGE_LENGTH)
                    self.socket.send(msg)
                    sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX); sys.stdout.flush()
                # case 2: from server socket
                else:
                    try:
                        self.server_msg += socket.recv(1024)
                        if len(self.server_msg) >= 200:
                            msg = self.server_msg.rstrip()
                            self.server_msg = ""
                            # msg from other clients 
                            if msg and msg[0] == '[':
                                name_index = 0
                                while msg[name_index] != ']':
                                    name_index += 1
                                currname = msg[:name_index + 1]
                                if currname[1:-1] != self.name:
                                    sys.stdout.write(utils.CLIENT_WIPE_ME + "\r" + msg + "\n") 
                                    sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX); sys.stdout.flush()
                            else: 
                                if msg:      # edge case: /list when no channels are present will send an empty msg
                                    sys.stdout.write(utils.CLIENT_WIPE_ME + "\r" + msg + "\n") 
                                    sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX); sys.stdout.flush()
                        elif not self.server_msg:
                            print(utils.CLIENT_WIPE_ME + "\r" + utils.CLIENT_SERVER_DISCONNECTED.format(self.address, self.port))
                            sys.exit()
                    except Exception as e:
                        print(e)
                        raise e


# handle command line input
args = sys.argv
if len(args) != 4:
    print "Please supply a server address and port."
    sys.exit()
client = BasicClient(args[1], args[2], args[3])
client.start()

