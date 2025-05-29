import java.util.Scanner;

public class VigenereCipher {

    // Função para cifrar ou decifrar o texto usando o Cifrador de Vigenère
    public static String vigenereCipher(String text, String key, char operation) {
        text = text.toUpperCase();
        key = key.toUpperCase();
        StringBuilder result = new StringBuilder();
        int keyLength = key.length();

        for (int i = 0; i < text.length(); i++) {
            char textChar = text.charAt(i);
            char keyChar = key.charAt(i % keyLength);

            if (operation == 'c') {
                // Cifrar o texto
                result.append(encryptChar(textChar, keyChar));
            } else if (operation == 'd') {
                // Decifrar o texto
                result.append(decryptChar(textChar, keyChar));
            }
        }
        return result.toString();
    }

    // Função para cifrar um caractere
    private static char encryptChar(char textChar, char keyChar) {
        int textVal = textChar - 'A';
        int keyVal = keyChar - 'A';
        return (char) ((textVal + keyVal) % 26 + 'A');
    }

    // Função para decifrar um caractere
    private static char decryptChar(char textChar, char keyChar) {
        int textVal = textChar - 'A';
        int keyVal = keyChar - 'A';
        return (char) ((textVal - keyVal + 26) % 26 + 'A');
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Digite o texto (apenas letras):");
        String text = scanner.nextLine();

        System.out.println("Digite a palavra-chave:");
        String key = scanner.nextLine();

        // Solicitar a operação
        System.out.println("Digite 'c' para cifrar ou 'd' para decifrar:");
        char operation = scanner.next().charAt(0);

        // Realizar a operação de cifragem ou decifragem
        String result = vigenereCipher(text, key, operation);

        if (operation == 'c') {
            System.out.println("Texto Cifrado: " + result);
        } else if (operation == 'd') {
            System.out.println("Texto Decifrado: " + result);
        } else {
            System.out.println("Operação inválida.");
        }

        scanner.close();
    }
}
