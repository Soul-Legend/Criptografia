import sign_lib

# 1. Bob instancia a biblioteca de assinaturas e gera um par de chaves (privada e pública)
print("Bob: Gerando chave privada")
bob = sign_lib.RSA()
print("Bob: Chave privada gerada")
print("Bob: Enviando chave pública para Alice")

# 2. Bob escreve uma mensagem para a Alice
bob_message = "Olá, Alice! Esta é uma mensagem importante."
print("\nBob: Enviando a mensagem:", bob_message)

# 3. Bob assina a mensagem, que consiste em gerar o hash da mensagem e encriptar usando sua chave privada
bob_signature = bob.sign_message(bob_message)
print("Bob: Assinatura digital da mensagem gerada")

# 4. Bob envia a mensagem e a assinatura para Alice
print("\nBob envia a mensagem e a assinatura para Alice")

# ---- A partir daqui, Alice recebe a mensagem e a assinatura de Bob ----

# 5. Alice recebe a chave pública de Bob, a mensagem e a assinatura
print("\nAlice: Recebendo a mensagem e a assinatura de Bob")
print("Alice: Recebendo a chave pública de Bob")

# 6. Alice calcula o hash da mensagem e usa a chave pública de Bob para verificar a assinatura (verifica se o hash que ela gerou e o que ela descriptou de bob são iguais)
alice = sign_lib.RSA()
signature_verification = alice.verify_signature(bob_message, bob_signature, bob.public_key)
if signature_verification:
    print("Alice: A assinatura é válida. A mensagem é autêntica e não foi alterada.")
else:
    print("Alice: A assinatura não é válida. A mensagem pode ter sido alterada ou não é autêntica.")

# ---- Seção para verificação com mensagem modificada ----
print("\n------------\n")

# 7. Mensagem original é alterada, mas a assinatura não é atualizada
bob_message_modified = "Olá, Alice! Esta é uma mensagem modificada."
print("Bob (após enviar): Mensagem original alterada:", bob_message_modified)

# 8. Alice tenta verificar com a mesma assinatura
signature_verification = alice.verify_signature(bob_message_modified, bob_signature, bob.public_key)
if signature_verification:
    print("Alice: A assinatura é válida. A mensagem é autêntica e não foi alterada.")
else:
    print("Alice: A assinatura NÃO é válida para a mensagem modificada. A integridade foi comprometida.")
