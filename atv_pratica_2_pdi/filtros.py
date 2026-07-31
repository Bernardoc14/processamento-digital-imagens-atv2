"""
filtros.py

Funcoes de filtragem espacial usadas na Questao 1 e 2:
convolucao manual, filtro laplaciano, filtro gaussiano (para
unsharp masking / highboost), deteccao de bordas (Prewitt e
Sobel) e filtro da mediana.
"""

import numpy as np


def aplicar_convolucao(image, mascara):
    pad = mascara.shape[0] // 2
    padded_image = np.pad(image, pad_width=pad, mode='constant', constant_values=0)
    saida = np.zeros_like(image, dtype=np.float32)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            regiao = padded_image[i:i + mascara.shape[0], j:j + mascara.shape[1]]
            saida[i, j] = np.sum(regiao * mascara)

    return saida


def laplaciano(image, mascara=None):
    """
    Filtro laplaciano. Se nenhuma mascara for passada, usa a mascara
    isotropica (com -8 no centro). A outra opcao usada no relatorio foi:
    np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    """
    if mascara is None:
        # Definindo a mascara laplaciana
        mascara = np.array([[1,  1, 1],
                             [1, -8, 1],
                             [1,  1, 1]])

    # Aplicar a convolucao
    imagem_saida = aplicar_convolucao(image, mascara)

    # Normalizando o resultado para o intervalo [0, 255]
    imagem_saida = np.clip(imagem_saida, 0, 255)
    imagem_saida = np.uint8(imagem_saida)

    return imagem_saida


def mascara_gaussiana(size, sigma):
    k = size // 2
    x, y = np.meshgrid(np.arange(-k, k + 1), np.arange(-k, k + 1))
    mascara = np.exp(-(x**2 + y**2) / (2 * sigma**2))

    return mascara / np.sum(mascara)


def borramento_gaussiano(image, mascara_size=(5, 5), sigma=1.0):
    # Criar a mascara Gaussiano
    mascara = mascara_gaussiana(mascara_size[0], sigma)

    # Aplicar a convolucao manualmente
    imagem_borrada = aplicar_convolucao(image, mascara)

    # Garantir que os valores estejam no intervalo [0, 255]
    imagem_borrada = np.clip(imagem_borrada, 0, 255)
    imagem_borrada = np.uint8(imagem_borrada)

    return imagem_borrada


# ------------------- Prewitt -------------------
Gx_prewitt = np.array([[-1, 0, 1],
                        [-1, 0, 1],
                        [-1, 0, 1]])

Gy_prewitt = np.array([[-1, -1, -1],
                        [ 0,  0,  0],
                        [ 1,  1,  1]])


def prewitt(img):
    # Aplicando os filtros na imagem gx e gy
    gradient_x = aplicar_convolucao(img, Gx_prewitt)
    gradient_y = aplicar_convolucao(img, Gy_prewitt)

    # Normalizando o resultado para o intervalo [0, 255]
    gradient_x = np.clip(gradient_x, 0, 255)
    gradient_y = np.clip(gradient_y, 0, 255)

    # Calculando a magnitude do gradiente
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    magnitude = np.clip(magnitude, 0, 255)

    return gradient_x, gradient_y, magnitude


# ------------------- Sobel -------------------
Gx_sobel = np.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]])

Gy_sobel = np.array([[-1, -2, -1],
                      [ 0,  0,  0],
                      [ 1,  2,  1]])


def sobel(img):
    gradient_x = aplicar_convolucao(img, Gx_sobel)
    gradient_y = aplicar_convolucao(img, Gy_sobel)

    gradient_x = np.clip(gradient_x, 0, 255)
    gradient_y = np.clip(gradient_y, 0, 255)

    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    magnitude = np.clip(magnitude, 0, 255)

    return gradient_x, gradient_y, magnitude


# ------------------- Filtro da mediana -------------------
def aplicar_filtro_mediana(image, tamanho_janela):
    pad = tamanho_janela // 2
    padded_image = np.pad(image, pad_width=pad, mode='constant', constant_values=0)
    saida = np.zeros_like(image, dtype=np.float32)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i:i + tamanho_janela, j:j + tamanho_janela]
            saida[i, j] = np.median(region)

    return saida
