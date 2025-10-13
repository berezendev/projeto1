import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="I.A. Detetive", layout="centered")

st.title("🕵️‍♂️ I.A. Detetive")
st.write("Bem-vindo(a) ao **I.A. Detetive**, o jogo onde apenas os verdadeiros investigadores descobrem a verdade. A vítima foi encontrada... mas quem será o culpado?")

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

locais = [
    "na biblioteca da faculdade",
    "no estacionamento do fórum",
    "no plenário da câmara municipal",
    "no saguão do tribunal",
    "na cobertura de um prédio em Copacabana",
    "na sala do júri",
]

armas = [
    "um Vade Mecum de 8kg",
    "uma caneta tinteiro envenenada",
    "um grampeador pesado",
    "uma garrafa de café fervente",
    "um taco de sinuca",
]

motivos = [
    "por causa de uma disputa de herança",
    "por ciúmes profissionais",
    "porque perdeu uma ação judicial",
    "por puro tédio",
    "para encobrir um caso de corrupção",
]

# Inicialização de estado
if "crime" not in st.session_state:
    st.session_state.crime = None
if "tentativas" not in st.session_state:
    st.session_state.tentativas = 8
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "revelado" not in st.session_state:
    st.session_state.revelado = False

# Função para gerar um novo crime
def gerar_crime():
    return {
        "assassino": random.choice(pessoas),
        "vitima": random.choice(["Jair, o porteiro", "Fabíola, a juíza", "Tadeu, o vereador", "Matt, o influencer"]),
        "local": random.choice(locais),
        "arma": random.choice(armas),
        "motivo": random.choice(motivos),
    }

# Botão para gerar novo caso
if st.button("🔪 Gerar Novo Caso"):
    st.session_state.crime = gerar_crime()
    st.session_state.tentativas = 8
    st.session_state.mensagens = []
    st.session_state.revelado = False

# Se houver um caso ativo
if st.session_state.crime:
    crime = st.session_state.crime

    st.subheader("🩸 O CRIME")
    st.write(f"A vítima é **{crime['vitima']}**.")
    st.write("A polícia encontrou a cena do crime, mas as evidências ainda são inconclusivas. Cabe a você descobrir o culpado.")

    st.write(f"Tentativas restantes: **{st.session_state.tentativas}**")

    assassino = st.selectbox("Quem é o assassino?", [""] + pessoas)
    local = st.selectbox("Onde ocorreu o crime?", [""] + locais)
    arma = st.selectbox("Qual foi a arma do crime?", [""] + armas)

    if st.button("🔍 Fazer palpite"):
        if st.session_state.tentativas <= 0:
            st.warning("Suas tentativas acabaram! Revele o mistério abaixo.")
        elif not assassino or not local or not arma:
            st.warning("Preencha todas as opções antes de fazer um palpite.")
        else:
            st.session_state.tentativas -= 1
            acertos = 0
            if assassino == crime["assassino"]:
                acertos += 1
            if local == crime["local"]:
                acertos += 1
            if arma == crime["arma"]:
                acertos += 1

            if acertos == 3:
                st.success(
                    f"🎉 Você desvendou o caso! "
                    f"{crime['assassino']} matou {crime['vitima']} {crime['local']} com {crime['arma']}, {crime['motivo']}."
                )
                st.session_state.revelado = True
            else:
                msg = f"❌ Palpite errado. Você acertou **{acertos}** elemento(s) do crime."
                st.session_state.mensagens.append(msg)

    # Histórico dos palpites
    for msg in reversed(st.session_state.mensagens):
        st.write(msg)

    # Revelar o caso se acabar as tentativas
    if st.session_state.tentativas == 0 and not st.session_state.revelado:
        if st.button("🕯️ Revelar o mistério"):
            st.error(
                f"O verdadeiro assassino era **{crime['assassino']}**, "
                f"que matou **{crime['vitima']}** {crime['local']} com **{crime['arma']}**, {crime['motivo']}."
            )
else:
    st.info("Clique em **Gerar Novo Caso** para começar a investigação.")
