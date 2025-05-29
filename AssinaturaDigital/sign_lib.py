from Cryptodome.PublicKey import RSA as CryptoRSA
from Cryptodome.Signature import pkcs1_15, DSS
from Cryptodome.Hash import SHA256
from base64 import b64encode, b64decode

# Classe RSA para operações de criptografia e assinatura digital com RSA
class RSA:
    def __init__(self, key_size: int = 2048, public_exponent: int = 65537):
        """
        Inicializa a classe RSA gerando um par de chaves RSA com o tamanho e o expoente público especificados.

        :param key_size: Tamanho da chave RSA em bits (padrão 2048).
        :param public_exponent: Expoente público para a chave RSA (padrão 65537).
        """
        self.private_key: CryptoRSA.RsaKey
        self.public_key: CryptoRSA.RsaKey
        self.generate_keys(key_size, public_exponent)

    def generate_keys(self, key_size: int, public_exponent: int):
        """
        Gera um par de chaves RSA e armazena a chave privada e pública na instância.

        :param key_size: Tamanho da chave RSA em bits.
        :param public_exponent: Expoente público da chave RSA.
        """
        key: CryptoRSA.RsaKey = CryptoRSA.generate(key_size, e=public_exponent)
        self.private_key = key
        self.public_key = key.publickey()

    def sign_message(self, message: str) -> str:
        """
        Assina digitalmente uma mensagem usando a chave privada RSA.

        :param message: A mensagem em texto simples a ser assinada.
        :return: Assinatura da mensagem codificada em base64.
        """
        message_hash = SHA256.new(message.encode())
        signature = pkcs1_15.new(self.private_key).sign(message_hash)
        return b64encode(signature).decode()

    def verify_signature(self, message: str, signature: str, public_key: CryptoRSA.RsaKey) -> bool:
        """
        Verifica uma assinatura RSA de uma mensagem usando a chave pública RSA.

        :param message: A mensagem original em texto simples.
        :param signature: A assinatura codificada em base64 a ser verificada.
        :param public_key: A chave pública RSA do remetente.
        :return: True se a assinatura for válida, False caso contrário.
        """
        message_hash = SHA256.new(message.encode())
        try:
            pkcs1_15.new(public_key).verify(message_hash, b64decode(signature))
            return True
        except (ValueError, TypeError):
            return False
