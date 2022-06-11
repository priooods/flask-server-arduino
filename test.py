import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('',8585))
s.listen(0)

while True:
    client,addr = s.accept()
    client.settimeout(5)
    print("oke running")
    while True:
        print(f"users connect = {addr}")
        content = client.recv(1024)
        if len(content) == 0:
            break
        if str(content,'utf-8') == '\r\n':
            continue
        else:
            print(str(content,'utf-8'))
            client.send(b'hello from server')
    client.close()