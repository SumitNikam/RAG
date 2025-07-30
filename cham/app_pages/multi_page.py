import streamlit as st
from PIL import Image


class MultiPage:

    def __init__(self, app_name) -> None:
        self.pages = []
        self.app_name = app_name
        vf_logo = Image.open("./assets/Vodafone.png")

        st.set_page_config(
            page_title=self.app_name,
            layout="wide",
            page_icon=vf_logo
        )

    def app_page(self, title, func, *params) -> None:
        """ Appends title"""
        self.pages.append(
            {
                "title": title,
                "function": func,
                "params": params
            }
        )

    def page_run(self):
        st.logo("./assets/vodafone_sidebar_logo.png", icon_image="./assets/Vodafone.png")

        page = st.sidebar.selectbox(
            'Select Page...',
            self.pages,
            format_func=lambda page: page['title']
        )

        page['function'](*page['params'])
