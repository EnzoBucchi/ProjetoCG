import streamlit as st
import pandas as pd
import numpy as np
import cv2 as cv
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

arquivo_imagem = st.file_uploader(
    "Arquivo da Imagem:",
    help="Faça upload de uma imagem",
)

if arquivo_imagem is not None:
    imagem = Image.open(arquivo_imagem)
    coordenadas = streamlit_image_coordinates(imagem)
    matriz_img = np.array(imagem)
    if coordenadas is not None:
        rgb_pixel = (matriz_img[coordenadas["y"]][coordenadas["x"]])
        st.write(rgb_pixel)

    