"""
funcoes_morfologicas.py (importado como 'fm' nos outros scripts)

Operacoes logicas entre imagens binarias (objetos brancos - 255,
fundo preto - 0). Cada funcao recebe duas imagens do mesmo tamanho.
"""

import numpy as np


def uniao(imagem1, imagem2):
    # criar uma imagem preenchida com zeros com o mesmo tamanho da imagem1
    resultado = np.zeros_like(imagem1, dtype=np.uint8)
    for i in range(imagem1.shape[0]):  # percorrendo as linhas
        for j in range(imagem1.shape[1]):  # percorrendo as colunas
            # pega sempre o maior valor de cada pixel
            if imagem1[i, j] > imagem2[i, j]:
                resultado[i, j] = imagem1[i, j]
            else:
                resultado[i, j] = imagem2[i, j]

    return resultado


def intersecao(imagem1, imagem2):
    # criar uma imagem preenchida com zeros com o mesmo tamanho da imagem1
    resultado = np.zeros_like(imagem1, dtype=np.uint8)
    for i in range(imagem1.shape[0]):  # percorrendo as linhas
        for j in range(imagem1.shape[1]):  # percorrendo as colunas
            # se alguma delas for preta nao ha intersecao, entao vira preto,
            # mas se as duas forem brancas ha intersecao
            if imagem1[i, j] == 0 or imagem2[i, j] == 0:
                resultado[i, j] = 0
            else:
                resultado[i, j] = 255

    return resultado


def diferenca(imagem1, imagem2):
    # criar uma imagem preenchida com zeros com o mesmo tamanho da imagem1
    resultado = np.zeros_like(imagem1, dtype=np.uint8)
    for i in range(imagem1.shape[0]):  # percorrendo as linhas
        for j in range(imagem1.shape[1]):  # percorrendo as colunas
            # se ambos forem pretos, continua preto, se ambos forem brancos, vira preto
            # se A for branco e B preto, continua branco, se A for preto e B branco, continua preto
            if imagem1[i, j] == 0 and imagem2[i, j] == 0:
                resultado[i, j] = 0
            elif imagem1[i, j] == 255 and imagem2[i, j] == 0:
                resultado[i, j] = 255
            elif imagem1[i, j] == 0 and imagem2[i, j] == 255:
                resultado[i, j] = 0
            else:
                resultado[i, j] = 0

    return resultado
