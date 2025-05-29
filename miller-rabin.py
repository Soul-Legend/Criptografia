import random

def miller_rabin(n, a):
    m = n - 1
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1
    
    x = pow(a, m, n)
    if x == 1 or x == n - 1:
        return True
    
    for _ in range(k - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    
    return False

def miller_rabin_test(n):
    if n < 2:
        return "composto"
    
    resultados = []
    for a in range(2, 6):
        if a >= n:
            continue
        
        resultado = miller_rabin(n, a)
        if resultado:
            resultados.append(f"Teste a={a} -> provavelmente primo")
        else:
            resultados.append(f"Teste a={a} -> composto")
    
    if all("provavelmente primo" in res for res in resultados):
        resultado_final = f"Resultado final: {n} é provavelmente primo"
    else:
        resultado_final = f"Resultado final: {n} é composto"
    
    print("\n".join(resultados))
    print()
    print(resultado_final)

if __name__ == "__main__":
    n = int(input("Digite um numero inteiro: "))
    miller_rabin_test(n)
