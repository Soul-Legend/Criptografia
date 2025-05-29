import hashlib
import random

def gerar_hash(array):
    # Converte o array de inteiros para uma string
    array_str = ''.join(map(str, array))

    # Inicializa o objeto hashlib com SHA-256
    hash_object = hashlib.sha256(array_str.encode())
    hash_hex = hash_object.hexdigest()

    return hash_hex

def fornecedor():
    # Gera um array de 5 posições com valores aleatórios
    array_pacotes = [random.randint(0, 99) for _ in range(5)]

    # Gera o hash original do array
    hash_original = gerar_hash(array_pacotes)

    # Imprime o array original e o hash gerado
    print("Array original:", array_pacotes)
    print("Hash de segurança:", hash_original)

    return array_pacotes, hash_original

def receptor(array_recebido, hash_original):
    # Gera o hash do array recebido
    novo_hash = gerar_hash(array_recebido)

    # Imprime o array recebido e o novo hash gerado
    print("Array recebido:", array_recebido)
    print("Hash do array recebido:", novo_hash)

    # Verifica se o novo hash é igual ao hash original
    if novo_hash == hash_original:
        print("Recebimento bem-sucedido: o hash é igual ao original.")
    else:
        print("Falha no recebimento: o hash é diferente do original.")

r = 1

while r:
    array, hash = fornecedor()
    
    # Aplica uma probabilidade de 50% de chance de remover o último elemento
    remove_ultimo = random.choice([True, False])
    if remove_ultimo:
        array_modificado = array[:-1]  # Remove o último elemento
    else:
        array_modificado = array  # Mantém o array original
    
    # Verifica a integridade do array modificado ou original
    receptor(array_modificado, hash)
    
    print()
    r = input("Digite 1 para novo teste: ")
    print()
