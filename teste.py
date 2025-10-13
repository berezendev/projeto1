import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="I.A. Detetive",layout="centered")

st.title(" I.A. Detetive")
st.write("Bem-vindo(a) ao simulador de casos criminais mais misterioso da internet. Clique no botão abaixo e descubra o próximo crime a ser desvendado!")

# Listas de possibilidades
pessoas = [
    "Dona Gertrudes, a vizinha fofoqueira",
    "Sr. Almeida, o advogado aposentado",
    "Capitão Ramos, o militar reformado",
    "Clara, a estudante de Direito",
    "Ricardo, o estagiário do fórum",
    "Padre Bento, o pároco local",
    "Helena, a professora de Filosofia",
]

vitimas = [
    "o síndico do prédio",
    "a juíza da comarca",
    "um vereador influente",
    "o segurança do tribunal",
    "um influenciador jurídico",
    "o professor de Processo Penal",
    "um corretor de imóveis",
]

locais = [
    "na biblioteca da faculdade",
    "no estacionamento do fórum",
    "no plenário da câmara municipal",
    "no saguão do tribunal",
    "na cobertura de um prédio em Copacabana",
    "na sala do júri",
    "no cartório às escuras",
]

armas = [
    "com um código civil de 2kg",
    "com uma caneta tinteiro envenenada",
    "com um grampeador pesado",
    "com um exemplar de 'O Capital'",
    "com uma garrafa de café fervente",
    "com o próprio diploma de Direito",
    "com um taco de sinuca",
]

motivos = [
    "por vingança acadêmica",
    "por causa de uma disputa de herança",
    "por ciúmes profissionais",
    "porque perdeu uma ação judicial",
    "por puro tédio jurídico",
    "para encobrir um caso de corrupção",
    "por um erro de petição mal redigida",
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
