import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="I.A. Detetive",layout="centered")

st.title(" I.A. Detetive")
st.write("Bem-vindo(a) ao simulador de casos criminais mais misterioso da internet. Clique no botão abaixo e descubra o próximo crime a ser desvendado!")

# Listas de possibilidades
pessoas = [
    "Dona Gertrudes, a vizinha fofoqueira",
    "Dr. Campos, o advogado",
    "Capitão Ramos, o militar aposentado",
    "Clara, a estudante de Direito",
    "Ricardo, o estagiário do fórum",
    "Padre Bento, o pároco",
    "Helena, a professora de Filosofia",
]

vitimas = [
    "Jair, o porteito do prédio",
    "Fabíola, a juíza",
    "Tadeu, o vereador",
    "Robson, o segurança do tribunal",
    "Matt, o influencer",
    "Roberto, o corretor de imóveis",
]

locais = [
    "na biblioteca da faculdade",
    "no estacionamento do fórum",
    "no plenário da câmara municipal",
    "no saguão do tribunal",
    "na cobertura de um prédio em Copacabana",
    "na sala do júri",
]

armas = [
    "com um Vade Mecum de 8kg",
    "com uma caneta tinteiro envenenada",
    "com um grampeador pesado",
    "com uma garrafa de café fervente",
    "com um taco de sinuca",
]

motivos = [
    "por causa de uma disputa de herança",
    "por ciúmes profissionais",
    "porque perdeu uma ação judicial",
    "por puro tédio",
    "para encobrir um caso de corrupção",
]

# Função para gerar o caso
def gerar_caso():
    autor = random.choice(pessoas)
    vitima = random.choice(vitimas)
    local = random.choice(locais)
    arma = random.choice(armas)
    motivo = random.choice(motivos)

    caso = f"""
**CASO GERADO:**

O(a) suspeito(a) **{autor}** teria assassinado **{vitima}** {local},  
**{arma}**, **{motivo}**.

Agora cabe a você, detetive, descobrir se há provas, álibi e o verdadeiro culpado...

🔎 *O mistério está lançado!*
"""
    return caso

# Botão
if st.button("Gerar Novo Caso 🔪"):
    st.markdown(gerar_caso())
else:
    st.info("Clique no botão acima para gerar um novo caso misterioso!")
