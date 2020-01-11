import socket, sys, select, socketserver, struct, time
import c_encrypt
import ssl

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass


class Socks5Server(socketserver.StreamRequestHandler):
    def handle_tcp(self,sock,remote):
        fdset = [sock,remote]
        while True:
            r, w, e = select.select(fdset, [], [],10)
            if sock in r:
                data=sock.recv(2048)
                if remote.send(c_encrypt.decrypt_message(data,c_encrypt.glo_de_table15)) <= 0:
                    break
            if remote in r:
                data=remote.recv(2048)
                if sock.send(c_encrypt.encrypt_message(data,c_encrypt.glo_en_table15)) <= 0:
                    break

    def handle(self):
        s=self.connection
        len1=struct.unpack('>i', c_encrypt.decrypt_message(s.recv(4),c_encrypt.glo_de_table15))[0]
        addr = c_encrypt.decrypt_message(s.recv(len1),c_encrypt.glo_de_table15).decode()
        print(addr)
        print(len(addr))
        len2 = struct.unpack('>i', c_encrypt.decrypt_message(s.recv(4),c_encrypt.glo_de_table15))[0]
        port=struct.unpack('>H',c_encrypt.decrypt_message(s.recv(len2),c_encrypt.glo_de_table15)[:2])[0]
        remote=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((addr,port))
        self.handle_tcp(s,remote)



def main():
    server = ThreadingTCPServer(('', 4569), Socks5Server)
    server.serve_forever()

if __name__ == '__main__':
    main()