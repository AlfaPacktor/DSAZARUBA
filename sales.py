import streamlit as st
import pandas as pd
import json
import os


DATA_FILE = "sales_data.json"


EMPLOYEES = [
    "Константинов Я.",
    "Михно Д.",
    "Ласковая А.",
    "Фельдман Л.",
    "Орлик Л.",
    "Шевчак В.",
    "Колесникова А.",
    "Шувалов И.",
    "Шабунина Д."
]

PRODUCTS = [
    "Кредит Наличными",
    "Коробочное Страхование"
]


def create_empty_data():
    return {
        emp: {prod: 0 for prod in PRODUCTS}
        for emp in EMPLOYEES
    }


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return create_empty_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def init_data():
    if "sales_data" not in st.session_state:
        st.session_state.sales_data = load_data()


def input_section():

    st.header("Ввод данных")

    employee = st.selectbox(
        "Выберите сотрудника",
        EMPLOYEES
    )

    st.subheader(f"Продажи сотрудника: {employee}")

    entries = {}

    for product in PRODUCTS:

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            value = st.number_input(
                product,
                min_value=0,
                step=1,
                key=f"value_{employee}_{product}"
            )

        with col2:
            operation = st.radio(
                "Операция",
                ["+", "-"],
                horizontal=True,
                key=f"op_{employee}_{product}"
            )

        entries[product] = (value, operation)

    if st.button("Принять данные"):

        for product, (value, operation) in entries.items():

            if value > 0:

                if operation == "+":
                    st.session_state.sales_data[employee][product] += value
                else:
                    st.session_state.sales_data[employee][product] -= value

        save_data(st.session_state.sales_data)

        st.success("Данные обновлены и сохранены")


def leaderboard():

    st.header("Рейтинг")

    tabs = st.tabs(PRODUCTS)

    for i, product in enumerate(PRODUCTS):

        with tabs[i]:

            ranking = []

            for emp in EMPLOYEES:

                score = st.session_state.sales_data[emp][product]

                ranking.append({
                    "Сотрудник": emp,
                    "Продажи": score
                })

            df = pd.DataFrame(ranking)

            df = df.sort_values(
                by="Продажи",
                ascending=False
            ).reset_index(drop=True)

            df.index += 1

            st.dataframe(
                df,
                use_container_width=True
            )


def main():

    st.set_page_config(
        page_title="Конкурс продаж",
        layout="wide"
    )

    st.title("🏆 Конкурс продаж")

    init_data()

    input_section()

    st.divider()

    leaderboard()


if __name__ == "__main__":
    main()
