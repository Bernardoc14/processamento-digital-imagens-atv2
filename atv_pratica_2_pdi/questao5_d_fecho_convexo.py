"""
Questao 5d - A partir do resultado do item (c), encontrar o fecho
convexo dos objetos de cor: azul, amarelo e verde.

Baseado no algoritmo de fecho convexo descrito no livro
"Processamento Digital de Imagens" (3a edicao, Gonzalez e Woods).

Requisitos: rodar 'questao5_a_b_c_quadro.py' antes, para gerar os
arquivos 'p_azul.png', 'p_verde.png' e 'p_amarelo.png'.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

import funcoes_morfologicas as fm

# Define as mascaras (regras de hit-or-miss para o fecho convexo)
b1 = np.array([[255, -1, -1],
               [255,  0, -1],
               [255, -1, -1]])

b2 = np.array([[255, 255, 255],
               [-1,    0,  -1],
               [-1,   -1,  -1]])

b3 = np.array([[-1, -1, 255],
               [-1,  0, 255],
               [-1, -1, 255]])

b4 = np.array([[-1, -1, -1],
               [-1,  0, -1],
               [255, 255, 255]])

masks = [b1, b2, b3, b4]


def compararJanelas(image, mask):
    linhas, colunas = image.shape
    result = np.zeros_like(image)  # Inicializa a imagem resultante

    for i in range(linhas):
        for j in range(colunas):
            # Extrai a janela 3x3, considerando 0 fora das bordas
            window = np.zeros((3, 3), dtype=image.dtype)
            for m in range(3):
                for n in range(3):
                    if 0 <= i + m - 1 < linhas and 0 <= j + n - 1 < colunas:
                        window[m, n] = image[i + m - 1, j + n - 1]

            # Verifica casamento com a mascara
            match = all(
                mask[m, n] == -1 or window[m, n] == mask[m, n]
                for m in range(3)
                for n in range(3)
            )

            if match:
                result[i, j] = 255  # Marca pixel central

    return result


def fecho_convexo(image):
    res_final = np.zeros_like(image)  # Inicializa o resultado final
    resultados = []
    for mask in masks:
        imagem_anterior = None
        imagem_atual = image.copy()

        # Itera ate convergencia
        while not np.array_equal(imagem_anterior, imagem_atual):
            imagem_anterior = imagem_atual.copy()
            comp = compararJanelas(imagem_atual, mask)
            imagem_atual = fm.uniao(imagem_atual, comp)  # Uniao com original

        resultados.append(imagem_atual.copy())

    # Itera sobre os resultados
    for imagem_atual in resultados:
        res_final = fm.uniao(imagem_atual, res_final)

    return res_final


def processar(caminho_imagem, nome_cor):
    objeto = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

    # converte pra binaria
    _, objeto = cv2.threshold(objeto, 127, 255, cv2.THRESH_BINARY)

    # inverte as cores pra bater com a convencao (objeto branco, fundo preto)
    objeto = cv2.bitwise_not(objeto)

    fc = fecho_convexo(objeto)

    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1), plt.imshow(objeto, cmap='gray'), plt.title(f'Original ({nome_cor})')
    plt.axis('off')
    plt.subplot(1, 2, 2), plt.imshow(fc, cmap='gray'), plt.title(f'Fecho convexo ({nome_cor})')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return fc


if __name__ == "__main__":
    processar("p_azul.png", "azul")
    processar("p_verde.png", "verde")
    processar("p_amarelo.png", "amarelo")
