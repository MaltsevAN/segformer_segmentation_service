import streamlit as st
from PIL import Image
import requests
import io
from settings import current_settings
from utils import img2bytes
url_segm = f'http://{current_settings.HOST}:{current_settings.PORT}/api/segmentation_img'

st.title('Semantic Segmentation using SegFormer')
origin_col, segmentation_col = st.columns(2)
with origin_col:
    raw_image = st.file_uploader('Raw Input Image', type=['png', 'jpg'])
with segmentation_col:
    segm_button = st.button("Segmentation")

if raw_image is not None:
    with origin_col:
        image = Image.open(raw_image)
        st.image(image, caption="Оригинальное изображение")
    with segmentation_col:
        if segm_button:
            response = requests.post(url_segm,
                                     files={'file': (raw_image.name,
                                                     raw_image.getvalue(),
                                                     raw_image.type)
                                            })
            seg_img = Image.open(io.BytesIO(response.content))
            st.image(seg_img)
