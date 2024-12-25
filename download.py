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

@st.cache_data
def get_glossary(filename: str | None):

    glos_dataframe = pd.read_excel(
        filename,
        skiprows=1,
        engine="calamine",
    )
    return glos_dataframe


glossary_head = "Шаг 1: Загрузите данные справочника (.xlsx)"

st.subheader(glossary_head)
image = Image.open(fp=str(BASE_DIR) + r"/image.png")
st.image(image, caption="Убедитесь, что вы загрузили данные в таком формате...")
uploaded_glos_file = st.file_uploader("📥 Выберите файл для загрузки", type=["xlsx"], key='glossary')
if uploaded_glos_file is not None:
    glos_df = get_glossary(uploaded_glos_file)
    st.session_state["glos_df"] = glos_df

st.divider()

# Первая часть - загрузка данных и просмотр датафрейма
text_head = "Шаг 2: Загрузите данные о загруженности оборудования (.xlsx)"

st.subheader(text_head)
image = Image.open(fp=str(BASE_DIR) + r"/example.png")
st.image(image, caption="Убедитесь, что вы загрузили данные в таком формате...")
uploaded_file = st.file_uploader("📥 Выберите файл для загрузки", type=["xlsx"], key='main_data')
if uploaded_file is not None:
    # if 'load' not in st.session_state or st.session_state['load'] == False:
    #     st.info('Дождитесь загрузки данных', icon="ℹ️")
    #     st.session_state['load'] = True
    df = get_data(uploaded_file)
    st.session_state["df"] = df