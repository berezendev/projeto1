streamlit run advogadogpt_realista.py
import streamlit as st

st.set_page_config(page_title="AdvogadoGPT Realista", page_icon="⚖️")

st.title("⚖️ AdvogadoGPT Realista")
st.write("Seu assistente jurídico confiável (e ligeiramente sarcástico).")

duvida = st.text_input("Qual é sua dúvida jurídica?", placeholder="Ex: Posso ser preso por dever pensão?")

# Base de respostas simples
respostas = {
    "pensão": "Sim, pode. A prisão civil por dívida de pensão alimentícia é permitida no Brasil, pois o objetivo é forçar o pagamento, não punir. Mas claro, se pagar, sai. Milagre jurídico? Não, só coerção legítima.",
    "contrato": "Contratos valem como lei entre as partes. Se você assinou sem ler, o Direito não tem pena de ingênuos — apenas cláusulas abusivas podem ser anuladas.",
    "multa": "Multas devem respeitar o devido processo legal. Se o agente errou na autuação, você pode recorrer. Mas alegar 'não vi a placa' não é defesa, é confissão.",
    "divórcio": "Sim, pode se divorciar quando quiser. Desde 2010, o divórcio é direto, sem necessidade de separação prévia. O amor acabou? A papelada resolve.",
    "trabalho": "O empregado tem direito a férias, 13º e horas extras. Já o patrão tem direito a dor de cabeça se não pagar corretamente.",
    "injúria": "Ofender alguém é crime, mesmo pela internet. Liberdade de expressão não é salvo-conduto pra ser grosseiro.",
    "imposto": "Imposto é compulsório, não opcional. 'Não quero pagar' é um sentimento comum, mas juridicamente irrelevante.",
}

if st.button("Responder"):
    if not duvida.strip():
        st.warning("Digite sua dúvida primeiro.")
    else:
        resposta_encontrada = None
        for palavra, resposta in respostas.items():
            if palavra in duvida.lower():
                resposta_encontrada = resposta
                break
        
        if resposta_encontrada:
            st.success("Resposta do AdvogadoGPT:")
            st.write(resposta_encontrada)
        else:
            st.info("Não encontrei nada específico, mas lembre-se: o Google não é advogado, e o advogado não é o Google.")
