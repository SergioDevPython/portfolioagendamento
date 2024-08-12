
import streamlit as st
from pymongo import MongoClient 
import pandas as pd
import datetime
from PIL import Image


serve_name = st.secrets["service_name"]
data_base = st.secrets["db"]
collection = st.secrets["col"]


st.set_page_config(
    page_icon=":clipboard",
    page_title="Barber Family",
)



st.title('BarberApp - :blue[Agendamentos] ' )


# Função para verificar a disponibilidade do horário
def is_slot_available(date, time):
    date_time = datetime.datetime.combine(date, time)
    count = collection.count_documents({'date_time': date_time})
    return count < 3

# Função para salvar o agendamento no MongoDB
def save_appointment(name, cpf, date, time, services, total):
    date_time = datetime.datetime.combine(date, time)
    collection.insert_one({
        'name': name,
        'cpf': cpf,
        'date_time': date_time,
        'services': services,
        'total': total
    })

# Função para obter os agendamentos
def get_appointments():
    appointments = collection.find({}, {'_id': 0, 'name': 1, 'date_time': 1})
    return list(appointments)

# Função para buscar agendamentos pelo CPF
def get_appointments_by_cpf(last_four_digits):
    regex = f'.*{last_four_digits}$'
    appointments = collection.find({'cpf': {'$regex': regex}}, {'_id': 0, 'name': 1, 'date_time': 1})
    return list(appointments)

# Lista de serviços e seus preços
services_list = {
    'Corte com máquina R$:10.00': 10.00,
    'Corte com máquina e TesouraR$:15.00': 15.00,
    'Corte Degradê R$:25.00': 25.00,
    'Barba Normal R$:10.00': 10.00,
    'Barboterapia R$:15.00': 15.00,
    'Barboterapia com máscara R$:30.00': 30.00,
    'Sombracelha R$:5.00': 5.00,
    'Luzes R$:30.00': 30.00,
    'Platinado R$:60.00': 60.00,
    'Pintura R$:20.00': 20.00,
    'Progressiva R$:40.00': 40.00,
    'Relaxamento R$:20.00': 20.00
}


# Formulário de agendamento
name = st.text_input('Digite seu nome:')
prof = st.selectbox('Escolha o profissional', ["Profissional 1", "Profissional 2", "Profissional 3"])  
date = st.date_input('Data:', datetime.date.today())
time = st.time_input('Hora:', datetime.time(9, 0))
selected_services = st.multiselect('Selecione os serviços:', list(services_list.keys()))

# Calcular o total dos serviços selecionados
total = sum(services_list[service] for service in selected_services)

if st.button('Verificar disponibilidade + Valor total'):
    
    if is_slot_available(date, time, ):
        st.success(f'Horário disponível! O valor total dos serviços é R$ {total} Reais  Para confirmar clique em Agendar')
    
    else:
        st.error('Este horário já está cheio. Por favor, escolha outro horário.')

if st.button('Agendar'):
    if is_slot_available(date, time):
        save_appointment(name, prof, date, time, selected_services, total)
        st.success('Agendamento realizado com sucesso!')
        st.balloons()
    else:
        st.error('Este horário já está cheio. Por favor, escolha outro horário.')
