from Cryptodome.Cipher import AES
import binascii

class AESCipher:
    def __init__(self, key_size=128, mode='ECB'):
        self.key_size = key_size // 8
        self.mode = mode.upper()

    def get_cipher(self, key, iv=None):
        if self.mode == 'ECB':
            return AES.new(key, AES.MODE_ECB)
        elif self.mode == 'CBC':
            return AES.new(key, AES.MODE_CBC, iv)
        elif self.mode == 'CFB':
            return AES.new(key, AES.MODE_CFB, iv)
        elif self.mode == 'OFB':
            return AES.new(key, AES.MODE_OFB, iv)
        elif self.mode == 'CTR':
            return AES.new(key, AES.MODE_CTR, nonce=b'\x00' * 8)
        else:
            raise ValueError("Modo de operacao nao suportado.")

    def encrypt(self, plaintext, key):
        # IV zerado, exceto para ECB
        iv = b'\x00' * 16 if self.mode != 'ECB' else None
        cipher = self.get_cipher(key, iv)

        if self.mode in ['ECB', 'CBC']:
            from Cryptodome.Util.Padding import pad
            padded_text = pad(plaintext.encode(), AES.block_size)
            ciphertext = cipher.encrypt(padded_text)
        else:
            ciphertext = cipher.encrypt(plaintext.encode())
        return binascii.hexlify(ciphertext).decode()

    def decrypt(self, ciphertext, key):
        # IV zerado para CBC e outros modos que usam IV
        iv = b'\x00' * 16 if self.mode != 'ECB' else None
        cipher = self.get_cipher(key, iv)

        decoded_ciphertext = binascii.unhexlify(ciphertext)

        if self.mode in ['ECB', 'CBC']:
            from Cryptodome.Util.Padding import unpad
            decrypted_data = cipher.decrypt(decoded_ciphertext)
            return unpad(decrypted_data, AES.block_size).decode()
        else:
            return cipher.decrypt(decoded_ciphertext).decode()

def main():
    mode = input("Escolha o modo de operacao (ECB, CBC, CFB, OFB, CTR): ").strip().upper()
    key_size = int(input("Escolha o tamanho da chave (128, 192, 256): "))
    operation = input("Escolha o tipo de operacao (E para cifrar, D para decifrar): ").strip().upper()
    text = input("Digite o texto para cifrar ou decifrar: ")

    keys = {
        128: bytes.fromhex('637572736F63727970746F6772616679'),
        192: bytes.fromhex('637572736F63727970746F6772616679637572736F637279'),
        256: bytes.fromhex('637572736F63727970746F6772616679637572736F63727970746F6772616679')
    }

    # Cria o cifrador AES com a chave correspondente e recupera a chave
    aes_cipher = AESCipher(key_size=key_size, mode=mode)
    key = keys.get(key_size)

    if not key:
        print("Tamanho de chave invalido. Escolha 128, 192 ou 256.")
        return

    if operation == 'E':
        ciphertext = aes_cipher.encrypt(text, key)
        print(f"Texto cifrado (Hex): {ciphertext}")
    elif operation == 'D':
        try:
            decrypted_text = aes_cipher.decrypt(text, key)
            print(f"Texto decifrado: {decrypted_text}")
        except ValueError as e:
            print(f"Erro ao decifrar o texto: {e}")
    else:
        print("Operacao invalida. Por favor, escolha 'E' para cifrar ou 'D' para decifrar.")

if __name__ == "__main__":
    main()
