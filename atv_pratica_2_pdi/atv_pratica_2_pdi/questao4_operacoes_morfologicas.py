"""
Questao 4 - Crie uma funcao para realizar cada uma das operacoes
morfologicas abaixo. Cada funcao deve receber 3 parametros: a imagem
a ser transformada, o elemento estruturante e o centro dele.
Considere que as imagens sao objetos brancos em um fundo preto.

Imagem de entrada livre: qualquer imagem binaria (objeto branco em
fundo preto) serve para testar a logica. No relatorio original foi
usado um desenho 80x80 feito no Paint (um carrinho), mas o tamanho
nao importa. Elemento estruturante usado: 5x5 de 1s (255), com
centro (2, 2).
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

import morfologia as mf

CAMINHO_IMG = "imagens_entrada/carro.png"

# representacao do elemento estruturante
elemento_estruturante = np.array([
    [255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255],
    [255, 255, 255, 255, 255],
], dtype=np.uint8)

centro = (2, 2)


def main():
    imagem = cv2.imread(CAMINHO_IMG, cv2.IMREAD_GRAYSCALE)

    # a. Dilatacao
    dilatada = mf.dilatacao(imagem, elemento_estruturante, centro)
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1), plt.imshow(imagem, cmap='gray'), plt.title('Original')
    plt.axis('off')
    plt.subplot(1, 2, 2), plt.imshow(dilatada, cmap='gray'), plt.title('Dilatada')
    plt.axis('off')
    plt.show()

    # b. Erosao
    erodida = mf.erosao(imagem, elemento_estruturante, centro)
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1), plt.imshow(imagem, cmap='gray'), plt.title('Original')
    plt.axis('off')
    plt.subplot(1, 2, 2), plt.imshow(erodida, cmap='gray'), plt.title('Erodida')
    plt.axis('off')
    plt.show()

    # c. Abertura
    abertura_img = mf.abertura(imagem, elemento_estruturante, centro)
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1), plt.imshow(imagem, cmap='gray'), plt.title('Original')
    plt.axis('off')
    plt.subplot(1, 2, 2), plt.imshow(abertura_img, cmap='gray'), plt.title('Abertura')
    plt.axis('off')
    plt.show()

    # d. Fechamento
    fechamento_img = mf.fechamento(imagem, elemento_estruturante, centro)
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1), plt.imshow(imagem, cmap='gray'), plt.title('Original')
    plt.axis('off')
    plt.subplot(1, 2, 2), plt.imshow(fechamento_img, cmap='gray'), plt.title('Fechamento')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()
