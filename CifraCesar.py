def cifra_cesar(texto, deslocamento, operacao):
    def shift_caracter(caracter, deslocamento):
        if caracter.isalpha():
            alfabeto = 'A' if caracter.isupper() else 'a'
            return chr((ord(caracter) - ord(alfabeto) + deslocamento) % 26 + ord(alfabeto))
        return caracter

    # Ajusta o deslocamento para a operação de decifrar
    if operacao == 'd':
        deslocamento = -deslocamento

    texto_resultado = ''.join(shift_caracter(c, deslocamento) for c in texto)
    return texto_resultado

# Entradas do usuário

texto = input()
deslocamento = int(input())
operacao = input()

# Processa a cifra de César
resultado = cifra_cesar(texto, deslocamento, operacao)
print(resultado)
