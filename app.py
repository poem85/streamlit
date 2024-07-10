import streamlit as st
import streamlit_option_menu as som
from info_app import run_info_app


def main():
    st.set_page_config(layout="wide")

    with st.sidebar:
        choose = som.option_menu(
            menu_title="Main Menu",
            options=["Home", "Infomation", "Analysis"],
            icons=["house", "info-square", "activity"],
            menu_icon="app-indicator",
            default_index=0
        )
    
    if choose == "Home":
        st.header('EU Heating Site Analysis')
    elif choose == "Infomation":
        st.subheader('Infomation')
        run_info_app()
    elif choose == "Analysis":
        st.subheader('Analysis')
    

if __name__ == "__main__":
    main()
