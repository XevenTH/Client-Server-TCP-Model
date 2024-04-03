import pickle
import os

def DownloadClient(client):
    status = client.recv(1024).decode()
    print("status: " + status)

    if status == "EXIST":
        nama_file = client.recv(1024).decode()
        file_length_data = client.recv(4)
        file_length = int.from_bytes(file_length_data, byteorder='big')
        file_data = client.recv(file_length)

        with open(nama_file, 'wb') as f:
            f.write(file_data)

        print(f"File {nama_file} berhasil didownload.")
    else:
        print("File atau Folder tidak Ditemukan")

def UploadClient(client, command):
    word = command.split()
    nama_file = word[1]
    try:
        if os.path.exists(nama_file):
            client.sendall(b"EXIST")
            with open(nama_file, "rb") as f:
                file_data = f.read()
                file_length = len(file_data)
                client.sendall(file_length.to_bytes(4, byteorder='big'))
                client.sendall(file_data)
            print(f"File {nama_file} sent successfully.")
        else:
            client.sendall(b"NOTEXIST")
            print(f"Tidak ada Nama File/Folder Bernama {nama_file}")
    except Exception as e:
       print(str(e))

def ConmeClient(client, address, command):
    client.connect(address)
    client.sendall(command.encode())

    data = client.recv(4096)
    message_received = pickle.loads(data)

    print("Server Sudah Terhubung, silahkan bereksplorasi!!!")
    print('Balasan dari server: ', message_received)


def ByeClient(client, command):
    client.sendall(command.encode())
    print("\nMenutup koneksi...")
    print("gunakan conme untuk terhubung kembali...")
    client.close()

def OtherClient(client):
    data = client.recv(4096)
    if data:
        message_received = pickle.loads(data)
        print('Balasan dari server:\n\n', message_received)
    else:
        print("Tidak ada data dari server")