from Cryptodome.PublicKey import DSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import pad, unpad
import base64

class Alice:
    def __init__(self, p, g):
        print("Alice: Gerando seu número privado (secreto)...")
        self.private_key = DSA.generate(2048).x  # Gerando número privado (secreto)
        print(f"Alice: Número privado gerado: {self.private_key}")
        self.p = p
        self.g = g
        print(f"Alice: Usando os parâmetros públicos p (primo grande) e g (gerador):\np = {p}\ng = {g}")
        
        # Calculando a chave pública de Alice: g^a mod p
        self.public_key = pow(self.g, self.private_key, self.p)
        print(f"Alice: Chave pública gerada (g^a mod p): {self.public_key}")
        self.shared_key = None  # A chave compartilhada ainda não foi gerada

    def generate_shared_key(self, bob_public_key):
        # Gerando a chave compartilhada K = Bob_public^a mod p
        print(f"Alice: Recebendo a chave pública de Bob: {bob_public_key}")
        print("Alice: Gerando a chave compartilhada (K = Bob_public^a mod p)...")
        self.shared_key = pow(bob_public_key, self.private_key, self.p)
        print(f"Alice: Chave compartilhada gerada: {self.shared_key} (Essa chave será usada para criptografia)")

    def encrypt_message(self, message):
        print("Alice: Criptografando mensagem para Bob usando a chave compartilhada...")
        # Deriva uma chave AES a partir da chave compartilhada usando scrypt
        key = scrypt(str(self.shared_key).encode(), b'salt', 32, N=2**14, r=8, p=1)
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv  # Vetor de inicialização
        ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode('utf-8')  # Codifica para facilitar a transmissão

    def decrypt_message(self, encrypted_message):
        print("Alice: Descriptografando mensagem de Bob usando a chave compartilhada...")
        # Deriva a chave AES novamente para descriptografar
        key = scrypt(str(self.shared_key).encode(), b'salt', 32, N=2**14, r=8, p=1)
        encrypted_message = base64.b64decode(encrypted_message)
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
        return plaintext


class Bob:
    def __init__(self, p, g):
        print("Bob: Gerando seu número privado (secreto)...")
        self.private_key = DSA.generate(2048).x  # Gerando número privado (secreto)
        print(f"Bob: Número privado gerado: {self.private_key}")
        self.p = p
        self.g = g
        print(f"Bob: Usando os parâmetros públicos p (primo grande) e g (gerador):\np = {p}\ng = {g}")
        
        # Calculando a chave pública de Bob: g^b mod p
        self.public_key = pow(self.g, self.private_key, self.p)
        print(f"Bob: Chave pública gerada (g^b mod p): {self.public_key}")
        self.shared_key = None  # A chave compartilhada ainda não foi gerada

    def generate_shared_key(self, alice_public_key):
        # Gerando a chave compartilhada K = Alice_public^b mod p
        print(f"Bob: Recebendo a chave pública de Alice: {alice_public_key}")
        print("Bob: Gerando a chave compartilhada (K = Alice_public^b mod p)...")
        self.shared_key = pow(alice_public_key, self.private_key, self.p)
        print(f"Bob: Chave compartilhada gerada: {self.shared_key} (Essa chave será usada para criptografia)")

    def encrypt_message(self, message):
        print("Bob: Criptografando mensagem para Alice usando a chave compartilhada...")
        # Deriva uma chave AES a partir da chave compartilhada usando scrypt
        key = scrypt(str(self.shared_key).encode(), b'salt', 32, N=2**14, r=8, p=1)
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv  # Vetor de inicialização
        ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode('utf-8')  # Codifica para facilitar a transmissão

    def decrypt_message(self, encrypted_message):
        print("Bob: Descriptografando mensagem de Alice usando a chave compartilhada...")
        # Deriva a chave AES novamente para descriptografar
        key = scrypt(str(self.shared_key).encode(), b'salt', 32, N=2**14, r=8, p=1)
        encrypted_message = base64.b64decode(encrypted_message)
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
        return plaintext


# Parâmetros públicos do protocolo Diffie-Hellman (p é um número primo grande e g é um gerador)
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E08
g = 2

# Instanciando Alice e Bob, com os parâmetros públicos p e g
alice = Alice(p, g)
bob = Bob(p, g)

# Troca de chaves públicas entre Alice e Bob
print("\n--- Troca de chaves públicas ---")
print("Alice envia sua chave pública para Bob.")
alice.generate_shared_key(bob.public_key)
print("Bob envia sua chave pública para Alice.")
bob.generate_shared_key(alice.public_key)

# Alice envia uma mensagem para Bob
print("\n--- Alice envia uma mensagem criptografada para Bob ---")
mensagem_alice = "Olá Bob, aqui é Alice!"
mensagem_encriptada_para_bob = alice.encrypt_message(mensagem_alice)
print(f"Alice (mensagem encriptada): {mensagem_encriptada_para_bob}")
mensagem_recebida_por_bob = bob.decrypt_message(mensagem_encriptada_para_bob)
print(f"Bob (mensagem recebida): {mensagem_recebida_por_bob}")

# Bob envia uma mensagem para Alice
print("\n--- Bob envia uma mensagem criptografada para Alice ---")
mensagem_bob = "Olá Alice, recebi sua mensagem!"
mensagem_encriptada_para_alice = bob.encrypt_message(mensagem_bob)
print(f"Bob (mensagem encriptada): {mensagem_encriptada_para_alice}")
mensagem_recebida_por_alice = alice.decrypt_message(mensagem_encriptada_para_alice)
print(f"Alice (mensagem recebida): {mensagem_recebida_por_alice}")
