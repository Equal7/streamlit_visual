import time

import streamlit as st
import pandas as pd
from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent


@st.cache_data
def get_data(filename: str | None):

    dataframe = pd.read_excel(
        filename,
        skiprows=1,
        usecols=[0,1,2,3,4,5],
        engine="calamine",
    )
    dataframe = dataframe[
        ~(dataframe["Дата запуска"].isna() | dataframe["Дата остановки"].isna())
    ]
    dataframe["Задача"] = (
        dataframe["Название"].astype(str)
        + "-"
        + dataframe["Серийный номер"].astype(str)
    )
    dataframe = dataframe[
        [
            "Участок",
            "Операция",
            "Задача",
            "Дата запуска",
            "Дата остановки",
        ]
    ].sort_values(by=['Задача'])
    return dataframe


# Первая часть - загрузка данных и просмотр датафрейма
text_head = "Загрузите данные в формате .xlsx"
# test_download_head = f"<p style='font-family: Arial; color: black; font-size: 25px; text-align: center'>{text_head}</p>"
# st.markdown(test_download_head, unsafe_allow_html=True)
st.subheader(text_head)
image = Image.open(fp=str(BASE_DIR) + r"/example.png")
st.image(image, caption="Убедитесь, что вы загрузили данные в таком формате...")
uploaded_file = st.file_uploader("Выберите файл для загрузки", type=["xlsx"])
if uploaded_file is not None:
    # if 'load' not in st.session_state or st.session_state['load'] == False:
    #     st.info('Дождитесь загрузки данных', icon="ℹ️")
    #     st.session_state['load'] = True
    df = get_data(uploaded_file)
    st.session_state["df"] = df
