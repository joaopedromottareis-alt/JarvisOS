import streamlit as st
import streamlit.components.v1 as components
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
# Tenta importar a biblioteca oficial da Groq Cloud
try:
    from groq import Groq
    groq_disponivel = True
except ImportError:
    groq_disponivel = False

def chamar_jarvis_ia(prompt_usuario):
    """Função para gerenciar chamadas de IA dinâmicas usando a API da Groq"""
    # Procura a chave de API nas variáveis de ambiente ou segredos do Streamlit
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
                {"role": "system", "content": f"Você é o Jarvis OS, um assistente operacional avançado e refinado. Responda ao usuário {st.session_state.username} de forma polida, prestativa e focada em produtividade."},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Falha na conexão neural com a rede Groq: {str(e)}"

# --- ESTILIZAÇÃO CSS AVANÇADA (Layout Expansivo de Tela Cheia) ---
estilos_css = """
<style>
    :root {
        --bg-main: #080705;
        --bg-card: #110e0a;
        --gold-primary: #d4af37;
        --gold-gradient: linear-gradient(135deg, #ffd700 0%, #b8860b 100%);
        --text-main: #ffffff;
        --text-muted: #8e8271;
        --border-color: #231c12;
    }

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: 'Montserrat', sans-serif;
    }

    body {
        background-color: var(--bg-main);
        color: var(--text-main);
        padding: 30px;
    }

    /* Layout do Painel Principal (Ocupa a Guia Toda) */
    .dashboard-container {
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
        background: radial-gradient(circle at center, #14100a 0%, #070604 100%);
        border: 2px solid var(--border-color);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }

    /* Cabeçalho Superior */
    .jarvis-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #231c12;
        padding-bottom: 25px;
        margin-bottom: 35px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 3px;
        background: var(--gold-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .status-pill {
        font-size: 11px;
        color: #ff4a4a;
        font-weight: 600;
        background: rgba(255, 74, 74, 0.1);
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid rgba(255, 74, 74, 0.2);
        letter-spacing: 1px;
    }

    /* Cartões e Containers de Conteúdo */
    .panel-card {
        background: linear-gradient(145deg, #16120d 0%, #0e0b08 100%);
        border: 1px solid #2d2314;
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .panel-title {
        font-size: 18px;
        color: var(--gold-primary);
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Orbe de IA Inteligente */
    .orbe-glow {
        width: 140px;
        height: 140px;
        background: radial-gradient(circle, rgba(212,175,55,0.15) 0%, transparent 70%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
    }

    .orbe-core {
        width: 60px;
        height: 60px;
        background: #080705;
        border-radius: 50%;
        border: 2px solid var(--gold-primary);
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.4);
    }

    /* Cronograma de Calendário Expandido Desktop */
    .grid-calendario {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 15px;
        margin-top: 20px;
    }

    .dia-semana {
        text-align: center;
        font-weight: 600;
        color: var(--text-muted);
        font-size: 13px;
        text-transform: uppercase;
    }

    .celula-dia {
        background: #0b0906;
        border: 1px solid #1f1910;
        border-radius: 12px;
        height: 100px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .celula-dia.hoje {
        border: 2px solid var(--gold-primary);
        background: #19140e;
    }

    .num-dia {
        font-weight: 700;
        color: #635747;
    }

    .celula-dia.hoje .num-dia {
        color: var(--gold-primary);
    }

    .evento-tag {
        background: rgba(212, 175, 55, 0.15);
        color: #fcefd2;
        border-left: 3px solid var(--gold-primary);
        padding: 4px 8px;
        font-size: 11px;
        border-radius: 4px;
        font-weight: 500;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""

# --- ETAPA DE AUTENTICAÇÃO / LOGIN ---
if not st.session_state.logged_in:
    # Exibição do Painel de Entrada Centralizado
    interface_login = f"""
    {estilos_css}
    <div class="dashboard-container" style="max-width: 600px; margin: 80px auto; text-align: center;">
        <header class="jarvis-header" style="justify-content: center; border-bottom: none;">
            <h1 class="brand-title">INICIALIZAR CORTEX</h1>
        </header>
        <p style="color: #8e8271; font-size: 14px; margin-bottom: 30px;">Identifique-se para descriptografar os módulos de produtividade.</p>
    </div>
    """
    components.html(interface_login, height=220)
    
    # Inputs nativos do Streamlit para controle preciso de dados e ações
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            input_user = st.text_input("Username / Operador", placeholder="Digite seu nome corporativo...")
            btn_entrar = st.button("Autenticar Conexão", use_container_width=True)
            
            if btn_entrar and input_user:
                st.session_state.username = input_user
                st.session_state.logged_in = True
                st.rerun()
else:
    # --- HUB OPERACIONAL PRINCIPAL (USUÁRIO LOGADO) ---
    
    # Cabeçalho Fixo do Sistema Operacional
    header_html = f"""
    {estilos_css}
    <div class="dashboard-container" style="padding-bottom: 10px; border-bottom-left-radius: 0; border-bottom-right-radius: 0;">
        <header class="jarvis-header" style="margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 12px; height: 12px; background: var(--gold-gradient); border-radius: 50%;"></div>
                <h1 class="brand-title">JARVIS OS CORE</h1>
            </div>
            <div style="display: flex; align-items: center; gap: 20px;">
                <span style="font-size: 13px; color: #8e8271;">Operador: <strong style="color: #fff;">{st.session_state.username}</strong></span>
                <div class="status-pill">SISTEMA CONECTADO</div>
            </div>
        </header>
    </div>
    """
    components.html(header_html, height=120)

    # Menu de Navegação Superior Integrado via Streamlit (Janelas completas separadas)
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
    with col_nav1:
        if st.button("🎛️ Painel de Gerenciamento", use_container_width=True):
            st.session_state.current_tab = "gerenciamento"
    with col_nav2:
        if st.button("🎯 Planejar Nova Meta", use_container_width=True):
            st.session_state.current_tab = "nova_meta"
    with col_nav3:
        if st.button("📅 Cronograma Mensal", use_container_width=True):
            st.session_state.current_tab = "calendario"
    with col_nav4:
        if st.button("⏳ Sessão de Foco", use_container_width=True):
            st.session_state.current_tab = "foco"

    st.markdown("<br>", unsafe_allow_html=True)

    # --- JANELA 1: GERENCIAMENTO (TELA CHEIA) ---
    if st.session_state.current_tab == "gerenciamento":
        html_gerenciamento = f"""
        {estilos_css}
        <div class="dashboard-container" style="border-top-left-radius: 0; border-top-right-radius: 0;">
            <div class="panel-card">
                <div class="panel-title">Relatório Semanal de Atividades</div>
                <p style="font-size: 14px; color: #c9beaf; line-height: 1.6; margin-bottom: 20px;">
                    Olá, <strong>{st.session_state.username}</strong>. Analisamos seus padrões de trabalho mais recentes. Atualmente, existem tarefas administrativas e relatórios estruturais aguardando sua validação final.
                </p>
                <div style="font-size: 12px; color: var(--text-muted); background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border: 1px solid #231c12; display: inline-block;">
                    Arquivos em Cache: Relatorio_Jan.zip, Documentos_Core.tar +3
                </div>
            </div>
        </div>
        """
        components.html(html_gerenciamento, height=280)
        
        # Área de interação com a IA da Groq Cloud
        st.markdown("### 🧠 Consultar Núcleo Cognitivo (Jarvis IA)")
        pergunta = st.text_input(f"Envie uma instrução operacional, {st.session_state.username}:", placeholder="Ex: Crie um sumário para o relatório de Janeiro...")
        if st.button("Transmitir Comando"):
            if pergunta:
                with st.spinner("Processando através dos clusters da Groq..."):
                    resposta_ia = chamar_jarvis_ia(pergunta)
                    st.info(resposta_ia)
            else:
                st.warning("Por favor, insira um comando válido antes de transmitir.")

    # --- JANELA 2: NOVA META (TELA CHEIA COM ORBE CENTRAL) ---
    elif st.session_state.current_tab == "nova_meta":
        html_meta = f"""
        {estilos_css}
        <div class="dashboard-container" style="border-top-left-radius: 0; border-top-right-radius: 0; text-align: center;">
            <div class="orbe-glow">
                <div class="orbe-core"></div>
            </div>
            <h2 style="font-weight: 500; margin-bottom: 30px; letter-spacing: 1px;">O que pretende planejar hoje, {st.session_state.username}?</h2>
        </div>
        """
        components.html(html_meta, height=280)
        
        with st.container():
            st.markdown("#### Configuração de Vetor de Meta")
            meta_txt = st.text_input("Definição do Objetivo Comercial / Acadêmico:")
            horario_meta = st.text_input("Janela Recomendada de Execução:", placeholder="Ex: 20:30 - Hoje")
            if st.button("Fixar Meta no Painel"):
                st.success(f"Meta mapeada com sucesso para o operador {st.session_state.username}!")

    # --- JANELA 3: CALENDÁRIO MENSAL MIGRADO DE DESKTOP ---
    elif st.session_state.current_tab == "calendario":
        # Montagem dinâmica do HTML do calendário em tamanho de tela cheia
        dias_semana_html = "".join(f'<div class="dia-semana">{d}</div>' for d in ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"])
        
        celulas_dias_html = ""
        # Offset inicial para alinhamento correto do calendário
        celulas_dias_html += "<div></div>" 
        
        for dia in range(1, 29):
            classe_hoje = "hoje" if dia == 15 else ""
            conteudo_evento = ""
            
            if dia == 19:
                conteudo_evento = '<div class="evento-tag">📅 Prova de Geografia</div>'
                
            celulas_dias_html += f"""
            <div class="celula-dia {classe_hoje}">
                <div class="num-dia">{dia}</div>
                {conteudo_evento}
            </div>
            """

        html_calendario = f"""
        {estilos_css}
        <div class="dashboard-container" style="border-top-left-radius: 0; border-top-right-radius: 0;">
            <h3 style="font-weight: 500; letter-spacing: 1px; margin-bottom: 25px; text-align: center;">VETOR DE CRONOGRAMA INTEGRADO</h3>
            <div class="grid-calendario">
                {dias_semana_html}
                {celulas_dias_html}
            </div>
        </div>
        """
        components.html(html_calendario, height=620)

    # --- JANELA 4: SESSÃO DE FOCO (POMODORO) ---
    elif st.session_state.current_tab == "foco":
        html_foco = f"""
        {estilos_css}
        <div class="dashboard-container" style="border-top-left-radius: 0; border-top-right-radius: 0; text-align: center; padding: 60px 40px;">
            <h3 style="font-weight: 600; letter-spacing: 1px; color: var(--text-muted);">MÓDULO DE PRODUTIVIDADE ISOLADA</h3>
            <div style="font-size: 84px; font-weight: 300; margin: 30px 0; background: var(--gold-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px;">
                25:00
            </div>
        </div>
        """
        components.html(html_foco, height=320)
        st.button("Disparar Fluxo de Concentração Alpha", use_container_width=True)
