import streamlit as st

download_page = st.Page("download.py", title="Загрузка данных", icon="📁")
dashboard_page = st.Page("dashboard.py", title="Диграмма загруженности", icon="📈")
glossary_page = st.Page("glossary.py", title='Справочник', icon='📖')

pg = st.navigation([download_page, dashboard_page, glossary_page])
st.set_page_config(page_title="Загрузка данных", page_icon="📥", layout="wide")
pg.run()
