import streamlit as st

st.title('Meu programa')
st.write('Olá, mundo!')]

nome=st.text_input("Digite o seu nome")
if nome:
  st.write(nome.upper())


