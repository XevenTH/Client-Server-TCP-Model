import socket
import pickle

from ServerUtils import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)
server.bind(server_address)

server.listen(1)

print('Menunggu koneksi...')
while True:
    connection, client_address = server.accept()
    print('Terhubung dengan', client_address)

    try:
        while True:
            print('\nMenunggu pesan dari client...')
            data = connection.recv(4096)

            if not data:
                print("Koneksi ditutup oleh klien.")
                break

            print('Menerima pesan dari client: ', data.decode())

            if data.decode() == "ls":
                message = "Daftar File dan Folder:\n" + perintah_ls()
            elif data.decode() == "byebye":
                print("Koneksi ditutup oleh klien.")
                break
            elif "rm" in data.decode():
                word = data.decode().split()

                if len(word) >= 2:
                    message = perintah_rm(word[1])
                else:
                    message = "Masukan nama File!!!"
            elif "download" in data.decode():
                command = data.decode().split()

                if len(command) >= 2:
                    nama_file = command[1]
                    perintah_download(connection, nama_file)
                    continue
                else:
                    message = "Masukan nama File untuk didownload!!!"
            elif "upload" in data.decode():
                command = data.decode().split()

                if len(command) >= 2:
                    nama_file = command[1]
                    perintah_upload(connection, nama_file)
                    continue
                else:
                    message = "Masukkan nama File untuk di upload!!!"
            elif "size" in data.decode():
                word = data.decode().split()

                if len(word) >= 2:
                    message = perintah_size(word[1])
                    message_pickle = pickle.dumps(message)
                    connection.sendall(message_pickle)
                    continue
                else:
                    message = "Masukkan nama File untuk melihat size File!!!"
            elif data.decode() == "conme":
                message = "Halloo, Selamat Datang di Server Kami"
            else:
                message = "Perintah tidak valid."

            message_pickle = pickle.dumps(message)
            connection.sendall(message_pickle)
    except ConnectionResetError:
        print("Koneksi ditutup oleh client")
    finally:
        connection.close()
