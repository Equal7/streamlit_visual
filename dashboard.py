import streamlit as st
import plotly.express as px
import pandas as pd
from pandas.tseries.offsets import DateOffset


st.markdown(
    """
        <style>
        /* The input itself */
        div[data-baseweb="select"] > div > div {
            overflow-y: scroll;
            max-height: 150px;
        }

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
            width: auto;
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

# NOTE: отключено
# def filtered_dataframe(start, finish, uchs):
#     st.session_state["result_df"] = st.session_state["df"][
#         (st.session_state["df"]["Участок"].isin(uchs))
#         & (st.session_state["df"]["Дата запуска"] >= pd.to_datetime(start))
#         & (st.session_state["df"]["Дата остановки"] <= pd.to_datetime(finish))
#     ]

# def filter_by_date():
#     print('check!')
#     st.session_state["result_df"] = st.session_state["df"][
#         (
#             st.session_state["df"]["Дата запуска"]
#             >= pd.to_datetime(st.session_state["filter_start_date"])
#         )
#         & (
#             st.session_state["df"]["Дата остановки"]
#             <= pd.to_datetime(st.session_state["filter_finish_date"])
#         )
#     ]

# def filter_check():
#     st.seession_state['filter_check'] = not st.session_state['filter_check']


def filter_by_uchs():
    # print('uchs check!', st.session_state["uchs_changer"])
    if "Все участки" in st.session_state["uchs_changer"]:
        st.session_state["uchs"] = st.session_state["df"]["Участок"].unique().tolist()
    else:
        st.session_state["uchs"] = st.session_state["uchs_changer"]


def filter_by_oper():
    if "Все операции" in st.session_state["oper_changer"]:
        st.session_state["operations"] = (
            st.session_state["df"][
                st.session_state["df"]["Участок"].isin(st.session_state["uchs"])
            ]["Операция"]
            .unique()
            .tolist()
        )
    else:
        st.session_state["operations"] = st.session_state["oper_changer"]

def filter_by_tasks():
    if "Всё оборудование" in st.session_state["task_changer"]:
        unique_uchs = st.session_state["df"][
                st.session_state["df"]["Участок"].isin(st.session_state["uchs"])
            ]
        st.session_state["tasks"] = (
            unique_uchs[unique_uchs["Операция"].isin(st.session_state["operations"])]
            ['Задача']
            .unique()
            .tolist()
        )
    else:
        st.session_state["tasks"] = st.session_state["task_changer"]


def get_current_state_of_used_glossary(filtered_df: pd.DataFrame):
    main_data = filtered_df
    glossary_data = st.session_state["glos_df"]
    glossary_data["Задача"] = (
        glossary_data["Название"].astype(str)
        + "-"
        + glossary_data["Серийный номер"].astype(str)
    )
    # main_data = main_data.sort_values(by='')
    glossary_data = glossary_data[
        [
            "Участок",
            "Задача",
            "Порядок",
        ]
    ]
    main_data = main_data.merge(glossary_data, how="left", on=["Участок", "Задача"])
    return main_data


# st.header("Диграмма загруженности")

if "df" in st.session_state:

    # Получите минимальную и максимальную дату
    min_date = st.session_state["df"]["Дата запуска"].dt.date.min()
    max_date = st.session_state["df"]["Дата остановки"].dt.date.max()

    if "filter_start_date" not in st.session_state:
        st.session_state["filter_start_date"] = min_date

    if "filter_finish_date" not in st.session_state:
        st.session_state["filter_finish_date"] = (
            st.session_state["filter_start_date"] + DateOffset(days=7)
        ).date()

    if "uchs" not in st.session_state:
        st.session_state["uchs"] = st.session_state.get("uchs", None)

    if "operations" not in st.session_state:
        st.session_state["operations"] = st.session_state.get("operations", None)

    if "tasks" not in st.session_state:
        st.session_state["tasks"] = st.session_state.get("tasks", None)

    with st.sidebar:
        (
            st.session_state["filter_start_date"],
            st.session_state["filter_finish_date"],
        ) = st.slider(
            "Выберите диапазон дат:",
            min_value=min_date,
            max_value=max_date,
            value=(
                st.session_state["filter_start_date"],
                st.session_state["filter_finish_date"],
            ),
        )
        st.multiselect(
            "Выберите участки:",
            options=(
                ["Все участки"] + st.session_state["df"]["Участок"].unique().tolist()
                if len(st.session_state["df"]["Участок"].unique().tolist()) > 1
                else st.session_state["df"]["Участок"].unique().tolist()
            ),
            key="uchs_changer",
            default=st.session_state["uchs"],
            on_change=filter_by_uchs,
        )

        if st.session_state["uchs"]:
            unique_tasks = st.session_state["df"][
                st.session_state["df"]["Участок"].isin(st.session_state["uchs"])
            ]
            uniq_opers_list = unique_tasks["Операция"].unique().tolist()
            st.multiselect(
                "Выберите операции:",
                options=(
                    ["Все операции"] + uniq_opers_list
                    if len(uniq_opers_list) > 1
                    else uniq_opers_list
                ),
                key="oper_changer",
                default=st.session_state["operations"],
                on_change=filter_by_oper,
            )

        if st.session_state["uchs"] and st.session_state["operations"]:
            unique_tasks_plus_operations = unique_tasks[
                unique_tasks["Операция"].isin(st.session_state["operations"])
            ]
            uniq_tasks_list = unique_tasks_plus_operations["Задача"].unique().tolist()
            st.multiselect(
                "Выберите оборудование:",
                options=(
                    ["Всё оборудование"] + uniq_tasks_list
                    if len(uniq_tasks_list) > 1
                    else uniq_tasks_list
                ),
                key="task_changer",
                on_change=filter_by_tasks,
                default=st.session_state["tasks"],
            )

        st.session_state["date_by_day"] = st.radio(
            "Выберите диапазон отображения дат:",
            [
                "Авто",
                "Дневной",
            ],
            horizontal=True,
        )
    # print("tasks", st.session_state["tasks"])
    # print("operations", st.session_state["operations"])
    # print("uchs", st.session_state["uchs"])
    # print("start", st.session_state["filter_start_date"])
    # print("finish", st.session_state["filter_finish_date"])
    # print(st.session_state["df"])
    if (
        st.session_state["uchs"]
        and st.session_state["operations"]
        and st.session_state["tasks"]
        and st.session_state["filter_start_date"]
        and st.session_state["filter_finish_date"]
    ):
        filtered_df = st.session_state["df"][
            (st.session_state["df"]["Участок"].isin(st.session_state["uchs"]))
            & (st.session_state["df"]["Операция"].isin(st.session_state["operations"]))
            & (st.session_state["df"]["Задача"].isin(st.session_state["tasks"]))
            & (
                st.session_state["df"]["Дата запуска"]
                >= pd.to_datetime(st.session_state["filter_start_date"])
            )
            & (
                st.session_state["df"]["Дата остановки"]
                <= pd.to_datetime(st.session_state["filter_finish_date"])
            )
        ]

        filtered_df = get_current_state_of_used_glossary(filtered_df)

        fig = px.timeline(
            filtered_df,
            x_start="Дата запуска",
            x_end="Дата остановки",
            y="Задача",
            hover_name="Операция",
            category_orders={
                # "Операция": sorted(filtered_df["Операция"].unique()),
                "Задача": filtered_df.sort_values(by="Порядок", ascending=True)[
                    "Задача"
                ].unique(),
            },
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

        fig.update_layout(
            # bargap=0.7,
            bargroupgap=0.2,
            # xaxis_range=[
            #     filtered_df["Дата запуска"].min(),
            #     filtered_df["Дата остановки"].max(),
            # ],
            xaxis=dict(
                showgrid=True,
                # rangeslider_visible=True,
                side="bottom",
                # tickmode="array",
                # fixedrange=False,
                # exponentformat='e',
                gridcolor="silver",
                # tickformat="Q%q %Y \n",
                # ticklabelmode="period",
                # ticks="outside",
                # tickson="boundaries",
                # tickwidth=0.1,
                # layer="below traces",
                # ticklen=20,
                # tickfont=dict(family="Old Standard TT, serif", size=24, color="gray"),
                # rangeselector=dict(
                #     buttons=list(
                #         [
                #             dict(count=1, label="1m", step="month", stepmode="backward"),
                #             dict(count=6, label="6m", step="month", stepmode="backward"),
                #             dict(count=1, label="YTD", step="year", stepmode="todate"),
                #             dict(count=1, label="1y", step="year", stepmode="backward"),
                #             dict(step="all"),
                #         ]
                #     ),
                #     x=0.37,
                #     y=-0.05,
                #     font=dict(family="Arial", size=14, color="darkgray"),
                # ),
            ),
            yaxis=dict(
                title="",
                # autorange="min",
                # automargin='width',
                # autoshift=True,
                # ticklen=10,
                # showgrid=True,
                # gridcolor="silver",
                # showticklabels=True,
                tickfont=dict(family="Old Standard TT, serif", size=16, color="gray"),
            ),
            legend=dict(
                orientation="h",
                # yanchor="bottom",
                # y=0.8,
                title="Операции: ",
                # xanchor="right",
                # x=1,
                font=dict(family="Arial", size=12, color="darkgray"),
            ),
            # updatemenus=dict(
            #     buttons=list(
            #         [
            #             dict(args=["dtick", 'D1'], label="False", method="restyle"),
            #             dict(args=["dtick", True], label="True", method="restyle"),
            #         ]
            #     )
            # ),
        )
        if st.session_state["date_by_day"] == "Дневной":
            fig.update_layout(xaxis=dict(dtick="D1"))
        # Add range slider
        # fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"))

        fig.update_traces(  # marker_color='rgb(158,202,225)'
            marker_line_color="rgb(8,48,107)", marker_line_width=1.5, opacity=0.95
        )

        fig.update_layout(
            # title="<b>Загруженность оборудования</b>",
            title_x=0.3,
            title_font_size=36,
            xaxis_title="",
            #     margin_l=400,
            yaxis_title="",
            #     legend_title="Dimension: ",
            font=dict(family="Arial", size=32, color="darkgray"),
            showlegend=False,
        )

        # Отобразите диаграмму на странице
        st.plotly_chart(fig)
