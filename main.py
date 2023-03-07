import streamlit as st
import pandas as pd
import numpy as np
import math as mt
from PIL import Image
import matplotlib.pyplot as plt
from streamlit_image_coordinates import streamlit_image_coordinates

### FUNÇÕES DE CONVERSÃO ###
def rgb_to_cmy(rgb_array):
    return [(255 - rgb_array[0]), (255 - rgb_array[1]), (255 - rgb_array[2])]

def rgb_to_hsi(rgb_array):
    Sum = sum(rgb_array)
    
    r = rgb_array[0] / Sum
    g = rgb_array[1] / Sum
    b = rgb_array[2] / Sum
    
    h_part = mt.pow((mt.pow((r - g), 2) + (r - b) * (g - b)), 0.5)
    if h_part != 0:
        if b <= g:
            h = mt.acos(((0.5 * ((r - g) + (r - b))) / h_part))
        else:
            h = 2 * mt.pi - (mt.acos(((0.5 * ((r - g) + (r - b))) / h_part)))
    else:
        h = 0
        
    s = 1 - 3 * min(r, g, b)
    i = Sum / (3 * 255)
    
    H = round((h * 180) / mt.pi)
    S = round(s * 100)
    I = round(i * 255)
    
    return [(H), (S), (I)] 

def hsi_to_rgb(hsi_array):
    h = hsi_array[0] * mt.pi / 180
    s = hsi_array[1] / 100
    i = hsi_array[2] / 255
    
    opt = 0
    if 2 * mt.pi / 3 <= h < 4 * mt.pi / 3:
        h = h - 2 * mt.pi / 3
        opt = 1
    elif 4 * mt.pi / 3 <= h < 2 * mt.pi:
        h = h - 4 * mt.pi / 3
        opt = 2
    
    x = i * (1 - s)
    y = i * (1 + (s * mt.cos(h) / mt.cos(mt.pi / 3 - h)))
    z = 3 * i - (x + y)
    
    if opt == 1:
        r = x
        g = y
        b = z
    elif opt == 2:
        r = z
        g = x
        b = y
    else:
        r = y
        g = z
        b = x
        
    return [(255 * r), (255 * g), (255 * b)]

### LUMINANCIA ###
#   -- Histograma
#   -- Equalização de Histogram
#   -- Binarização (manual)
#   -- Binarização com Otsu (extra)
#
def alterarLuminancia(imagem):
    novaImagem = imagem.copy()

    for x in range(imagem.width):
        for y in range(imagem.height):
            pixel = imagem.getpixel((x,y))
            media = int(pixel[0]*0.299 + pixel[1]*0.587 + pixel[2]*0.114)
            novaImagem.putpixel((x,y), (media, media, media))

    return novaImagem

def histograma(imagem):
    matriz = np.array(imagem)
    histograma, bins = np.histogram(matriz.flatten(), bins=256, range=(0, 256))

    resultado, ax = plt.subplots()
    ax.bar(bins[:-1], histograma, width=1)
    ax.set_xlim(0, 256)
    ax.set_ylim(0, np.max(histograma))
    ax.set_xlabel('Intensidade pixel')
    ax.set_ylabel('N° pixels')
    ax.set_title('Histograma')
    resultado.set_figheight(3)
    resultado.set_figwidth(10)
    st.pyplot(resultado)

### BRILHO ###
def alterarBrilho(imagem, brilho):
    teste = 5;
    return imagem

### MATIZ ###
def alterarMatiz(imagem, brilho):
    teste = 5;
    return imagem

### MONTAGEM DA INTERFACE ###
arq_image = st.file_uploader(
    "Arquivo da Imagem:",
    help="Faça upload de uma imagem",
)

if arq_image is not None:
    image = Image.open(arq_image)
    image_matrix = np.array(image)
    image.histogram()
    
    coords = streamlit_image_coordinates(image)
    
    line1 = st.columns((1, 1, 1))
    line2 = st.columns((1, 1, 1))
    line3 = st.columns((1, 1, 1))
    
    if coords is not None:
        rgb_pixel = (image_matrix[coords["y"]][coords["x"]])
        cmy_pixel = rgb_to_cmy(rgb_pixel)
        hsi_pixel = rgb_to_hsi(rgb_pixel)
        
        with line1[0]:
            st.write("R = " + str(rgb_pixel[0]))
        with line2[0]:
            st.write("G = " + str(rgb_pixel[1]))
        with line3[0]:
            st.write("B = " + str(rgb_pixel[2]))
            
        with line1[1]:
            st.write("C = " + str(cmy_pixel[0]))
        with line2[1]:
            st.write("M = " + str(cmy_pixel[1]))
        with line3[1]:
            st.write("Y = " + str(cmy_pixel[2]))
            
        with line1[2]:
            st.write("H = " + str(hsi_pixel[0]))
        with line2[2]:
            st.write("S = " + str(hsi_pixel[1]))
        with line3[2]:
            st.write("I = " + str(hsi_pixel[2]))
    
    if st.button("Luminância e Histograma"):
        novaImagem = alterarLuminancia(image)
        st.image(novaImagem) 
        histograma(novaImagem)

    brightness = st.sidebar.slider("Brilho", min_value=0, max_value=100, value=50)
    if brightness != 50:
        novaImagem = alterarBrilho(image, brightness);
        st.image(novaImagem) 

    hue = st.sidebar.slider("Matiz", min_value=0, max_value=360, value=0)
    if hue != 0:
        novaImagem = alterarMatiz(image, brightness);
        st.image(novaImagem)