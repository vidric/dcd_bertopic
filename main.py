import streamlit as st
from streamlit_option_menu import option_menu
from tools.utilities import load_css
import json

from views.dashboard import Dashboard
from views.model_bertopic import ModelBertopic

# Initialize connection.
#conn = st.experimental_connection("mysql", type='sql')

st.set_page_config(
    page_title="Customer Review HMNS Menggunakan BERTopic",
    page_icon="favicon.ico",
    layout="wide"
)

load_css()


class Model:
    menuTitle = "Customer Review Dashboard"
    option1 = "Home"
    option2 = "Model BERTopic"
    option3 = "Model Training"
    option4 = "Model Tuning"
    option5 = "Data Produk"
    option6 = "Data Review"

    menuIcon = "menu-up"
    icon1 = "speedometer"
    icon2 = "activity"
    icon3 = "motherboard"
    icon4 = "graph-up-arrow"
    icon5 = "journal-arrow-down"
    icon6 = "clipboard-data"


def view(model):
    with st.sidebar:
        menuItem = option_menu(model.menuTitle,
                               [model.option1, model.option2, model.option5, model.option6],
                               icons=[model.icon1, model.icon2, model.icon5, model.icon6],
                               menu_icon=model.menuIcon,
                               default_index=0,
                               styles={
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "black", "font-size": "25px"},
                                   "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#037ffc"},
                               })

    if menuItem == model.option1:
        Dashboard().view(Dashboard.Model())
        

    if menuItem == model.option2:
        ModelBertopic().view(ModelBertopic.Model())

view(Model())
