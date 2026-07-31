"""
Questao 2 - Aplique as mascaras abaixo na imagem "lena_ruido.bmp" e
compare cada resultado com o filtro da mediana.

Requisitos: colocar 'lena_ruido.bmp' na pasta 'imagens_entrada/'.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

from filtros import aplicar_convolucao, aplicar_filtro_mediana

CAMINHO_IMG = "imagens_entrada/lena_ruido.bmp"


def main():
    image = cv2.imread(CAMINHO_IMG, cv2.IMREAD_GRAYSCALE)

    # Definindo as mascaras
    mask1 = (1 / 5) * np.array([[0, 1, 0],
                                 [1, 1, 1],
                                 [0, 1, 0]], dtype=np.float32)

    mask2 = (1 / 9) * np.array([[1, 1, 1],
                                 [1, 1, 1],
                                 [1, 1, 1]], dtype=np.float32)

    mask3 = (1 / 32) * np.array([[1, 3, 1],
                                  [3, 16, 3],
                                  [1, 3, 1]], dtype=np.float32)

    mask4 = (1 / 8) * np.array([[0, 1, 0],
                                 [1, 4, 1],
                                 [0, 1, 0]], dtype=np.float32)

    # Aplicar filtros com as mascaras
    filtrada1 = aplicar_convolucao(image, mask1)
    filtrada2 = aplicar_convolucao(image, mask2)
    filtrada3 = aplicar_convolucao(image, mask3)
    filtrada4 = aplicar_convolucao(image, mask4)

    # Aplicar o filtro da mediana com uma janela de 3x3
    filtro_mediana = aplicar_filtro_mediana(image, 3)

    # Exibir os resultados
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Imagem Original')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(filtrada1, cmap='gray')
    plt.title('Mascara 1')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.imshow(filtrada2, cmap='gray')
    plt.title('Mascara 2')
    plt.axis('off')

    plt.subplot(2, 3, 4)
    plt.imshow(filtrada3, cmap='gray')
    plt.title('Mascara 3')
    plt.axis('off')

    plt.subplot(2, 3, 5)
    plt.imshow(filtrada4, cmap='gray')
    plt.title('Mascara 4')
    plt.axis('off')

    plt.subplot(2, 3, 6)
    plt.imshow(filtro_mediana, cmap='gray')
    plt.title('Filtro da Mediana')
    plt.axis('off')
    plt.show()

    # Comparando a mediana com cada resultado de mascara usado, fazendo uma
    # subtracao absoluta da imagem filtrada com a mascara menos a imagem
    # filtrada com a mediana
    diffs = [
        ("Diferenca Mascara 1", filtrada1),
        ("Diferenca Mascara 2", filtrada2),
        ("Diferenca Mascara 3", filtrada3),
        ("Diferenca Mascara 4", filtrada4),
    ]

    plt.figure(figsize=(10, 8))
    for idx, (titulo, filtrada) in enumerate(diffs, start=1):
        diferenca_abs = np.abs(filtrada - filtro_mediana)
        plt.subplot(2, 2, idx)
        plt.imshow(diferenca_abs, cmap='gray')
        plt.title(titulo)
        plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()
