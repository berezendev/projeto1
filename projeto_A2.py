import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="Mapa Judicial Inteligente",
    page_icon="⚖️",
    layout="wide"
)

# Dados dos foros e varas (em produção, isso viria de um banco de dados)
FOROS_DATA = {
    "São Paulo": {
        "Foro Central": {
            "endereco": "Praça da Sé, 100 - Centro, São Paulo - SP",
            "telefone": "(11) 3105-6000",
            "horario_funcionamento": "08:00-18:00 (Seg-Sex)",
            "coordenadas": [-23.5505, -46.6333],
            "acessibilidade": True,
            "estacionamento": "Sim - Pago",
            "modalidade": "Híbrido",
            "varas": {
                "Vara Cível 15": {
                    "competencia": "Ações de indenização até R$ 100.000",
                    "juiz": "Dr. João Silva",
                    "contato": "(11) 3105-6015",
                    "email": "vara15@tjsp.jus.br",
                    "sistema_online": "PJe",
                    "link_sistema": "https://pje.tjsp.jus.br",
                    "horario_audiencia": "Segundas e quartas - 14h-18h",
                    "tempo_medio_tramitacao": "45 dias",
                    "avaliacao": 4.2
                },
                "Vara Criminal 8": {
                    "competencia": "Crimes contra o patrimônio",
                    "juiz": "Dra. Maria Santos",
                    "contato": "(11) 3105-6008",
                    "email": "vara8@tjsp.jus.br",
                    "sistema_online": "EPROC",
                    "link_sistema": "https://eproc.tjsp.jus.br",
                    "horario_audiencia": "Terças e quintas - 09h-12h",
                    "tempo_medio_tramitacao": "30 dias",
                    "avaliacao": 4.5
                }
            }
        },
        "Foro Regional Leste": {
            "endereco": "Av. Paes de Barros,  Pinto - São Paulo - SP",
            "telefone": "(11) 3396-7000",
            "horario_funcionamento": "08:00-17:00 (Seg-Sex)",
            "coordenadas": [-23.5400, -46.5900],
            "acessibilidade": True,
            "estacionamento": "Sim - Gratuito",
            "modalidade": "Digital",
            "varas": {
                "Vara do Trabalho 12": {
                    "competencia": "Ações trabalhistas em geral",
                    "juiz": "Dr. Pedro Oliveira",
                    "contato": "(11) 3396-7012",
                    "email": "vara12@trtsp.jus.br",
                    "sistema_online": "PJe-JT",
                    "link_sistema": "https://pje.jt.jus.br",
                    "horario_audiencia": "Quintas - 13h-17h",
                    "tempo_medio_tramitacao": "60 dias",
                    "avaliacao": 4.0
                }
            }
        }
    },
    "Rio de Janeiro": {
        "Foro Central RJ": {
            "endereco": "Av. Erasmo Braga, 115 - Centro, Rio de Janeiro - RJ",
            "telefone": "(21) 3133-4000",
            "horario_funcionamento": "09:00-18:00 (Seg-Sex)",
            "coordenadas": [-22.9068, -43.1729],
            "acessibilidade": True,
            "estacionamento": "Não",
            "modalidade": "Híbrido",
            "varas": {
                "Vara de Família 3": {
                    "competencia": "Divórcios e guarda de filhos",
                    "juiz": "Dra. Ana Costa",
                    "contato": "(21) 3133-4003",
                    "email": "vara3@tjrj.jus.br",
                    "sistema_online": "EPROC",
                    "link_sistema": "https://eproc.tjrj.jus.br",
                    "horario_audiencia": "Sextas - 08h-12h",
                    "tempo_medio_tramitacao": "90 dias",
                    "avaliacao": 4.3
                }
            }
        }
    }
}

# Função para criar mapa
def criar_mapa(foros, localizacao_usuario=None):
    if localizacao_usuario:
        mapa = folium.Map(location=localizacao_usuario, zoom_start=12)
    else:
        mapa = folium.Map(location=[-23.5505, -46.6333], zoom_start=10)
    
    for estado, foros_estado in foros.items():
        for foro_nome, foro_info in foros_estado.items():
            # Cor baseada na modalidade
            if foro_info['modalidade'] == 'Digital':
                cor = 'green'
            elif foro_info['modalidade'] == 'Presencial':
                cor = 'red'
            else:  # Híbrido
                cor = 'blue'
            
            popup_text = f"""
            <b>{foro_nome}</b><br>
            <b>Modalidade:</b> {foro_info['modalidade']}<br>
            <b>Endereço:</b> {foro_info['endereco']}<br>
            <b>Telefone:</b> {foro_info['telefone']}<br>
            <b>Acessibilidade:</b> {'Sim' if foro_info['acessibilidade'] else 'Não'}
            """
            
            folium.Marker(
                foro_info['coordenadas'],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=foro_nome,
                icon=folium.Icon(color=cor, icon='scale-balanced', prefix='fa')
            ).add_to(mapa)
    
    return mapa

# Interface principal
st.title("🏛️ Mapa Judicial Inteligente")
st.markdown("Encontre foros, varas e informações para atuação presencial e digital")

# Sidebar para filtros
with st.sidebar:
    st.header("🔍 Filtros de Busca")
    
    estado_selecionado = st.selectbox(
        "Selecione o Estado:",
        list(FOROS_DATA.keys())
    )
    
    tipo_acao = st.selectbox(
        "Tipo de Ação:",
        ["Selecione...", "Cível", "Criminal", "Trabalhista", "Família", "Consumidor"]
    )
    
    modalidade = st.radio(
        "Modalidade Preferida:",
        ["Todas", "Presencial", "Digital", "Híbrido"]
    )
    
    usar_localizacao = st.checkbox("Usar minha localização atual")

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Mapa", "📋 Foros e Varas", "💻 Processos Online", "📊 Estatísticas"])

with tab1:
    st.header("Mapa Interativo dos Foros")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if usar_localizacao:
            # Em produção, isso usaria geolocalização real
            localizacao_usuario = [-23.5505, -46.6333]
            st.info("📍 Localização: São Paulo (exemplo)")
        else:
            localizacao_usuario = None
        
        mapa = criar_mapa({estado_selecionado: FOROS_DATA[estado_selecionado]}, localizacao_usuario)
        folium_static(mapa, width=700, height=500)
    
    with col2:
        st.subheader("Legenda do Mapa")
        st.markdown("""
        <div style='background-color: green; color: white; padding: 5px; margin: 2px; border-radius: 3px;'>
        🟢 Digital - Processos majoritariamente online
        </div>
        <div style='background-color: blue; color: white; padding: 5px; margin: 2px; border-radius: 3px;'>
        🔵 Híbrido - Presencial e digital
        </div>
        <div style='background-color: red; color: white; padding: 5px; margin: 2px; border-radius: 3px;'>
        🔴 Presencial - Atendimento físico
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Dicas Rápidas")
        st.info("""
        💡 **Clique nos marcadores** para ver detalhes
        💡 **Cores indicam** a modalidade predominante
        💡 **Use os filtros** para refinar sua busca
        """)

with tab2:
    st.header("Lista Detalhada de Foros e Varas")
    
    for foro_nome, foro_info in FOROS_DATA[estado_selecionado].items():
        with st.expander(f"🏛️ {foro_nome} - {foro_info['modalidade']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📞 Informações de Contato")
                st.write(f"**Endereço:** {foro_info['endereco']}")
                st.write(f"**Telefone:** {foro_info['telefone']}")
                st.write(f"**Horário:** {foro_info['horario_funcionamento']}")
                st.write(f"**Acessibilidade:** {'✅ Sim' if foro_info['acessibilidade'] else '❌ Não'}")
                st.write(f"**Estacionamento:** {foro_info['estacionamento']}")
            
            with col2:
                st.subheader("⚖️ Varas Disponíveis")
                for vara_nome, vara_info in foro_info['varas'].items():
                    with st.expander(f"📋 {vara_nome}"):
                        st.write(f"**Competência:** {vara_info['competencia']}")
                        st.write(f"**Juiz:** {vara_info['juiz']}")
                        st.write(f"**Contato:** {vara_info['contato']}")
                        st.write(f"**Avaliação:** ⭐ {vara_info['avaliacao']}/5.0")
                        
                        if modalidade == "Todas" or modalidade == foro_info['modalidade']:
                            st.write(f"**Tempo médio:** {vara_info['tempo_medio_tramitacao']}")

with tab3:
    st.header("💻 Portal de Processos Online")
    
    st.info("""
    ⚡ **Acesso rápido aos sistemas digitais** dos tribunais. 
    Encontre links diretos, tutoriais e suporte técnico.
    """)
    
    # Filtro por sistema
    sistemas = set()
    for foro_info in FOROS_DATA[estado_selecionado].values():
        for vara_info in foro_info['varas'].values():
            sistemas.add(vara_info['sistema_online'])
    
    sistema_selecionado = st.selectbox("Sistema Online:", ["Todos"] + list(sistemas))
    
    st.subheader("📋 Varas com Atendimento Digital")
    
    for foro_nome, foro_info in FOROS_DATA[estado_selecionado].items():
        if foro_info['modalidade'] in ['Digital', 'Híbrido']:
            for vara_nome, vara_info in foro_info['varas'].items():
                if sistema_selecionado == "Todos" or vara_info['sistema_online'] == sistema_selecionado:
                    with st.expander(f"🔗 {vara_nome} - {foro_nome}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Sistema:** {vara_info['sistema_online']}")
                            st.write(f"**Email:** {vara_info['email']}")
                            st.write(f"**Contato:** {vara_info['contato']}")
                            
                            if st.button(f"Acessar {vara_info['sistema_online']}", key=f"btn_{vara_nome}"):
                                st.markdown(f"[🔗 Clique aqui para acessar]({vara_info['link_sistema']})")
                        
                        with col2:
                            st.write("**📊 Estatísticas Digitais**")
                            st.write(f"**Tempo médio digital:** {vara_info['tempo_medio_tramitacao']}")
                            st.write(f"**Avaliação do sistema:** ⭐ {vara_info['avaliacao']}/5.0")
                            
                            # Simulação de status do sistema
                            status = "✅ Online" if vara_info['avaliacao'] > 4.0 else "🟡 Instável"
                            st.write(f"**Status:** {status}")

with tab4:
    st.header("📊 Estatísticas e Análises")
    
    # Dados para gráficos
    dados_estatisticos = []
    for estado, foros_estado in FOROS_DATA.items():
        for foro_nome, foro_info in foros_estado.items():
            for vara_nome, vara_info in foro_info['varas'].items():
                dados_estatisticos.append({
                    'Estado': estado,
                    'Foro': foro_nome,
                    'Vara': vara_nome,
                    'Modalidade': foro_info['modalidade'],
                    'Sistema': vara_info['sistema_online'],
                    'Avaliacao': vara_info['avaliacao'],
                    'Tempo_Medio': int(vara_info['tempo_medio_tramitacao'].split()[0])
                })
    
    df = pd.DataFrame(dados_estatisticos)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Distribuição por Modalidade")
        modalidade_count = df['Modalidade'].value_counts()
        st.bar_chart(modalidade_count)
        
        st.subheader("⚖️ Tempo Médio por Sistema")
        tempo_medio = df.groupby('Sistema')['Tempo_Medio'].mean()
        st.bar_chart(tempo_medio)
    
    with col2:
        st.subheader("⭐ Avaliação Média por Estado")
        avaliacao_media = df.groupby('Estado')['Avaliacao'].mean()
        st.bar_chart(avaliacao_media)
        
        st.subheader("🔧 Sistemas Mais Utilizados")
        sistema_count = df['Sistema'].value_counts()
        st.bar_chart(sistema_count)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>⚖️ <b>Mapa Judicial Inteligente</b> - Facilitando o acesso à justiça presencial e digital</p>
    <p><small>Desenvolvido para a disciplina de Programação para Advogados</small></p>
</div>
""", unsafe_allow_html=True)
