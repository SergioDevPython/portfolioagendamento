import streamlit as st
from pymongo import MongoClient
import hashlib


serve_name = st.secrets["service_name"]
data_base = st.secrets["db"]
collection = st.secrets["col"]






# Função para hash de senhas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Função para cadastrar usuário
def cadastrar_usuario(username, password):
    if collection.find_one({"username": username}):
        st.warning("Usuário já existe! Escolha outro nome de usuário.")
    else:
        collection.insert_one({
            "username": username,
            "password": hash_password(password)
        })
        st.success("Usuário cadastrado com sucesso!")

# Função para verificar login
def verificar_login(username, password):
    user = collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True
    else:
        return False

# Interface principal
st.title("Autenticação")

# Menu para seleção de Cadastro ou Login
menu = st.selectbox("Selecione uma opção", ["Login", "Cadastro"])

if menu == "Cadastro":
    st.subheader("Cadastro de Novo Usuário")
    username = st.text_input("Nome de usuário", key="cadastro_username")
    password = st.text_input("Senha", type="password", key="cadastro_password")
    password_confirm = st.text_input("Confirme a senha", type="password", key="cadastro_password_confirm")

    if st.button("Cadastrar"):
        if password == password_confirm:
            cadastrar_usuario(username, password)
        else:
            st.error("As senhas não coincidem. Tente novamente.")

elif menu == "Login":
    st.subheader("Login de Usuário")
    username = st.text_input("Nome de usuário", key="login_username")
    password = st.text_input("Senha", type="password", key="login_password")

    if st.button("Login"):
        if verificar_login(username, password):
            st.success(f"Bem-vindo, {username}!")
            st.balloons()
            # Aqui você pode adicionar o que deve acontecer após o login bem-sucedido
        else:
            st.error("Nome de usuário ou senha incorretos. Tente novamente.")
