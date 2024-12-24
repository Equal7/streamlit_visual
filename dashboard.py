import os
import datetime

import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd
from pandas.tseries.offsets import DateOffset

# import matplotlib.pyplot as plt
from PIL import Image


st.markdown(
    """
        <style>
        /* The input itself */
        div[data-baseweb="select"] > div {
            # background-color:#fff;
            # border-color:rgb(194, 189, 189);
            # width: 50%;
            # font-size: 12px !important;
        }

        /* change the tag font properties */
        span[data-baseweb="tag"] {
            # color: black;
            # font-size: 14px;
            width: 45%;
            # background-color: black;
        }

        span[data-baseweb="tag"]>span {
            # color: black;
            font-size: 12px;
            # background-color: black;
        }

        li {
            # background-color: green !important;
        }
        </style>
    """,
    unsafe_allow_html=True,
)
# print('df', st.session_state['df'])
# NOTE: отключено 
def filtered_dataframe(start, finish, uchs):
    st.session_state['result_df'] = st.session_state['df'][
        (st.session_state['df']["Участок"].isin(uchs))
        & (st.session_state['df']["Дата запуска"] >= pd.to_datetime(start))
        & (st.session_state['df']["Дата остановки"] <= pd.to_datetime(finish))
    ]

def filter_by_date():
    st.session_state['result_df'] = st.session_state['df'][
       (st.session_state['df']["Дата запуска"] >= pd.to_datetime(st.session_state['filter_start_date']))
        & (st.session_state['df']["Дата остановки"] <= pd.to_datetime(st.session_state['filter_finish_date']))
    ]

def filter_by_uchs():
    st.session_state['result_df'] = st.session_state['df'][
        (st.session_state['df']["Участок"].isin(st.session_state['uchs']))
        & (st.session_state['df']["Дата запуска"] >= pd.to_datetime(st.session_state['filter_start_date']))
        & (st.session_state['df']["Дата остановки"] <= pd.to_datetime(st.session_state['filter_finish_date']))
    ]

if 'df' in st.session_state:   
    
    # Получите минимальную и максимальную дату
    if 'min_date' not in st.session_state:
        st.session_state['min_date'] = st.session_state['df']["Дата запуска"].dt.date.min()
    if 'max_date' not in st.session_state:
        st.session_state['max_date'] = st.session_state['df']["Дата остановки"].dt.date.max()

    start_slider_date = st.session_state['min_date']
    finish_slider_date = (st.session_state['min_date'] + DateOffset(days=7)).date()

    if 'uchs' not in st.session_state:
        st.session_state['uchs'] = st.session_state.get('uchs', None)

    if 'result_df' not in st.session_state:
        st.session_state['result_df'] = st.session_state['df']

    with st.sidebar:
        st.header("Фильтры")
        st.session_state['filter_start_date'], st.session_state['filter_finish_date'] = st.slider(
            "Выберите диапазон дат:",
            min_value=st.session_state['min_date'],
            max_value=st.session_state['max_date'],
            value=(start_slider_date, finish_slider_date),
            on_change=filter_by_date,
            # args=(start_date, end_date),
        )
        st.session_state['uchs'] = st.multiselect(
            "Выберите участки:",
            options=st.session_state['df']["Участок"].unique(),
            # on_change=filter_by_uchastok,
            default=st.session_state['df']["Участок"].unique()[0],
        )
        print('uchs', st.session_state['uchs'])
        if st.session_state['uchs']:
            unique_tasks = st.session_state['df'][st.session_state['df']['Участок'].isin(st.session_state['uchs'])]
            uniq_tasks_list = unique_tasks["Задача"].unique()
            # st.write(st.session_state['uchs'])
            st.session_state['tasks'] = st.multiselect(
                "Выберите оборудование:",
                options=uniq_tasks_list,
                # on_change=filter_by_uchastok,
                default=uniq_tasks_list[0],
            )
        if st.session_state['uchs'] and st.session_state['tasks']:
            unique_tasks_plus_operations = unique_tasks[unique_tasks['Задача'].isin(st.session_state['tasks'])]
            uniq_oper_list = unique_tasks_plus_operations["Операция"].unique()
            st.session_state['operations'] = st.multiselect(
                "Выберите операции:",
                options=uniq_oper_list,
                # on_change=filter_by_uchastok,
                default=uniq_oper_list[0],
            )
        # with st.expander("See explanation2"):
        # st.session_state['tasks'] = st.container(height=150).multiselect(
    
    # print('uchs', st.session_state['uchs'])
    filtered_df = st.session_state['df'][
        (st.session_state['df']["Участок"].isin(st.session_state['uchs']))
        & (st.session_state['df']["Операция"].isin(st.session_state['operations']))
        & (st.session_state['df']["Задача"].isin(st.session_state['tasks']))
        & (st.session_state['df']["Дата запуска"] >= pd.to_datetime(st.session_state['filter_start_date']))
        & (st.session_state['df']["Дата остановки"] <= pd.to_datetime(st.session_state['filter_finish_date']))
    ]

    # print('filtered_df', filtered_df)

    fig = px.timeline(
        filtered_df,
        x_start="Дата запуска",
        x_end="Дата остановки",
        y="Задача",
        hover_name="Операция",
        color_discrete_sequence=px.colors.qualitative.Prism,
        opacity=0.5,
        range_x=None,
        range_y=None,
        template="plotly_white",
        height=800,
        width=1500,
        color="Операция",
        title="<b>Загруженность оборудования</b>",
        #                   , color=colors
    )
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.update_traces(  # marker_color='rgb(158,202,225)'
        marker_line_color="rgb(8,48,107)", marker_line_width=1.5, opacity=0.95
    )

    fig.update_layout(
        title="<b>Загруженность оборудования</b>",
        title_x=0.3,
        title_font_size=36,
        xaxis_title="",
        #     margin_l=400,
        yaxis_title="",
        #     legend_title="Dimension: ",
        font=dict(family="Arial", size=32, color="darkgray"),
        showlegend=False
    )


    # Отобразите диаграмму на странице
    st.plotly_chart(fig)



