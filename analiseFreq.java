import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class analiseFreq {

    // Dicionário de substituição de caracteres acentuados
    // Este mapa associa caracteres acentuados a seus equivalentes sem acento.
    // Isso é útil para normalizar o texto antes de qualquer análise ou decifração.
    private static final Map<Character, Character> substituicoes = new HashMap<>();
    
    static {
        // Mapeamento dos caracteres acentuados para seus equivalentes sem acento.
        substituicoes.put('á', 'a'); substituicoes.put('à', 'a'); substituicoes.put('ã', 'a');
        substituicoes.put('â', 'a'); substituicoes.put('ä', 'a'); substituicoes.put('é', 'e');
        substituicoes.put('è', 'e'); substituicoes.put('ê', 'e'); substituicoes.put('ë', 'e');
        substituicoes.put('í', 'i'); substituicoes.put('ì', 'i'); substituicoes.put('î', 'i');
        substituicoes.put('ï', 'i'); substituicoes.put('ó', 'o'); substituicoes.put('ò', 'o');
        substituicoes.put('õ', 'o'); substituicoes.put('ô', 'o'); substituicoes.put('ö', 'o');
        substituicoes.put('ú', 'u'); substituicoes.put('ù', 'u'); substituicoes.put('û', 'u');
        substituicoes.put('ü', 'u'); substituicoes.put('ç', 'c');
    }

    // Frequências típicas das letras na língua portuguesa
    // Este mapa armazena as frequências esperadas de cada letra em textos em português.
    // Esses valores são usados para calcular o valor de Chi-Quadrado e determinar o melhor deslocamento.
    private static final Map<Character, Double> frequenciasPortugues = new HashMap<>();
    
    static {
        // As frequências foram obtidas a partir de análises estatísticas da língua portuguesa.
        frequenciasPortugues.put('a', 14.63); frequenciasPortugues.put('b', 1.04);
        frequenciasPortugues.put('c', 3.88); frequenciasPortugues.put('d', 4.99);
        frequenciasPortugues.put('e', 12.57); frequenciasPortugues.put('f', 1.02);
        frequenciasPortugues.put('g', 1.30); frequenciasPortugues.put('h', 1.28);
        frequenciasPortugues.put('i', 6.18); frequenciasPortugues.put('j', 0.40);
        frequenciasPortugues.put('k', 0.02); frequenciasPortugues.put('l', 2.78);
        frequenciasPortugues.put('m', 4.74); frequenciasPortugues.put('n', 5.05);
        frequenciasPortugues.put('o', 10.73); frequenciasPortugues.put('p', 2.52);
        frequenciasPortugues.put('q', 1.20); frequenciasPortugues.put('r', 6.53);
        frequenciasPortugues.put('s', 7.81); frequenciasPortugues.put('t', 4.34);
        frequenciasPortugues.put('u', 4.63); frequenciasPortugues.put('v', 1.67);
        frequenciasPortugues.put('w', 0.01); frequenciasPortugues.put('x', 0.21);
        frequenciasPortugues.put('y', 0.01); frequenciasPortugues.put('z', 0.47);
    }

    /**
     * Normaliza o texto substituindo caracteres acentuados por suas versões sem acento.
     * A função também preserva a capitalização original dos caracteres.
     *
     * @param texto O texto a ser normalizado.
     * @return O texto normalizado.
     */
    public static String normalizarTexto(String texto) {
        StringBuilder textoNormalizado = new StringBuilder();

        // Percorre cada caractere do texto original.
        for (char c : texto.toCharArray()) {
            // Converte o caractere para minúsculo para facilitar a busca no mapa de substituições.
            char lowerC = Character.toLowerCase(c);
            
            // Verifica se o caractere está no mapa de substituições.
            if (substituicoes.containsKey(lowerC)) {
                // Se o caractere original era maiúsculo, converte a substituição para maiúsculo.
                if (Character.isUpperCase(c)) {
                    textoNormalizado.append(Character.toUpperCase(substituicoes.get(lowerC)));
                } else {
                    // Caso contrário, usa a versão minúscula do substituto.
                    textoNormalizado.append(substituicoes.get(lowerC));
                }
            } else {
                // Se o caractere não precisa ser substituído, simplesmente o adiciona ao texto normalizado.
                textoNormalizado.append(c);
            }
        }

        return textoNormalizado.toString();
    }

    /**
     * Calcula a frequência de cada letra no texto fornecido.
     * A frequência é expressa como uma porcentagem do total de letras no texto.
     *
     * @param texto O texto cuja frequência de letras será calculada.
     * @return Um mapa com as frequências das letras no texto.
     */
    public static Map<Character, Double> calcularFrequencias(String texto) {
        Map<Character, Double> frequencias = new HashMap<>();
        int totalLetras = 0;

        // Percorre cada caractere do texto normalizado.
        for (char c : texto.toLowerCase().toCharArray()) {
            // Verifica se o caractere é uma letra (ignorando espaços, pontuação, etc.).
            if (Character.isLetter(c)) {
                totalLetras++;
                // Incrementa a contagem da letra no mapa de frequências.
                frequencias.put(c, frequencias.getOrDefault(c, 0.0) + 1);
            }
        }

        // Converte as contagens absolutas de cada letra em porcentagens.
        for (char c : frequencias.keySet()) {
            frequencias.put(c, (frequencias.get(c) / totalLetras) * 100);
        }

        return frequencias;
    }

    /**
     * Calcula o valor do Chi-Quadrado para um determinado deslocamento no alfabeto.
     * Este valor mede a diferença entre as frequências de letras no texto e as frequências esperadas
     * na língua portuguesa. Quanto menor o valor, mais provável que o texto esteja decifrado corretamente.
     *
     * @param frequenciasTexto Mapa com as frequências das letras no texto cifrado.
     * @param deslocamento O deslocamento aplicado ao alfabeto para este cálculo.
     * @return O valor do Chi-Quadrado.
     */
    public static double calcularChiQuadrado(Map<Character, Double> frequenciasTexto, int deslocamento) {
        double chiQuadrado = 0.0;

        // Percorre cada entrada do mapa de frequências da língua portuguesa.
        for (Map.Entry<Character, Double> entry : frequenciasPortugues.entrySet()) {
            // Calcula o caractere após aplicar o deslocamento no alfabeto.
            char charDeslocado = (char) (((entry.getKey() - 'a' + deslocamento) % 26) + 'a');
            // Obtém a frequência do caractere deslocado no texto, ou assume 0 se não estiver presente.
            double freqTexto = frequenciasTexto.getOrDefault(charDeslocado, 0.0);

            // Aplica a fórmula do Chi-Quadrado: (observado - esperado)² / esperado.
            chiQuadrado += Math.pow(freqTexto - entry.getValue(), 2) / entry.getValue();
        }

        return chiQuadrado;
    }

    /**
     * Decifra um texto cifrado usando a cifra de César, identificando o melhor deslocamento
     * através da minimização do Chi-Quadrado.
     *
     * @param textoCifrado O texto cifrado que será decifrado.
     * @return Um array de strings, onde o primeiro elemento é o texto decifrado e o segundo é o deslocamento usado.
     */
    public static String[] decifrarCesar(String textoCifrado) {
        // Normaliza o texto cifrado para remover acentos e unificar o formato das letras.
        String textoNormalizado = normalizarTexto(textoCifrado);
        // Calcula as frequências de letras no texto cifrado normalizado.
        Map<Character, Double> frequenciasTexto = calcularFrequencias(textoNormalizado);

        int melhorDeslocamento = 0;
        double menorChiQuadrado = Double.POSITIVE_INFINITY;

        // Testa todos os deslocamentos possíveis (de 0 a 25).
        for (int deslocamento = 0; deslocamento < 26; deslocamento++) {
            // Calcula o valor do Chi-Quadrado para o deslocamento atual.
            double chiQuadrado = calcularChiQuadrado(frequenciasTexto, deslocamento);
            // Se o valor do Chi-Quadrado for menor que o menor valor encontrado até agora,
            // atualiza o melhor deslocamento.
            if (chiQuadrado < menorChiQuadrado) {
                menorChiQuadrado = chiQuadrado;
                melhorDeslocamento = deslocamento;
            }
        }

        StringBuilder textoDecifrado = new StringBuilder();

        // Decifra o texto usando o deslocamento identificado.
        for (char c : textoNormalizado.toCharArray()) {
            if (Character.isLetter(c)) {
                // Calcula o caractere decifrado aplicando o deslocamento inverso.
                if (Character.isLowerCase(c)) {
                    textoDecifrado.append((char) (((c - 'a' - melhorDeslocamento + 26) % 26) + 'a'));
                } else {
                    textoDecifrado.append((char) (((c - 'A' - melhorDeslocamento + 26) % 26) + 'A'));
                }
            } else {
                // Se o caractere não é uma letra, adiciona-o diretamente ao texto decifrado.
                textoDecifrado.append(c);
            }
        }

        return new String[]{textoDecifrado.toString(), String.valueOf(melhorDeslocamento)};
    }

    public static void main(String[] args) {
        // Recebe o texto cifrado como entrada do usuário.
        Scanner scanner = new Scanner(System.in);
        String textoCifrado = scanner.nextLine();

        // Decifra o texto e obtém o deslocamento utilizado na cifra.
        String[] resultado = decifrarCesar(textoCifrado);

        // Exibe o deslocamento encontrado e o texto decifrado.
        System.out.println(resultado[1]);
        System.out.println(resultado[0]);
    }
}
