from Cryptodome.Cipher import AES
import binascii

def print_diffusion_effect(plaintext1, plaintext2, key):
    """
    Função para demonstrar o efeito da difusão na criptografia. Esta função criptografa
    dois textos claros que diferem em apenas um bit e exibe a diferença nos textos cifrados.
    
    Args:
    plaintext1 (str): O primeiro texto claro.
    plaintext2 (str): O segundo texto claro, que difere de plaintext1 em apenas um bit.
    key (bytes): A chave de criptografia de 16 bytes (128 bits).
    """
    
    # Inicializa o objeto de cifra AES em modo ECB (Electronic Codebook)
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Criptografa os dois textos claros
    ciphertext1 = cipher.encrypt(plaintext1)
    ciphertext2 = cipher.encrypt(plaintext2)
    
    # Converte os textos cifrados para formato hexadecimal para visualização
    ciphertext1_hex = binascii.hexlify(ciphertext1).decode('utf-8')
    ciphertext2_hex = binascii.hexlify(ciphertext2).decode('utf-8')
    
    # Exibe os resultados
    print(f"Texto Claro 1: {binascii.hexlify(plaintext1).decode('utf-8')}")
    print(f"Texto Cifrado 1: {ciphertext1_hex}\n")
    
    print(f"Texto Claro 2: {binascii.hexlify(plaintext2).decode('utf-8')}")
    print(f"Texto Cifrado 2: {ciphertext2_hex}\n")
    
    # Calcula e exibe a quantidade de bits diferentes nos dois textos cifrados
    difference_bits = bin(int(ciphertext1_hex, 16) ^ int(ciphertext2_hex, 16)).count('1')
    print(f"Número de bits diferentes entre os textos cifrados: {difference_bits}\n")


def print_confusion_effect(plaintext, key1, key2):
    """
    Função para demonstrar o efeito da confusão na criptografia. Esta função criptografa
    o mesmo texto claro utilizando duas chaves que diferem em apenas um bit e exibe a 
    diferença nos textos cifrados.
    
    Args:
    plaintext (str): O texto claro a ser criptografado.
    key1 (bytes): A primeira chave de criptografia de 16 bytes (128 bits).
    key2 (bytes): A segunda chave de criptografia de 16 bytes (128 bits), que difere de key1 em apenas um bit.
    """
    
    # Inicializa os objetos de cifra AES em modo ECB
    cipher1 = AES.new(key1, AES.MODE_ECB)
    cipher2 = AES.new(key2, AES.MODE_ECB)
    
    # Criptografa o texto claro com as duas chaves
    ciphertext1 = cipher1.encrypt(plaintext)
    ciphertext2 = cipher2.encrypt(plaintext)
    
    # Converte os textos cifrados para formato hexadecimal para visualização
    ciphertext1_hex = binascii.hexlify(ciphertext1).decode('utf-8')
    ciphertext2_hex = binascii.hexlify(ciphertext2).decode('utf-8')
    
    # Exibe os resultados
    print(f"Chave 1: {binascii.hexlify(key1).decode('utf-8')}")
    print(f"Texto Cifrado com Chave 1: {ciphertext1_hex}\n")
    
    print(f"Chave 2: {binascii.hexlify(key2).decode('utf-8')}")
    print(f"Texto Cifrado com Chave 2: {ciphertext2_hex}\n")
    
    # Calcula e exibe a quantidade de bits diferentes nos dois textos cifrados
    difference_bits = bin(int(ciphertext1_hex, 16) ^ int(ciphertext2_hex, 16)).count('1')
    print(f"Número de bits diferentes entre os textos cifrados: {difference_bits}")

# Exemplo de chave de 128 bits (16 bytes)
key1 = b'This is a key123'

# Chave 2 que difere de key1 em apenas um bit
key2 = b'This is a key124'

# Exemplo de texto claro (deve ter 16 bytes para compatibilidade com AES-128)
plaintext1 = b'This is a test 1'

# Texto claro 2 que difere de plaintext1 em apenas um bit
plaintext2 = b'This is a test 2'

# Executa a função para demonstrar o efeito da difusão
print("Demonstração da Difusão:\n")
print_diffusion_effect(plaintext1, plaintext2, key1)

# Executa a função para demonstrar o efeito da confusão
print("\nDemonstração da Confusão:\n")
print_confusion_effect(plaintext1, key1, key2)
