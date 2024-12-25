import streamlit as st
import pandas as pd
import io

# buffer to use for excel writer
buffer = io.BytesIO()

st.subheader('Справочник оборудования c порядком визуализации')

if st.session_state.get("glos_df", None) is not None:
    edited_df = st.data_editor(
        st.session_state["glos_df"],
        num_rows="dynamic",
        height=595,
        hide_index=True,
        use_container_width=True,
    )
else:
    empty_df = pd.DataFrame(
        columns=["Участок", "Название", "Серийный номер", "Порядок"]
    )
    edited_df = st.data_editor(
        empty_df, num_rows="dynamic", hide_index=True, use_container_width=True
    )

def to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Справочник оборудования')
    workbook = writer.book
    worksheet = writer.sheets['Справочник оборудования']  
    writer.close()
    processed_data = output.getvalue()
    return processed_data

download = st.download_button(
    label="📥 Выгрузить данные в excel",
    data=to_excel(edited_df),
    file_name="Справочник оборудования c порядком визуализации_.xlsx",
)
