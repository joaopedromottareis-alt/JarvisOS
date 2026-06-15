import streamlit as st
import datetime
import time
import json
import os
import hashlib
import re
import calendar as pycalendar
from groq import Groq

# ==================== NÚCLEO DE CONFIGURAÇÃO ====================
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY and "GROQ_API_KEY" in st.secrets:
    API_KEY = st.secrets["GROQ_API_KEY"]

try:
    client = Groq(api_key=API_KEY) if API_KEY else None
except:
    client = None

MODELO_PRINCIPAL = "llama-3.3-70b-versatile" 
MODELO_EXTRATOR = "llama-3.3-70b-versatile"
LOGO_PATH = "logo.png"

# ==================== INTERFACE ADAPTATIVA (CSS AVANÇADO) ====================
st.set_page_config(page_title="Jarvis OS | Command Center", page_icon="🔱", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700&family=Space+Grotesk:wght@300;400;700&display=swap');
    
    /* Fundo imersivo com padrão de grade tática */
    .stApp { 
        background-color: #030303 !important; 
        color: #e0e0e0 !important; 
        font-family: 'Space Grotesk', sans-serif !important;
        background-image: 
            radial-gradient(circle at 2px 2px, rgba(212, 175, 55, 0.05) 1px, transparent 0),
            radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.1) 0%, transparent 50%) !important;
        background-size: 40px 40px, 100% 100% !important;
    }

    /* Esconder elementos padrão do Streamlit */
    [data-testid="stSidebarCollapsedControl"], [data-testid="stHeader"], footer { display: none !important; }
    .block-container { padding: 1.5rem 2rem !important; max-width: 95% !important; }

    /* Containers estilo Glassmorphism (Visto no Slide) */
    .glass-card {
        background: rgba(15, 15, 15, 0.6) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border: 1px solid rgba(212, 175, 55, 0.4);
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.1);
    }

    /* Títulos e Gradientes */
    .glitch-title {
        font-family: 'Kanit', sans-serif;
        background: linear-gradient(135deg, #fff 30%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .system-label {
        color: #d4af37;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        margin-bottom: 5px;
        display: block;
    }

    /* Input Styling */
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Botão Jarvis */
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important;
        color: black !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        border: none !important;
        width: 100%;
        border-radius: 8px !important;
        letter-spacing: 1px;
    }

    /* Ajuste de abas para o novo design */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.1);
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        color: #888;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(212, 175, 55, 0.15) !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== ÍCONES SVG ====================
ICONES = {
    "terminal": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>""",
    "vitals": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>""",
    "foco": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""
}

# ==================== LÓGICA DE USUÁRIO ====================
ARQUIVO_CONFIG_USERS = "usuarios_config.json"

def carregar_credenciais():
    if os.path.exists(ARQUIVO_CONFIG_USERS):
        with open(ARQUIVO_CONFIG_USERS, "r") as f: return json.load(f)["usernames"]
    return {"admin": {"name": "ADMIN", "password": hashlib.sha256("admin123".encode()).hexdigest()}}

usernames_db = carregar_credenciais()

if "autenticado" not in st.session_state: st.session_state.autenticado = False

# --- TELA DE ACESSO ---
if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        with st.container():
            st.markdown("<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
            if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=100)
            st.markdown("<h2 class='glitch-title'>Acessar Jarvis OS</h2>", unsafe_allow_html=True)
            user = st.text_input("Credencial de Operador").lower()
            pw = st.text_input("Código de Segurança", type="password")
            if st.button("Iniciar Protocolo"):
                if user in usernames_db and hashlib.sha256(pw.encode()).hexdigest() == usernames_db[user]["password"]:
                    st.session_state.autenticado = True
                    st.session_state.username = user
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================== DASHBOARD ADAPTATIVO ====================
username = st.session_state.username
name = usernames_db[username]["name"]
ARQUIVO_DADOS = f"dados_user_{username}.json"

def load_data():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as f: return json.load(f)
    return {"metas": [], "agua": 0, "peso": 70.0, "pomo": 0, "eventos": []}

db = load_data()

# --- HEADER TÁTICO ---
col_logo, col_stat1, col_stat2, col_stat3, col_out = st.columns([0.8, 1, 1, 1, 0.8])
with col_logo:
    if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=50)
with col_stat1:
    st.markdown(f"<span class='system-label'>IA SYNC</span><span style='color:#00ff88;'>● ONLINE</span>", unsafe_allow_html=True)
with col_stat2:
    st.markdown(f"<span class='system-label'>USER</span><span style='color:white;'>{name}</span>", unsafe_allow_html=True)
with col_stat3:
    st.markdown(f"<span class='system-label'>OS VERSION</span><span style='color:#d4af37;'>MK-IV NEXT</span>", unsafe_allow_html=True)
with col_out:
    if st.button("LOGOUT"):
        st.session_state.autenticado = False
        st.rerun()

st.markdown("<hr style='border: 0.5px solid rgba(212,175,55,0.2); margin-top:0;'>", unsafe_allow_html=True)

# --- GRID CENTRAL (Bento Box Productive Style) ---
main_l, main_r = st.columns([1.8, 1.2])

with main_l:
    # Módulo de Comando (Chat)
    st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='system-label'>{ICONES['terminal']} Terminal de Comando</span>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Protocolos ativos, {name}. Aguardando diretrizes."}]
    
    chat_box = st.container(height=350)
    for m in st.session_state.messages:
        chat_box.chat_message(m["role"]).write(m["content"])
        
    if prompt := st.chat_input("Insira comando tático..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Lógica simplificada de resposta (Jarvis Persona)
        if client:
            res = client.chat.completions.create(
                model=MODELO_PRINCIPAL,
                messages=[{"role":"system","content":"Você é o Jarvis MK-IV. Responda de forma curta, técnica e elegante."},{"role":"user","content":prompt}]
            ).choices[0].message.content
        else: res = "Erro de conexão com o núcleo neural."
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Módulo de Objetivos Ativos (Lista Rápida)
    st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='system-label'>Diretrizes Prioritárias</span>", unsafe_allow_html=True)
    if not db["metas"]: st.info("Nenhuma diretriz ativa.")
    else:
        for i, meta in enumerate(db["metas"][:3]): # Mostra as 3 primeiras
            st.markdown(f"➢ **{meta['nome']}** <span style='float:right; color:#d4af37;'>{meta['tempo_dedicado']}min</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with main_r:
    # Módulo de Foco (Pomodoro)
    st.markdown(f"<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown(f"<span class='system-label'>{ICONES['foco']} Ciclo de Concentração</span>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size:50px; margin:10px 0;'>25:00</h1>", unsafe_allow_html=True)
    st.button("Iniciar Ciclo")
    st.markdown("</div>", unsafe_allow_html=True)

    # Módulo de Hidratação (Vitals)
    st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='system-label'>{ICONES['vitals']} Nível de Hidratação</span>", unsafe_allow_html=True)
    progresso = min(db["agua"] / 2500, 1.0)
    st.progress(progresso)
    st.markdown(f"<small>{db['agua']}ml de 2500ml</small>", unsafe_allow_html=True)
    if st.button("Catalogar 250ml"):
        db["agua"] += 250
        with open(ARQUIVO_DADOS, "w") as f: json.dump(db, f)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Módulo de Agenda Rápida
    st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='system-label'>Cronograma Hoje</span>", unsafe_allow_html=True)
    st.markdown("<small>• 14:00 - Reunião Stark</small><br><small>• 17:00 - Análise de Dados</small>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ABAS PARA DETALHES ---
st.markdown("<br>", unsafe_allow_html=True)
aba1, aba2 = st.tabs(["HISTÓRICO COMPLETO", "CONFIGURAÇÕES DE SISTEMA"])

with aba1:
    st.write("Aqui você pode colocar as tabelas e gráficos que já tínhamos, mas em uma aba separada para não poluir o cockpit principal.")

with aba2:
    st.write("Ajuste de peso, troca de senha e calibração de IA.")
