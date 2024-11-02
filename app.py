import streamlit as st
from pages.import_page import main as import_page  # Импортируем основную функцию страницы Import

# Основная функция приложения
def main():
    st.set_page_config(page_title="Allamuchy Cars Stat", layout="wide", initial_sidebar_state="collapsed")

    # Меню
    tabs = st.tabs(["Import", "Other"])  # Добавляем другие вкладки, которые можно будет расширить

    # Вкладка для страницы "Import"
    with tabs[0]:
        import_page()  # Запуск страницы Import

    # Вкладка-заглушка для других страниц (пока пустая)
    with tabs[1]:
        st.write("Дополнительные страницы")

if __name__ == "__main__":
    main()
