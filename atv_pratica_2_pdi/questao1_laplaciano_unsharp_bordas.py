"""
Questao 1 - Dada a imagem "lena_gray.bmp", realize as seguintes operacoes:
a) Laplaciano
b) Unsharp masking
c) Filtragem highboost
d) Deteccao de bordas (Prewitt e Sobel)

Requisitos: colocar 'lena_gray.bmp' na pasta 'imagens_entrada/'.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

from filtros import (
    laplaciano,
    borramento_gaussiano,
    prewitt,
    sobel,
)

CAMINHO_IMG = "imagens_entrada/lena_gray.bmp"


def questao_1a():
    img = cv2.imread(CAMINHO_IMG, cv2.IMREAD_GRAYSCALE)

    # Mascara 1: prioriza mais as direcoes horizontais e verticais que as diagonais
    mascara1 = np.array([[0, 1, 0],
                          [1, -4, 1],
                          [0, 1, 0]])

    # Mascara 2: mais isotropica
    mascara2 = np.array([[1, 1, 1],
                          [1, -8, 1],
                          [1, 1, 1]])

    laplacian_m1 = laplaciano(img, mascara1)
    laplacian_m2 = laplaciano(img, mascara2)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1), plt.imshow(img, cmap='gray'), plt.title('Imagem Original')
    plt.axis('off')
    plt.subplot(1, 2, 2), plt.imshow(laplacian_m1, cmap='gray'), plt.title('Laplaciano (mascara 1)')
    plt.axis('off')
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1), plt.imshow(img, cmap='gray'), plt.title('Imagem Original')
    plt.axis('off')
    plt.subplot(1, 2, 2), plt.imshow(laplacian_m2, cmap='gray'), plt.title('Laplaciano (mascara 2)')
    plt.axis('off')
    plt.show()


def questao_1bc():
    image = cv2.imread(CAMINHO_IMG, cv2.IMREAD_GRAYSCALE)

    # Borrar a imagem original
    blurred = borramento_gaussiano(image, (9, 9), 1)  # mascara 9x9 e sigma = 1

    # Subtrair a imagem borrada da original para criar a mascara
    mask = cv2.subtract(image, blurred)

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1), plt.imshow(image, cmap='gray'), plt.title('Imagem Original')
    plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(blurred, cmap='gray'), plt.title('Imagem Borrada')
    plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(mask, cmap='gray'), plt.title('Mascara da nitidez')
    plt.axis('off')
    plt.show()

    # Unsharp mask (k = 1)
    k = 1
    sharpened = cv2.addWeighted(image, 1.0, mask, k, 0)
    plt.figure()
    plt.imshow(sharpened, cmap='gray')
    plt.title(f'Imagem com Unsharp Mask (k={k})')
    plt.axis('off')
    plt.show()

    # Filtragem highboost (k = 2 ate 10)
    plt.figure(figsize=(12, 12))
    for idx, k in enumerate(range(2, 11), start=1):
        # Adicionar a mascara a imagem original com um peso k
        sharpened = cv2.addWeighted(image, 1.0, mask, k, 0)
        plt.subplot(3, 3, idx)
        plt.imshow(sharpened, cmap='gray')
        plt.title(f'Highboost (k={k})')
        plt.axis('off')
    plt.tight_layout()
    plt.show()


def questao_1d():
    img = cv2.imread(CAMINHO_IMG, cv2.IMREAD_GRAYSCALE)

    # i. Prewitt
    grad_x, grad_y, magnitude = prewitt(img)

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1), plt.imshow(img, cmap='gray'), plt.title('Imagem Original')
    plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(grad_x, cmap='gray'), plt.title('Bordas - Gradiente X')
    plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(grad_y, cmap='gray'), plt.title('Bordas - Gradiente Y')
    plt.axis('off')
    plt.show()

    plt.figure()
    plt.imshow(magnitude, cmap='gray')
    plt.title('Magnitude do Gradiente')
    plt.axis('off')
    plt.show()

    # ii. Sobel
    grad_x_s, grad_y_s, magnitude_s = sobel(img)

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1), plt.imshow(img, cmap='gray'), plt.title('Imagem Original')
    plt.axis('off')
    plt.subplot(1, 3, 2), plt.imshow(grad_x_s, cmap='gray'), plt.title('Bordas Sobel - Gradiente X')
    plt.axis('off')
    plt.subplot(1, 3, 3), plt.imshow(grad_y_s, cmap='gray'), plt.title('Bordas Sobel - Gradiente Y')
    plt.axis('off')
    plt.show()

    plt.figure()
    plt.imshow(magnitude_s, cmap='gray')
    plt.title('Magnitude do Gradiente Sobel')
    plt.axis('off')
    plt.show()

    # iii. Diferenca entre Prewitt e Sobel
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 3, 1), plt.imshow(magnitude_s - magnitude, cmap='gray'), plt.title('Sobel - Prewitt, Magnitude')
    plt.axis('off')
    plt.subplot(2, 3, 2), plt.imshow(grad_x_s - grad_x, cmap='gray'), plt.title('Sobel - Prewitt, Gradiente X')
    plt.axis('off')
    plt.subplot(2, 3, 3), plt.imshow(grad_y_s - grad_y, cmap='gray'), plt.title('Sobel - Prewitt, Gradiente Y')
    plt.axis('off')
    plt.subplot(2, 3, 4), plt.imshow(magnitude - magnitude_s, cmap='gray'), plt.title('Prewitt - Sobel, Magnitude')
    plt.axis('off')
    plt.subplot(2, 3, 5), plt.imshow(grad_x - grad_x_s, cmap='gray'), plt.title('Prewitt - Sobel, Gradiente X')
    plt.axis('off')
    plt.subplot(2, 3, 6), plt.imshow(grad_y - grad_y_s, cmap='gray'), plt.title('Prewitt - Sobel, Gradiente Y')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    questao_1a()
    questao_1bc()
    questao_1d()
