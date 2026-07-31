"""
morfologia.py (importado como 'mf' nos outros scripts)

Operacoes morfologicas basicas: dilatacao, erosao, abertura e fechamento.
Cada funcao recebe a imagem a ser transformada, o elemento estruturante
e o centro dele. Considera-se que as imagens sao objetos brancos (255)
em um fundo preto (0).
"""

import numpy as np


def dilatacao(imagem, elemento_estruturante, centro):
    # pego as dimensoes da imagem e do elemento estruturante
    altura_img, largura_img = imagem.shape
    altura_ee, largura_ee = elemento_estruturante.shape

    # e criado uma nova imagem de saida com zeros
    imagem_dilatada = np.zeros_like(imagem)

    # e definido o centro do elemento estruturante
    centro_x, centro_y = centro

    # Percorre cada pixel da imagem
    for i in range(altura_img):
        for j in range(largura_img):
            # Se o pixel atual e branco (valor 255)
            if imagem[i, j] == 255:
                # Percorre cada pixel do elemento estruturante
                for m in range(altura_ee):
                    for n in range(largura_ee):
                        # Se o pixel do elemento estruturante e branco (valor 255)
                        if elemento_estruturante[m, n] == 255:
                            # Calcula a posicao na imagem dilatada
                            x = i + (m - centro_x)
                            y = j + (n - centro_y)
                            # Verifica se a posicao calculada esta dentro dos limites da imagem
                            if 0 <= x < altura_img and 0 <= y < largura_img:
                                # Define o pixel correspondente na imagem dilatada como branco
                                imagem_dilatada[x, y] = 255

    # Retorna a imagem dilatada
    return imagem_dilatada


def erosao(imagem, elemento_estruturante, centro):
    # pego as dimensoes da imagem e do elemento estruturante
    altura_img, largura_img = imagem.shape
    altura_ee, largura_ee = elemento_estruturante.shape

    # e criado uma nova imagem de saida com zeros (toda preta que e o fundo)
    imagem_erodida = np.zeros_like(imagem)

    # e definido o centro do elemento estruturante
    centro_x, centro_y = centro

    # Percorre cada pixel da imagem
    for i in range(altura_img):
        for j in range(largura_img):
            is_eroded = True  # Assume que o pixel sera erodido
            # Percorre cada pixel do elemento estruturante
            for m in range(altura_ee):
                for n in range(largura_ee):
                    # Verifica se o pixel do elemento estruturante e 255 (parte do elemento)
                    if elemento_estruturante[m, n] == 255:
                        # Calcula a posicao correspondente na imagem original
                        x = i + (m - centro_x)
                        y = j + (n - centro_y)

                        # Verifica se a posicao esta dentro dos limites da imagem e se o pixel e 255
                        if not (0 <= x < altura_img and 0 <= y < largura_img and imagem[x, y] == 255):
                            is_eroded = False  # Se nao estiver, o pixel nao sera erodido
                            break
                if not is_eroded:
                    break
            # Se todos os pixels do elemento estruturante corresponderem,
            # entao aquele pixel permanece na imagem, portanto, pinto de branco
            if is_eroded:
                imagem_erodida[i, j] = 255

    return imagem_erodida  # Retorna a imagem erodida


def abertura(imagem, elemento_estruturante, centro):
    # aqui e mais simples, basta chamar uma erosao
    # e depois dilatar a imagem erodida
    erodir = erosao(imagem, elemento_estruturante, centro)
    dilatar = dilatacao(erodir, elemento_estruturante, centro)
    return dilatar


def fechamento(imagem, elemento_estruturante, centro):
    # aqui e mais simples, basta chamar uma dilatacao
    # e depois erodir a imagem dilatada
    dilatar = dilatacao(imagem, elemento_estruturante, centro)
    erodir = erosao(dilatar, elemento_estruturante, centro)
    return erodir
