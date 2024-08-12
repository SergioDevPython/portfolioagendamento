import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from PIL import Image
import time
import hashlib

# Configurações da página
st.set_page_config(
    page_icon=":clipboard:",
    page_title="Barber Family",
)

serve_name = st.secrets["service_name"]
data_base = st.secrets["db"]
collection = st.secrets["col"]




# Carregar logo


# Função para hash de senhas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Função para verificar login
def verificar_login(username, password):
    user = collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True
    else:
        return False

# Tela de Login
st.title("Gestão de horários")

username = st.text_input("Nome de usuário")
password = st.text_input("Senha", type="password")

if st.button("Login"):
    if verificar_login(username, password):
        st.success(f"Bem-vindo, {username}!")
        
        # Página principal - Exibe dados apenas após login
        def format_date(date):
            """Converte a data para um formato legível."""
            return date.strftime('%d-%m-%Y %H:%M:%S') if isinstance(date, datetime) else date

        def read_mongo(db_name, collection_name, query={}, projection=None):
            """
            Lê dados do MongoDB, converte a data para um formato legível e retorna um DataFrame do pandas.
            
            :param db_name: Nome do banco de dados.
            :param collection_name: Nome da coleção.
            :param query: Consulta a ser executada no MongoDB (padrão é {}).
            :param projection: Projeção para incluir/excluir campos (padrão é None).
            :return: DataFrame do pandas com os dados da consulta.
            """
            # Conectar ao MongoDB
            db = serve_name[db_name]
            collection = db[collection_name]

            # Consultar dados do MongoDB
            data = list(collection.find(query, projection))

            # Converter a data para um formato legível
            for item in data:
                if 'date_time' in item:
                    item['date_time'] = format_date(item['date_time'])

            # Transformar os dados em um DataFrame
            df = pd.DataFrame(data)
            return df

        # Função para verificar novos agendamentos
        def check_new_appointments(last_check_time):
            db = serve_name["Clientes"]
            collection = db["Barbearia"]
            
            # Consultar agendamentos após a última verificação
            new_appointments = list(collection.find({"date_time": {"$gt": last_check_time}}))
            
            if new_appointments:
                st.success(f"Novo(s) agendamento(s) encontrado(s): {len(new_appointments)}")
                st.balloons()
            
            return new_appointments

        # Página principal
        def main():
            st.title('Tabela de Serviços')
            st.write('Abaixo estão os detalhes dos serviços:')

            # Inicializa o tempo da última verificação
            if "last_check_time" not in st.session_state:
                st.session_state["last_check_time"] = datetime.now()

            while True:
                new_appointments = check_new_appointments(st.session_state["last_check_time"])
                if new_appointments:
                    st.session_state["last_check_time"] = datetime.now()
                    df = read_mongo(db_name="Clientes", collection_name="Barbearia", projection=projection)
                    st.write(df)

                time.sleep(10)  # Espera 10 minutos antes de verificar novamente
                st.experimental_rerun()  # Recarrega a aplicação

        # Exemplo de uso
        if __name__ == "__main__":
            projection = {
                '_id': 0,
                'name': 1,
                'date_time': 1,
                'cpf': 1,
                'services': 1,
                'total': 1
            }

            df = read_mongo(db_name="Clientes", collection_name="Barbearia", projection=projection)
            st.write(df)
            main()
    else:
        st.error("Nome de usuário ou senha incorretos. Tente novamente.")
