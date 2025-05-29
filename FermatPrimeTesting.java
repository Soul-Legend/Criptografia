import java.util.Scanner;

public class FermatPrimeTesting {

    // Função de MDC utilizando o algoritmo de Euclides
    public static int mdc(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            // Lê os valores de 'a' e 'p'
            System.out.print("Informe os valores de 'a' e 'p' para testar a primalidade de 'p': ");
            int a = scanner.nextInt();
            int p = scanner.nextInt();

            // Testa se são relativamente primos (MDC = 1)
            if (mdc(a, p) != 1) {
                System.out.println("Falha! a = " + a + " e p = " + p + " não são relativamente primos.");
            } else {
                System.out.println("Os números " + a + " e " + p + " são relativamente primos.");
            }
            System.out.println();

            // "a" elevado a "p-1" é calculado para verificar primalidade de "p" usando o pequeno teorema de Fermat
            double power = Math.pow(a, p - 1);
            double res = power % p;

            System.out.println("Cálculo de a^(p-1) mod p:");
            System.out.println(a + "^" + (p - 1) + " = " + power);
            System.out.println(power + " mod " + p + " = " + res);
            System.out.println();

            if (res == 1) {
                System.out.println(p + " é provavelmente primo.");
            } else {
                System.out.println(p + " não é primo.");
            }

            System.out.println();
        }
    }
}
