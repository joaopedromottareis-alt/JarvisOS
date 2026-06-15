import streamlit as st
import os

# 1. CONFIGURAÇÃO PREMIUM DA PÁGINA STREAMLIT
st.set_page_config(
    page_title="Jarvis OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialização das variáveis de estado do ecossistema
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "gerenciamento"

# --- BACKEND INTEGRAÇÃO DE INTELIGÊNCIA ARTIFICIAL (GROQ) ---
try:
    from groq import Groq
    groq_disponivel = True
except ImportError:
    groq_disponivel = False

def chamar_jarvis_ia(prompt_usuario):
    """Função para gerenciar chamadas de IA dinâmicas usando a API da Groq"""
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)
    
    if not groq_disponivel:
        return "Erro do Sistema: Biblioteca 'groq' não encontrada. Instale usando 'pip install groq'."
    if not api_key:
        return "Modo Offline: Configure a chave 'GROQ_API_KEY' no seu ambiente para ativar as respostas cognitivas do Jarvis."
    
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"Você é o Jarvis OS, um assistente operacional avançado e refinado. Responda ao usuário {st.session_state.username} de forma polida, prestativa e focada em produtividade e saúde de alta performance. Seja direto."},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Falha na conexão neural com a rede Groq: {str(e)}"

# --- ESTILIZAÇÃO GLOBAL (CSS injetado para unificar o layout) ---
st.markdown("""
<style>
    /* Reset e Variáveis de Design */
    :root {
        --bg-main: #080705;
        --bg-card: #110e0a;
        --gold-primary: #d4af37;
        --gold-gradient: linear-gradient(135deg, #ffd700 0%, #b8860b 100%);
        --text-main: #ffffff;
        --text-muted: #8e8271;
        --border-color: #231c12;
    }

    /* Modificando containers nativos do Streamlit para evitar divisões feias */
    .stApp {
        background-color: #080705 !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }

    /* Estilos das Janelas e Paineis Uniformes */
    .jarvis-container {
        width: 100%;
        background: linear-gradient(145deg, #120e09 0%, #070604 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 35px;
        margin-bottom: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    }

    .jarvis-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #231c12;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }

    .brand-title {
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #ffd700 0%, #b8860b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .status-pill {
        font-size: 11px;
        color: #ffd700;
        font-weight: 600;
        background: rgba(212, 175, 55, 0.1);
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        letter-spacing: 1px;
    }

    .panel-title {
        font-size: 18px;
        color: var(--gold-primary);
        font-weight: 600;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }

    /* Orbe de IA */
    .orbe-glow {
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(212,175,55,0.12) 0%, transparent 70%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 10px auto 20px auto;
    }

    .orbe-core {
        width: 50px;
        height: 50px;
        background: #080705;
        border-radius: 50%;
        border: 2px solid var(--gold-primary);
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }

    /* Grid do Calendário Desktop Completo */
    .grid-calendario {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 12px;
        margin-top: 15px;
    }

    .dia-semana {
        text-align: center;
        font-weight: 600;
        color: var(--text-muted);
        font-size: 12px;
        text-transform: uppercase;
    }

    .celula-dia {
        background: #0b0906;
        border: 1px solid #1f1910;
        border-radius: 10px;
        height: 95px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .celula-dia.hoje {
        border: 1px solid var(--gold-primary);
        background: #16120d;
    }

    .num-dia {
        font-weight: 700;
        color: #524738;
    }

    .celula-dia.hoje .num-dia {
        color: var(--gold-primary);
    }

    .evento-tag {
        background: rgba(212, 175, 55, 0.1);
        color: #f2e3c6;
        border-left: 2px solid var(--gold-primary);
        padding: 3px 6px;
        font-size: 10px;
        border-radius: 3px;
    }

    /* Customizações extras para inputs nativos parecerem premium */
    .stTextInput>div>div>input {
        background-color: #0d0a07 !important;
        color: #ffffff !important;
        border: 1px solid #231c12 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ETAPA DE LOGIN ---
if not st.session_state.logged_in:
    st.markdown("""
    <div class="jarvis-container" style="max-width: 550px; margin: 60px auto; text-align: center;">
        <div class="brand-title" style="margin-bottom: 10px;">INICIALIZAR CORTEX</div>
        <p style="color: #8e8271; font-size: 13px;">Identifique-se para descriptografar os módulos operacionais.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        input_user = st.text_input("Operador / Username", placeholder="Digite seu login...", key="login_username")
        if st.button("Autenticar Conexão", use_container_width=True):
            if input_user:
                st.session_state.username = input_user
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Por favor, digite um username válido.")

else:
    # --- HUB OPERACIONAL PRINCIPAL (TELA UNIFICADA) ---
    
    # Cabeçalho Superior Dinâmico com Nome do Usuário Logado
    st.markdown(f"""
    <div class="jarvis-container" style="padding-bottom: 15px; margin-bottom: 15px;">
        <div class="jarvis-header" style="margin-bottom: 0; border-bottom: none; padding-bottom: 0;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 8px; height: 8px; background: var(--gold-gradient); border-radius: 50%;"></div>
                <div class="brand-title">JARVIS OS CORE</div>
            </div>
            <div style="display: flex; align-items: center; gap: 20px;">
                <span style="font-size: 13px; color: #8e8271;">Operador: <strong style="color: #fff;">{st.session_state.username}</strong></span>
                <div class="status-pill">SISTEMA CONECTADO</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Menu de Janelas Únicas (Substituído emojis por Labels com Design Uniforme)
    col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)
    with col_nav1:
        if st.button("Painel de Controle", use_container_width=True):
            st.session_state.current_tab = "gerenciamento"
    with col_nav2:
        if st.button("Planejar Metas", use_container_width=True):
            st.session_state.current_tab = "nova_meta"
    with col_nav3:
        if st.button("Cronograma", use_container_width=True):
            st.session_state.current_tab = "calendario"
    with col_nav4:
        if st.button("Sessão Foco", use_container_width=True):
            st.session_state.current_tab = "foco"
    with col_nav5:
        if st.button("Sinais Vitais / Saúde", use_container_width=True):
            st.session_state.current_tab = "saude"

    st.markdown("<hr style='border-color: #1f1910; margin: 10px 0 25px 0;'>", unsafe_allow_html=True)

    # --- JANELA 1: GERENCIAMENTO ---
    if st.session_state.current_tab == "gerenciamento":
        st.markdown(f"""
        <div class="jarvis-container">
            <div class="panel-title">Relatório Semanal de Atividades</div>
            <p style="font-size: 14px; color: #c9beaf; line-height: 1.6; margin-bottom: 15px;">
                Olá, <strong>{st.session_state.username}</strong>. Mapeamos os seus parâmetros operacionais mais recentes. Existem pendências estruturais prontas para sua triagem e aprovação de relatórios.
            </p>
            <div style="font-size: 11px; color: #8e8271; background: #0b0906; padding: 10px; border-radius: 6px; border: 1px solid #231c12; display: inline-block;">
                Módulos Locais carregados com sucesso.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🧠 Consultar Núcleo Cognitivo (Jarvis IA)")
        pergunta = st.text_input(f"Instrua o Cortex, {st.session_state.username}:", placeholder="Ex: Prepare os tópicos essenciais para o planejamento estratégico...")
        if st.button("Transmitir Comando"):
            if pergunta:
                with st.spinner("Conectando aos clusters de processamento Groq..."):
                    resposta_ia = chamar_jarvis_ia(pergunta)
                    st.info(resposta_ia)

    # --- JANELA 2: NOVA META ---
    elif st.session_state.current_tab == "nova_meta":
        st.markdown(f"""
        <div class="jarvis-container" style="text-align: center;">
            <div class="orbe-glow"><div class="orbe-core"></div></div>
            <div class="panel-title" style="margin-bottom: 5px;">Direcionamento Estratégico</div>
            <p style="color: #8e8271; font-size: 14px;">O que pretende arquitetar e organizar hoje, {st.session_state.username}?</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            meta_txt = st.text_input("Definição clara do Objetivo Principal:")
            horario_meta = st.text_input("Prazo ou Janela sugerida:", placeholder="Ex: Até as 18:00 - Hoje")
            if st.button("Fixar Meta Operacional"):
                st.success(f"Objetivo devidamente registrado sob a custódia do operador {st.session_state.username}.")

    # --- JANELA 3: CRONOGRAMA ---
    elif st.session_state.current_tab == "calendario":
        dias_semana_html = "".join(f'<div class="dia-semana">{d}</div>' for d in ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"])
        celulas_dias_html = "<div></div>"  # Alinhamento
        
        for dia in range(1, 29):
            classe_hoje = "hoje" if dia == 15 else ""
            conteudo_evento = '<div class="evento-tag">Prova de Geografia</div>' if dia == 19 else ""
            celulas_dias_html += f"""
            <div class="celula-dia {classe_hoje}">
                <div class="num-dia">{dia}</div>
                {conteudo_evento}
            </div>
            """

        st.markdown(f"""
        <div class="jarvis-container">
            <div class="panel-title" style="text-align: center; margin-bottom: 20px;">Linha do Tempo e Agendamentos</div>
            <div class="grid-calendario">
                {dias_semana_html}
                {celulas_dias_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- JANELA 4: SESSÃO FOCO ---
    elif st.session_state.current_tab == "foco":
        st.markdown("""
        <div class="jarvis-container" style="text-align: center; padding: 50px 20px;">
            <div class="panel-title" style="color: #8e8271; font-size: 12px; letter-spacing: 2px;">MÓDULO DE ISOLAMENTO COGNITIVO</div>
            <div style="font-size: 72px; font-weight: 300; margin: 20px 0; background: linear-gradient(135deg, #ffd700 0%, #b8860b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px;">
                25:00
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Iniciar Ciclo de Concentração", use_container_width=True)

    # --- JANELA 5: MÓDULO SAÚDE (RESTAURADO E UNIFICADO) ---
    elif st.session_state.current_tab == "saude":
        st.markdown(f"""
        <div class="jarvis-container">
            <div class="panel-title">Módulo de Bio-Performance & Saúde</div>
            <p style="font-size: 14px; color: #c9beaf; margin-bottom: 25px;">
                Gerenciamento de energia física e foco do operador <strong>{st.session_state.username}</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Grid interno limpo e nativo para métricas de saúde
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric(label="Consumo Hidrológico", value="1.8 L", delta="Meta: 3.0 L")
        with col_s2:
            st.metric(label="Descanso Concluído", value="7h 45m", delta="Qualidade Ótima")
        with col_s3:
            st.metric(label="Rendimento Físico Diário", value="84%", delta="Estável")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Sincronizar Dispositivos Biométricos", use_container_width=True)
