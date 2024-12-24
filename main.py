import streamlit as st

download_page = st.Page("download.py", title="Загрузка данных", icon=":material/inbox_tray:")
dashboard_page = st.Page("dashboard.py", title="Диграмма загруженности", icon="📈")

pg = st.navigation([download_page, dashboard_page])
st.set_page_config(page_title="Загрузка данных", page_icon="📥", layout="wide")
pg.run()
