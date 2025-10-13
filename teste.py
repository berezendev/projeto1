import streamlit as st
import random

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(page_title="I.A. Detetive", layout="centered")

st.title("🕵️ I.A. Detetive — O Jogo")
st.write("""
Descubra o criminoso, o local e a arma do crime!  
Mas atenção: você tem **8 tentativas** para resolver o caso antes que o culpado fuja.  
Use sua intuição... e um pouco de sorte.
""")

# ==============================
# BASE DE DADOS
# ==============================
pessoas = [
    "Dona Gertrudes, a vizinha fofoqueira",
    "Dr. Campos, o advogado",
    "Capitão Ramos, o militar aposentado",
    "Clara, a estudante de Direito",
    "Ricardo, o estagiário do fórum",
    "Padre Bento, o pároco",
    "Helena, a professora de Filosofia",
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

# ==============================
# INICIALIZAÇÃO DO JOGO
# ==============================
if "caso" not in st.session_state:
    st.session_state.caso = {
        "autor": random.choice(pessoas),
        "local": random.choice(locais),
        "arma": random.choice(armas),
        "motivo": random.choice(motivos),
    }
    st.session_state.tentativas = 8
    st.session_state.encerrado = False
    st.session_state.venceu = False

# ==============================
# INTERFACE
# ==============================
st.subheader("🔍 Faça suas escolhas:")

autor_escolhido = st.selectbox("Quem cometeu o crime?", pessoas)
local_escolhido = st.selectbox("Onde o crime aconteceu?", locais)
arma_escolhida = st.selectbox("Com qual arma?", armas)

# ==============================
# LÓGICA DO JOGO
# ==============================
if st.button("Investigar 🔪") and not st.session_state.encerrado:
    correto = st.session_state.caso
    acertos = []

    if autor_escolhido == correto["autor"]:
        acertos.append("autor")
    if local_escolhido == correto["local"]:
        acertos.append("local")
    if arma_escolhida == correto["arma"]:
        acertos.append("arma")

    if len(acertos) == 3:
        st.success("🎉 Parabéns, detetive! Você desvendou o crime!")
        st.markdown(f"""
**Resumo do caso resolvido:**
O(a) culpado(a) era **{correto['autor']}**,  
que cometeu o crime **{correto['local']}**,  
**{correto['arma']}**,  
**{correto['motivo']}**.
""")
        st.session_state.venceu = True
        st.session_state.encerrado = True
    else:
        st.session_state.tentativas -= 1
        if st.session_state.tentativas > 0:
            dicas = {
                0: "Nenhuma pista certa ainda, tente observar melhor as conexões...",
                1: "Você acertou **uma** das opções!",
                2: "Você acertou **duas** das opções! Está perto!",
            }
            st.warning(
                f"❌ Ainda não foi dessa vez. {dicas.get(len(acertos), '')}\n\n"
                f"Tentativas restantes: **{st.session_state.tentativas}**"
            )
        else:
            st.error("💀 O culpado fugiu! O caso foi encerrado.")
            st.markdown(f"""
**Solução do caso:**
O(a) verdadeiro(a) assassino(a) era **{correto['autor']}**,  
no local **{correto['local']}**,  
**{correto['arma']}**,  
**{correto['motivo']}**.
""")
            st.session_state.encerrado = True

# ==============================
# REINICIAR JOGO
# ==============================
if st.session_state.encerrado:
    if st.button("Jogar Novamente 🔁"):
        st.session_state.caso = {
            "autor": random.choice(pessoas),
            "local": random.choice(locais),
            "arma": random.choice(armas),
            "motivo": random.choice(motivos),
        }
        st.session_state.tentativas = 8
        st.session_state.encerrado = False
        st.session_state.venceu = False
        st.experimental_rerun()
