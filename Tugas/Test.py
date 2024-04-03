kalimat = "Ini adalah sebuah contoh kalimat untuk demonstrasi."

kata_kata = kalimat.split()

if len(kata_kata) >= 2:
    kata_kedua = kata_kata[1]
    print(kata_kedua)
else:
    print("Kalimat tidak memiliki kata kedua.")
