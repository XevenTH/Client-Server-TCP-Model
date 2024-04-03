import socket

from ClientUtils import *

server_address = ('localhost', 12345)

AlreadyConnect = False

while True:
    print("\n1. ls")
    print("2. rm {namafile}")
    print("3. download {namafile}")
    print("4. upload {namafile}")
    print("5. size {namafile}")
    print("6. byebye")
    print("7. connme")

    command = input('\nMasukkan pesan: ')

    if command.startswith("conme") and not AlreadyConnect:
        AlreadyConnect = True
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ConmeClient(client, server_address, command)
        continue
    elif command.startswith("conme") and AlreadyConnect:
        print("Jangan pakai command ini lagi")
        continue
    elif AlreadyConnect:
        client.sendall(command.encode())

        if command.startswith("download"):
            DownloadClient(client)
        elif command.startswith("upload"):
            UploadClient(client, command)
        elif command.startswith("byebye"):
            ByeClient(client, command)
            AlreadyConnect = False
        else:
            OtherClient(client)
    else:
        print("Silahkan melakukan conme command sebelum yang lain")
