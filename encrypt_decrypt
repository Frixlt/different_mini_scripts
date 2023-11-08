import os
# код шифрования/дешифрования 
# Зашифровка и запись в файл
text = "ATTACK AT DAWN"
encrypted = encrypt(text)

with open('encrypted.txt', 'w') as f:
    f.write(encrypted)
    
print("Зашифрованный текст записан в файл encrypted.txt")

# Считывание из файла и расшифровка
with open('encrypted.txt', 'r') as f:
    encrypted = f.read()

decrypted = decrypt(encrypted)

with open('decrypted.txt', 'w') as f:
    f.write(decrypted)

print("Расшифрованный текст записан в файл decrypted.txt")
