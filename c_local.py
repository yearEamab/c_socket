import socket, sys, select, socketserver, struct, time,c_encrypt


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass


class Socks5Server(socketserver.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [],10)
            if sock in r:
                data=sock.recv(2048)
                if remote.send(c_encrypt.encrypt_message(data,c_encrypt.glo_en_table15)) <= 0:
                    break
            if remote in r:
                data=remote.recv(2048)
                if sock.send(c_encrypt.decrypt_message(data,c_encrypt.glo_de_table15)) <= 0:
                    break





    def handle(self):
        try:
            addr_remote='207.148.90.10'
            #addr_remote = '127.0.0.1'
            port_remote=4569
            print('socks connection from ', self.client_address)
            sock = self.connection
            # 1. Version
            sock.recv(262)
            sock.send(b"\x05\x00")
            # 2. Request
            data = self.rfile.read(4)
            mode = data[1]
            addrtype = data[3]
            if addrtype == 1:  # IPv4
                addr = socket.inet_ntoa(self.rfile.read(4))
            elif addrtype == 3:  # Domain name
                addr = self.rfile.read(int.from_bytes(self.rfile.read(1), byteorder='big', signed=False))
            #     #addr='www.baidu.com'
            port = struct.unpack('>H', self.rfile.read(2))
            #port=[80,]
            reply = b"\x05\x00\x00\x01"
            try:
                if mode == 1:  # 1. Tcp connect
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote.connect((addr_remote, port_remote))
                    # remote.send(struct.pack('>H',len(addr)))
                    # remote.send(addr)
                    # remote.send(struct.pack('>H',port[0]))
                    en_addr=addr
                    en_port=struct.pack('>H',port[0])
                    addr_len=len(en_addr)
                    port_len=len(en_port)
                    remote.send(c_encrypt.encrypt_message(struct.pack('>i',addr_len),c_encrypt.glo_en_table15))
                    remote.send(c_encrypt.encrypt_message(en_addr,c_encrypt.glo_en_table15))
                    remote.send(c_encrypt.encrypt_message(struct.pack('>i',port_len),c_encrypt.glo_en_table15))
                    remote.send(c_encrypt.encrypt_message(en_port,c_encrypt.glo_en_table15))
                    print('Tcp connect to', addr_remote,port_remote)
                else:
                    reply = b"\x05\x07\x00\x01"  # Command not supported
                local = remote.getsockname()
                reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
            except socket.error:
                # Connection refused
                reply = b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
            sock.send(reply)
            # 3. Transfering
            if reply[1] == 0:  # Success
                if mode == 1:  # 1. Tcp connect
                    self.handle_tcp(sock, remote)
        except socket.error:
            print('socket error')


def main():
    server = ThreadingTCPServer(('127.0.0.1', 1081), Socks5Server)
    server.serve_forever()


if __name__ == '__main__':
    main()