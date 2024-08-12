import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64





st.set_page_config(
    page_icon=":barber",
    page_title="BarberApp",
)


    
#st.sidebar.success('Selecione  a página ')
col1, col2,col3 = st.columns([1,2,1])

col2.markdown("# :blue[Bem vindo ao BarberApp]:blue[ ]")
col2.markdown("#  ") 

st.video("https://www.youtube.com/watch?v=n77aCvR6D-A")


texto1 = st.text('Espaço de Beleza BarberShop. WhatsApp (77)9.9999-9999')




