import subprocess
import os


def perintah_ls():
    try:
        result = subprocess.run(['ls'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return str(e)


def perintah_rm(nama_file):
    try:
        if os.path.exists(nama_file):
            os.remove(nama_file)
            return f"File {nama_file} berhasil dihapus."
        else:
            return f"File {nama_file} tidak ditemukan."
    except Exception as e:
        return str(e)


def perintah_download(connection, nama_file):
    try:
        if os.path.exists(nama_file):
            connection.sendall(b"EXIST")
            with open(nama_file, "rb") as f:
                file_data = f.read()
                file_length = len(file_data)
                connection.sendall(f"Downloaded-{nama_file}".encode())
                connection.sendall(file_length.to_bytes(4, byteorder='big'))
                connection.sendall(file_data)
            print(f"File {nama_file} Telah Dikirimkan.")
        else:
            connection.sendall(b"NOTEXIST")
            print(f"File atau direktori {nama_file} tidak ditemukan.")
    except Exception as e:
        print(str(e))


def perintah_upload(connection, nama_file):
    status = connection.recv(1024).decode()
    print("status: " + status)

    if status == "EXIST":
        try:
            file_length = int.from_bytes(connection.recv(4), byteorder='big')
            file_data = connection.recv(file_length)

            with open(f"Uploaded-{nama_file}", 'wb') as f:
                f.write(file_data)
                
            print(f"File {nama_file} Telah Diterima.")
        except Exception as e:
            print(f"gagal mengupload: {str(e)}")
    else:
        print("Error Saat Mengupload File (Lihat Error di client)")

def perintah_size(nama_file):
    try:
        if os.path.exists(nama_file):
            ukuran_byte = os.path.getsize(nama_file)
            ukuran_mb = ukuran_byte / (1024 * 1024)
            return f"Ukuran file {nama_file}: {ukuran_mb:.2f} MB"
        else:
            return f"File {nama_file} tidak ditemukan."
    except Exception as e:
        return str(e)