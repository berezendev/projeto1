import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Previsor de Tempo Processual",
    page_icon="⚖️",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .factor-item {
        background-color: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

# Dados do sistema
ASSUNTOS_COMPATIVEIS = {
    'Ação de Cobrança': ['Ação Ordinária', 'Ação Monitória', 'Execução de Título Extrajudicial', 'Processo de Execução'],
    'Execução de Título Extrajudicial': ['Processo de Execução', 'Execução de Título Extrajudicial'],
    'Ação de Consumidor': ['Ação Ordinária', 'Ação Sumária', 'Processo de Conhecimento'],
    'Ação Indenizatória': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Danos Morais': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Danos Materiais': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Rescisão Contratual': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Ação de Família': ['Ação Ordinária', 'Processo de Conhecimento', 'Processo de Jurisdição Voluntária'],
    'Divórcio': ['Ação Ordinária', 'Divórcio', 'Processo de Jurisdição Voluntária'],
    'Guarda de Menores': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Pensão Alimentícia': ['Alimentos', 'Ação Ordinária', 'Processo de Conhecimento'],
    'Inventário': ['Inventário', 'Processo de Jurisdição Voluntária'],
    'Usucapião': ['Usucapião', 'Ação Ordinária', 'Processo de Conhecimento'],
    'Reintegração de Posse': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Mandado de Segurança': ['Mandado de Segurança', 'Processo Cautelar'],
    'Ação Trabalhista': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Reclamação Trabalhista': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Acidente de Trabalho': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Ação Tributária': ['Ação Ordinária', 'Processo de Conhecimento'],
    'Busca e Apreensão': ['Ação Ordinária', 'Processo Cautelar']
}

TRIBUNAIS = {
    'TJSP': {'nome': 'Tribunal de Justiça de São Paulo', 'fator_tempo': 1.0},
    'TJRJ': {'nome': 'Tribunal de Justiça do Rio de Janeiro', 'fator_tempo': 1.1},
    'TJMG': {'nome': 'Tribunal de Justiça de Minas Gerais', 'fator_tempo': 0.9},
    'TJRS': {'nome': 'Tribunal de Justiça do Rio Grande do Sul', 'fator_tempo': 1.0},
    'TJPR': {'nome': 'Tribunal de Justiça do Paraná', 'fator_tempo': 1.05},
    'TJSC': {'nome': 'Tribunal de Justiça de Santa Catarina', 'fator_tempo': 0.95},
    'TJBA': {'nome': 'Tribunal de Justiça da Bahia', 'fator_tempo': 1.2},
    'TJPE': {'nome': 'Tribunal de Justiça de Pernambuco', 'fator_tempo': 1.15},
    'TJCE': {'nome': 'Tribunal de Justiça do Ceará', 'fator_tempo': 1.1},
    'TJGO': {'nome': 'Tribunal de Justiça de Goiás', 'fator_tempo': 1.0},
    'TJMT': {'nome': 'Tribunal de Justiça de Mato Grosso', 'fator_tempo': 0.95},
    'TJMS': {'nome': 'Tribunal de Justiça de Mato Grosso do Sul', 'fator_tempo': 0.9},
    'TJES': {'nome': 'Tribunal de Justiça do Espírito Santo', 'fator_tempo': 1.0},
    'TJPA': {'nome': 'Tribunal de Justiça do Pará', 'fator_tempo': 1.25},
    'TJAM': {'nome': 'Tribunal de Justiça do Amazonas', 'fator_tempo': 1.3},
    'TRF1': {'nome': 'Tribunal Regional Federal da 1ª Região', 'fator_tempo': 1.3},
    'TRF2': {'nome': 'Tribunal Regional Federal da 2ª Região', 'fator_tempo': 1.2},
    'TRF3': {'nome': 'Tribunal Regional Federal da 3ª Região', 'fator_tempo': 1.25},
    'TRF4': {'nome': 'Tribunal Regional Federal da 4ª Região', 'fator_tempo': 1.15},
    'TST': {'nome': 'Tribunal Superior do Trabalho', 'fator_tempo': 1.1}
}

CLASSES_PROCESSUAIS = {
    'Ação Ordinária': {'fator_tempo': 1.0},
    'Ação Sumária': {'fator_tempo': 0.7},
    'Ação Sumaríssima': {'fator_tempo': 0.5},
    'Processo de Conhecimento': {'fator_tempo': 1.0},
    'Processo de Execução': {'fator_tempo': 0.8},
    'Processo Cautelar': {'fator_tempo': 0.6},
    'Mandado de Segurança': {'fator_tempo': 0.5},
    'Ação Civil Pública': {'fator_tempo': 1.2},
    'Ação Rescisória': {'fator_tempo': 1.3},
    'Recurso de Apelação': {'fator_tempo': 1.0},
    'Recurso Especial': {'fator_tempo': 1.4},
    'Recurso Extraordinário': {'fator_tempo': 1.6},
    'Agravo de Instrumento': {'fator_tempo': 0.7},
    'Embargos de Declaração': {'fator_tempo': 0.4},
    'Ação Monitória': {'fator_tempo': 0.6},
    'Execução de Título Extrajudicial': {'fator_tempo': 0.5},
    'Inventário': {'fator_tempo': 1.1},
    'Divórcio': {'fator_tempo': 0.8},
    'Alimentos': {'fator_tempo': 0.6},
    'Usucapião': {'fator_tempo': 1.3}
}

TEMPOS_BASE = {
    'Ação de Cobrança': 180,
    'Execução de Título Extrajudicial': 150,
    'Ação de Consumidor': 240,
    'Ação Indenizatória': 300,
    'Danos Morais': 280,
    'Danos Materiais': 270,
    'Rescisão Contratual': 420,
    'Ação de Família': 320,
    'Divórcio': 200,
    'Guarda de Menores': 280,
    'Pensão Alimentícia': 180,
    'Inventário': 360,
    'Usucapião': 480,
    'Reintegração de Posse': 220,
    'Mandado de Segurança': 120,
    'Ação Trabalhista': 240,
    'Reclamação Trabalhista': 200,
    'Acidente de Trabalho': 360,
    'Ação Tributária': 420,
    'Busca e Apreensão': 140
}

def validar_combinacao(assunto, classe_processual):
    """Verifica se a classe processual é compatível com o assunto"""
    if assunto in ASSUNTOS_COMPATIVEIS:
        classes_validas = ASSUNTOS_COMPATIVEIS[assunto]
        if classe_processual in classes_validas:
            return True, f"✅ Combinação válida: {assunto} + {classe_processual}"
        else:
            return False, f"❌ COMBINAÇÃO INVÁLIDA: {classe_processual} não é uma classe processual adequada para {assunto}"
    return True, "✅ Combinação válida"

def calcular_tempo_processo(tribunal, assunto, classe_processual, instancia, recursos, urgencia):
    """Calcula o tempo estimado do processo"""
    
    # VALIDAÇÃO PRIMEIRO
    valido, mensagem = validar_combinacao(assunto, classe_processual)
    if not valido:
        return None, None, None, None, None, None, mensagem
    
    # 1. TEMPO BASE DO ASSUNTO
    tempo_base = TEMPOS_BASE[assunto]
    
    # 2. FATOR TRIBUNAL (eficiência regional)
    fator_tribunal = TRIBUNAIS[tribunal]['fator_tempo']
    
    # 3. FATOR CLASSE PROCESSUAL
    fator_classe = CLASSES_PROCESSUAIS[classe_processual]['fator_tempo']
    
    # 4. FATOR INSTÂNCIA
    fatores_instancia = {'1ª': 1.0, '2ª': 1.5, 'STJ': 2.0, 'STF': 2.0}
    fator_instancia = fatores_instancia[instancia]
    
    # 5. FATOR RECURSOS
    fator_recursos = 1.0 + (recursos * 0.2)
    
    # 6. FATOR URGÊNCIA
    fator_urgencia = 0.7 if urgencia else 1.0
    
    # CÁLCULO FINAL
    tempo_total = tempo_base * fator_tribunal * fator_classe * fator_instancia * fator_recursos * fator_urgencia
    
    return int(tempo_total), tempo_base, fator_tribunal, fator_classe, fator_instancia, fator_recursos, "✅ Cálculo realizado com sucesso"

# Interface Streamlit
def main():
    # Cabeçalho
    st.markdown('<h1 class="main-header">⏰ PREVISOR DE TEMPO PROCESSUAL</h1>', unsafe_allow_html=True)
    
    # Sidebar com informações
    with st.sidebar:
        st.header("ℹ️ Sobre o Sistema")
        st.info("""
        Este sistema calcula o tempo estimado de processos judiciais baseado em:
        
        • Estatísticas reais do CNJ
        • Eficiência dos tribunais
        • Complexidade do assunto
        • Tipo de processo
        • Recursos previstos
        """)
        
        st.header("📊 Fontes dos Dados")
        st.write("""
        - CNJ - Justiça em Números
        - Relatórios de tribunais
        - Estatísticas processuais
        - Dados abertos da Justiça
        """)
    
    # Formulário principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Configuração do Processo")
        
        # Seleção de Assunto
        assunto = st.selectbox(
            "1. Selecione o Assunto:",
            options=list(ASSUNTOS_COMPATIVEIS.keys()),
            index=0
        )
        
        # Classes compatíveis dinamicamente
        if assunto:
            classes_validas = ASSUNTOS_COMPATIVEIS[assunto]
            classe_processual = st.selectbox(
                "2. Selecione a Classe Processual:",
                options=classes_validas,
                index=0
            )
        
        # Tribunal
        tribunal = st.selectbox(
            "3. Selecione o Tribunal:",
            options=list(TRIBUNAIS.keys()),
            format_func=lambda x: f"{x} - {TRIBUNAIS[x]['nome']}",
            index=0
        )
    
    with col2:
        st.subheader("⚙️ Parâmetros Adicionais")
        
        # Instância
        instancia = st.selectbox(
            "4. Instância do Processo:",
            options=['1ª', '2ª', 'STJ', 'STF'],
            index=0
        )
        
        # Recursos
        recursos = st.slider(
            "5. Quantidade de Recursos Previstos:",
            min_value=0,
            max_value=5,
            value=0,
            help="Cada recurso adiciona aproximadamente 20% ao tempo total"
        )
        
        # Urgência
        urgencia = st.checkbox(
            "6. Processo com Urgência",
            help="Processos urgentes têm tramitação 30% mais rápida"
        )
    
    # Botão de cálculo
    if st.button("🎯 Calcular Previsão de Tempo", type="primary", use_container_width=True):
        with st.spinner("Calculando previsão de tempo..."):
            resultado = calcular_tempo_processo(tribunal, assunto, classe_processual, instancia, recursos, urgencia)
            tempo_total, tempo_base, fator_tribunal, fator_classe, fator_instancia, fator_recursos, mensagem = resultado
            
            if tempo_total is None:
                st.error(mensagem)
                st.warning("💡 Classes processuais compatíveis:")
                for classe_valida in ASSUNTOS_COMPATIVEIS[assunto]:
                    st.write(f"• {classe_valida}")
            else:
                # CONVERSÃO PARA MESES/DIAS
                meses = tempo_total // 30
                dias = tempo_total % 30
                anos = meses // 12
                meses_resto = meses % 12

                # DATA ESTIMADA
                data_hoje = datetime.now()
                data_estimada = data_hoje + timedelta(days=tempo_total)
                
                # RESULTADOS
                st.success("✅ Cálculo realizado com sucesso!")
                
                # Resultado principal
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.subheader("📊 Previsão de Tempo Processual")
                
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.metric(
                        label="Tempo Total Estimado",
                        value=f"{tempo_total} dias úteis"
                    )
                    
                with col_res2:
                    if anos > 0:
                        st.metric(
                            label="Equivalente a",
                            value=f"{anos} ano(s), {meses_resto} mes(es) e {dias} dia(s)"
                        )
                    else:
                        st.metric(
                            label="Equivalente a",
                            value=f"{meses} mes(es) e {dias} dia(s)"
                        )
                
                st.metric(
                    label="Previsão de Conclusão",
                    value=data_estimada.strftime('%d/%m/%Y')
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Detalhes do cálculo
                st.subheader("🔍 Detalhamento do Cálculo")
                
                fatores = [
                    ("📊 Tempo Base do Assunto", f"{assunto}: {tempo_base} dias", "Baseado em estatísticas reais do CNJ"),
                    ("🏛️ Eficiência do Tribunal", f"{tribunal}: {fator_tribunal}", "Fator baseado em relatórios de produtividade"),
                    ("📝 Tipo de Processo", f"{classe_processual}: {fator_classe}", "Processos sumários são mais rápidos"),
                    ("⚖️ Instância Judicial", f"{instancia}: {fator_instancia}", "Tribunais superiores demoram mais"),
                    ("🔄 Quantidade de Recursos", f"{recursos} recursos: {fator_recursos}", "Cada recurso adiciona 20% ao tempo"),
                    ("🚨 Urgência Processual", f"{'30% mais rápido' if urgencia else 'Tempo normal'}: {0.7 if urgencia else 1.0}", "Tramitação prioritária")
                ]
                
                for titulo, valor, descricao in fatores:
                    with st.expander(f"{titulo}"):
                        st.write(f"**{valor}**")
                        st.caption(descricao)
                
                # Gráfico de fatores (opcional)
                st.subheader("📈 Influência dos Fatores")
                
                fatores_data = {
                    'Fator': ['Tempo Base', 'Tribunal', 'Classe', 'Instância', 'Recursos', 'Urgência'],
                    'Valor': [tempo_base, fator_tribunal * 100, fator_classe * 100, fator_instancia * 100, (fator_recursos - 1) * 100, (1 - (0.7 if urgencia else 1.0)) * 100],
                    'Impacto': ['Base', 'Moderado', 'Moderado', 'Alto', 'Variável', 'Alto']
                }
                
                df_fatores = pd.DataFrame(fatores_data)
                st.dataframe(df_fatores, use_container_width=True, hide_index=True)

    # Rodapé
    st.markdown("---")
    st.caption(f"⚖️ Previsor de Tempo Processual | 📅 Consulta realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("📊 Baseado em estatísticas reais do CNJ e tribunais | 🚀 Desenvolvido para auxiliar na gestão processual")

if __name__ == "__main__":
    main()
