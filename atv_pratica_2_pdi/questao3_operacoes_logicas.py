"""
Questao 3 - Crie uma funcao para realizar cada uma das operacoes
morfologicas abaixo (uniao, intersecao, diferenca). Cada funcao deve
receber como parametros duas imagens. Considere que as imagens sao
objetos brancos em um fundo preto.

Imagens de teste usadas no relatorio original: um quadrado branco
(imagem1.png) e uma elipse branca (imagem2.png), ambas 200x200,
feitas no Paint. Substitua pelas suas proprias imagens em
'imagens_entrada/'.
"""

import cv2
import matplotlib.pyplot as plt

import funcoes_morfologicas as fm

CAMINHO_IMG1 = "imagens_entrada/imagem1.png"
CAMINHO_IMG2 = "imagens_entrada/imagem2.png"


def main():
    imagem1 = cv2.imread(CAMINHO_IMG1, cv2.IMREAD_GRAYSCALE)
    imagem2 = cv2.imread(CAMINHO_IMG2, cv2.IMREAD_GRAYSCALE)

    # a. Uniao
    resultado_uniao = fm.uniao(imagem1, imagem2)

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1), plt.imshow(imagem1, cmap='gray'), plt.title('Imagem 1')
    plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(imagem2, cmap='gray'), plt.title('Imagem 2')
    plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(resultado_uniao, cmap='gray'), plt.title('Resultado Uniao')
    plt.axis('off')
    plt.show()

    # b. Intersecao
    resultado_intersecao = fm.intersecao(imagem1, imagem2)

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1), plt.imshow(imagem1, cmap='gray'), plt.title('Imagem 1')
    plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(imagem2, cmap='gray'), plt.title('Imagem 2')
    plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(resultado_intersecao, cmap='gray'), plt.title('Resultado Intersecao')
    plt.axis('off')
    plt.show()

    # c. Diferenca (imagem1 - imagem2)
    resultado_diferenca = fm.diferenca(imagem1, imagem2)

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1), plt.imshow(imagem1, cmap='gray'), plt.title('Imagem 1')
    plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(imagem2, cmap='gray'), plt.title('Imagem 2')
    plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(resultado_diferenca, cmap='gray'), plt.title('Resultado Diferenca')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()
