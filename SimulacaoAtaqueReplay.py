import time
import uuid
from datetime import datetime
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

# Função para gerar chaves RSA
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key

# Função para enviar a mensagem assinada e cifrada
def send_message(sender_private_key, receiver_public_key, message, nonce=None, timestamp=None):
    # Se houver nonce e timestamp, incluí-los na mensagem
    if nonce and timestamp:
        message = message + f"||{timestamp}||{nonce}".encode('utf-8')
    elif timestamp:
        message = message + f"||{timestamp}".encode('utf-8')
    
    # Criar hash da mensagem
    h = SHA256.new(message)
    # Assinar a mensagem
    signature = pkcs1_15.new(sender_private_key).sign(h)

    # Cifrar a mensagem com a chave pública do destinatário
    cipher_rsa = PKCS1_OAEP.new(receiver_public_key)
    encrypted_message = cipher_rsa.encrypt(message)

    print(f"Mensagem enviada (cifrada): {encrypted_message}")
    time.sleep(1)
    
    return encrypted_message, signature

# Função para receber e verificar a mensagem
def receive_message(sender_public_key, receiver_private_key, encrypted_message, signature, used_nonces, timestamp=None, nonce=None):
    # Decifrar a mensagem com a chave privada do destinatário
    cipher_rsa = PKCS1_OAEP.new(receiver_private_key)
    decrypted_message = cipher_rsa.decrypt(encrypted_message)

    # Se houver timestamp ou nonce, extrair da mensagem
    message_content = decrypted_message.split(b'||')
    message = message_content[0]
    
    if timestamp and len(message_content) > 1:
        received_timestamp = message_content[1].decode('utf-8')
        print(f"Timestamp recebido: {received_timestamp}")
        if abs((datetime.now() - datetime.fromisoformat(received_timestamp)).total_seconds()) > 5:
            print("Ataque de replay detectado! Timestamp inválido.")
            return
    if nonce and len(message_content) > 2:
        received_nonce = message_content[2].decode('utf-8')
        print(f"Nonce recebido: {received_nonce}")
        if received_nonce in used_nonces:
            print("Ataque de replay detectado! Nonce já foi utilizado.")
            return
        used_nonces.add(received_nonce)

    print(f"Mensagem recebida (decifrada): {message.decode('utf-8')}")
    time.sleep(1)

    # Verificar assinatura
    h = SHA256.new(decrypted_message)
    try:
        pkcs1_15.new(sender_public_key).verify(h, signature)
        print("Assinatura verificada com sucesso!")
        time.sleep(1)
    except (ValueError, TypeError):
        print("Assinatura inválida!")
        time.sleep(1)

# Função para simular um ataque de replay
def replay_attack(sender_public_key, receiver_private_key, encrypted_message, signature, used_nonces, timestamp=None, nonce=None):
    print("\n--- Tentativa de ataque de replay: Reenvio de mensagem interceptada ---")
    time.sleep(1)
    receive_message(sender_public_key, receiver_private_key, encrypted_message, signature, used_nonces, timestamp, nonce)

# Função principal
def main():
    # Gerar chaves para Alice e Bob
    print("Gerando chaves RSA para Alice e Bob...")
    alice_private_key, alice_public_key = generate_rsa_keys()
    bob_private_key, bob_public_key = generate_rsa_keys()
    time.sleep(1)

    print("Chaves geradas com sucesso!\n")

    # Inicializar conjunto de nonces usados por Bob para prevenir replay
    used_nonces = set()

    # Cenário 1: Mensagem assinada simples (sem timestamp ou nonce)
    print("--- Cenário 1: Enviando mensagem assinada simples (sem proteção contra replay) ---")
    message1 = "Olá Bob! Esta é Alice.".encode('utf-8')  # Encode para bytes
    encrypted_message1, signature1 = send_message(alice_private_key, bob_public_key, message1)

    # Bob recebe a mensagem sem proteção contra replay
    print("\n--- Bob recebe a mensagem sem proteção ---")
    receive_message(alice_public_key, bob_private_key, encrypted_message1, signature1, used_nonces)

    # Ataque de replay no cenário 1
    replay_attack(alice_public_key, bob_private_key, encrypted_message1, signature1, used_nonces)

    # Cenário 2: Mensagem com timestamp
    print("\n--- Cenário 2: Enviando mensagem com timestamp (proteção parcial contra replay) ---")
    timestamp2 = datetime.now().isoformat()  # Timestamp atual
    message2 = "Oi Bob, esta é Alice novamente.".encode('utf-8')
    encrypted_message2, signature2 = send_message(alice_private_key, bob_public_key, message2, timestamp=timestamp2)

    # Bob recebe a mensagem com timestamp
    print("\n--- Bob recebe a mensagem com timestamp ---")
    receive_message(alice_public_key, bob_private_key, encrypted_message2, signature2, used_nonces, timestamp=True)

    # Ataque de replay no cenário 2
    replay_attack(alice_public_key, bob_private_key, encrypted_message2, signature2, used_nonces, timestamp=True)

    # Cenário 3: Mensagem com nonce e timestamp
    print("\n--- Cenário 3: Enviando mensagem com nonce e timestamp (proteção completa contra replay) ---")
    nonce3 = uuid.uuid4().hex  # Gerar nonce único
    timestamp3 = datetime.now().isoformat()  # Timestamp atual
    message3 = "Oi Bob, esta é uma mensagem com nonce e timestamp.".encode('utf-8')
    encrypted_message3, signature3 = send_message(alice_private_key, bob_public_key, message3, nonce=nonce3, timestamp=timestamp3)

    # Bob recebe a mensagem com nonce e timestamp
    print("\n--- Bob recebe a mensagem com nonce e timestamp ---")
    receive_message(alice_public_key, bob_private_key, encrypted_message3, signature3, used_nonces, timestamp=True, nonce=True)

    # Ataque de replay no cenário 3
    replay_attack(alice_public_key, bob_private_key, encrypted_message3, signature3, used_nonces, timestamp=True, nonce=True)

if __name__ == "__main__":
    main()
