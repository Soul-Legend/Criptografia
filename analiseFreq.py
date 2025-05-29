# Dicionário de substituição de caracteres acentuados
# Este dicionário mapeia caracteres acentuados para seus equivalentes sem acento,
# o que ajuda a normalizar o texto para análise posterior.
substituicoes = {
    'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a', 'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
    'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
    'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ç': 'c'
}

def normalizar_texto(texto):
    """
    Normaliza o texto substituindo caracteres acentuados por suas versões sem acento.
    Também preserva a capitalização original dos caracteres.
    """
    texto_normalizado = ""
    for char in texto:
        # Verifica se o caractere é acentuado, e substitui conforme o dicionário
        if char.lower() in substituicoes:
            if char.isupper():
                texto_normalizado += substituicoes[char.lower()].upper()
            else:
                texto_normalizado += substituicoes[char.lower()]
        else:
            texto_normalizado += char
    return texto_normalizado

# Frequências típicas das letras na língua portuguesa
# Estes valores são usados como referência para calcular o Chi-Quadrado
frequencias_portugues = {
    'a': 14.63,
    'b': 1.04,
    'c': 3.88,
    'd': 4.99,
    'e': 12.57,
    'f': 1.02,
    'g': 1.30,
    'h': 1.28,
    'i': 6.18,
    'j': 0.40,
    'k': 0.02,
    'l': 2.78,
    'm': 4.74,
    'n': 5.05,
    'o': 10.73,
    'p': 2.52,
    'q': 1.20,
    'r': 6.53,
    's': 7.81,
    't': 4.34,
    'u': 4.63,
    'v': 1.67,
    'w': 0.01,
    'x': 0.21,
    'y': 0.01,
    'z': 0.47
}

def calcular_frequencias(texto):
    """
    Calcula a frequência de cada letra no texto.
    O resultado é expresso em porcentagem do total de letras no texto.
    """
    frequencias = {}
    total_letras = 0
    for char in texto.lower():
        if char.isalpha():
            total_letras += 1
            if char in frequencias:
                frequencias[char] += 1
            else:
                frequencias[char] = 1
    # Converte as contagens absolutas em porcentagens
    for char in frequencias:
        frequencias[char] = (frequencias[char] / total_letras) * 100
    return frequencias

def calcular_chi_quadrado(frequencias_texto, deslocamento):
    """
    Calcula o valor do Chi-Quadrado para um determinado deslocamento no alfabeto.
    O Chi-Quadrado mede a diferença entre as frequências de letras no texto e 
    as frequências esperadas na língua portuguesa, considerando um deslocamento
    aplicado ao texto cifrado.
    """
    chi_quadrado = 0.0
    for char, freq in frequencias_portugues.items():
        # Calcula o caractere após aplicar o deslocamento no alfabeto
        char_deslocado = chr(((ord(char) - ord('a') + deslocamento) % 26) + ord('a'))
        # Obtém a frequência do caractere deslocado no texto, ou assume 0 se não estiver presente
        freq_texto = frequencias_texto.get(char_deslocado, 0)
        # Soma a contribuição do caractere ao valor total de Chi-Quadrado
        # A fórmula é: (observado - esperado)² / esperado
        chi_quadrado += ((freq_texto - freq) ** 2) / freq
    return chi_quadrado

def decifrar_cesar(texto_cifrado):
    """
    Decifra um texto cifrado usando a cifra de César, identificando o melhor deslocamento
    através da minimização do Chi-Quadrado.
    """
    # Normaliza o texto cifrado para remover acentos e unificar o formato das letras
    texto_normalizado = normalizar_texto(texto_cifrado)
    
    # Calcula as frequências de letras no texto cifrado normalizado
    frequencias_texto = calcular_frequencias(texto_normalizado)

    # Inicializa variáveis para encontrar o melhor deslocamento
    melhor_deslocamento = 0
    menor_chi_quadrado = float('inf')
    
    # Testa todos os deslocamentos possíveis (0 a 25)
    for deslocamento in range(26):
        chi_quadrado = calcular_chi_quadrado(frequencias_texto, deslocamento)
        # Atualiza o melhor deslocamento se o valor do Chi-Quadrado for menor
        if chi_quadrado < menor_chi_quadrado:
            menor_chi_quadrado = chi_quadrado
            melhor_deslocamento = deslocamento

    # Decifra o texto usando o deslocamento identificado
    texto_decifrado = ''
    for char in texto_normalizado:
        if char.isalpha():
            # Calcula o caractere decifrado aplicando o deslocamento inverso
            if char.islower():
                texto_decifrado += chr(((ord(char) - ord('a') - melhor_deslocamento) % 26) + ord('a'))
            else:
                texto_decifrado += chr(((ord(char) - ord('A') - melhor_deslocamento) % 26) + ord('A'))
        else:
            texto_decifrado += char

    return texto_decifrado, melhor_deslocamento

# Recebe o texto cifrado como entrada do usuário
texto_cifrado = input()
# Decifra o texto e obtém o deslocamento utilizado na cifra
texto_decifrado, deslocamento = decifrar_cesar(texto_cifrado)

# Exibe o deslocamento encontrado e o texto decifrado
print(deslocamento)
print(texto_decifrado)
