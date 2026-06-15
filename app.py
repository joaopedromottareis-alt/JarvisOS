import streamlit as st
import datetime
import time
import json
import os
import hashlib
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
LOGO_PATH = "logo.png"

# ==================== CODIFICAÇÃO DA INTERFACE HUD STARK ====================
st.set_page_config(page_title="JARVIS OS | HUD SYSTEM", page_icon="🔱", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Rajdhani:wght@500;600;700&display=swap');
    
    /* Reset e Fundo Cibernético */
    .stApp { 
        background-color: #020408 !important; 
        color: #00f0ff !important; 
        font-family: 'Rajdhani', sans-serif !important;
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px),
            radial-gradient(circle at 50% 50%, #050e1e 0%, #010408 100%) !important;
        background-size: 30px 30px, 30px 30px, 100% 100% !important;
        background-attachment: fixed !important;
    }

    [data-testid="stSidebarCollapsedControl"], [data-testid="stHeader"], footer { display: none !important; }
    .block-container { padding: 1rem 1.5rem !important; max-width: 98% !important; }

    /* Módulos Holográficos (Efeito Idêntico à Imagem) */
    .hud-box {
        background: rgba(4, 12, 24, 0.65) !important;
        backdrop-filter: blur(15px);
        border: 1px solid #00f0ff;
        border-radius: 4px;
        padding: 18px;
        margin-bottom: 15px;
        position: relative;
        box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.1), 0 4px 20px rgba(0,0,0,0.6);
    }
    
    /* Cantoneiras Estilo Interface Militar/Ficção Científica */
    .hud-box::before {
        content: ''; position: absolute; top: -1px; left: -1px; width: 10px; height: 10px;
        border-top: 2px solid #d4af37; border-left: 2px solid #d4af37;
    }
    .hud-box::after {
        content: ''; position: absolute; bottom: -1px; right: -1px; width: 10px; height: 10px;
        border-bottom: 2px solid #d4af37; border-right: 2px solid #d4af37;
    }

    /* Tipografia Avançada */
    .hud-header {
        font-family: 'Orbitron', sans-serif;
        color: #fff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .gold-glow {
        color: #d4af37 !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }

    /* Input e Formulários HUD */
    .stTextInput>div>div>input {
        background: rgba(0, 240, 255, 0.03) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        color: #fff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 16px !important;
        border-radius: 2px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.2) !important;
    }

    /* Botões Interativos */
    .stButton>button {
        background: transparent !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 11px !important;
        letter-spacing: 2px;
        font-weight: 600 !important;
        text-transform: uppercase;
        width: 100%;
        border-radius: 2px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        color: #fff !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    }

    /* Elementos Estilizados */
    .progress-bar-fill {
        height: 6px; background: #00f0ff;
        box-shadow: 0 0 10px #00f0ff;
        border-radius: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SISTEMA DE SEGURANÇA E ARQUIVOS ====================
ARQUIVO_CONFIG_USERS = "usuarios_config.json"

def carregar_usuarios():
    if os.path.exists(ARQUIVO_CONFIG_USERS):
        with open(ARQUIVO_CONFIG_USERS, "r") as f: return json.load(f)["usernames"]
    return {"admin": {"name": "DIRETOR", "password": hashlib.sha256("admin123".encode()).hexdigest()}}

usernames_db = carregar_usuarios()

if "autenticado" not in st.session_state: st.session_state.autenticado = False

# --- COMPONENTE DE LOGIN MILITAR ---
if not st.session_state.autenticado:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1.2, 1])
    with login_col:
        st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
        if os.path.exists(LOGO_PATH): 
            st.image(LOGO_PATH, width=80)
        st.markdown("<div class='hud-header'>SISTEMA AUTENTICADOR</div>", unsafe_allow_html=True)
        operador = st.text_input("ID OPERADOR").lower()
        chave = st.text_input("CHAVE CRIPTOGRÁFICA", type="password")
        if st.button("DESBLOQUEAR TERMINAL"):
            if operador in usernames_db and hashlib.sha256(chave.encode()).hexdigest() == usernames_db[operador]["password"]:
                st.session_state.autenticado = True
                st.session_state.username = operador
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================== OPERAÇÃO INTEGRADA COCKPIT ====================
username = st.session_state.username
name = usernames_db[username]["name"]
ARQUIVO_DADOS = f"dados_user_{username}.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as f: return json.load(f)
    return {"metas": [{"nome": "Mapeamento Quântico", "tempo_dedicado": 15}], "agua": 500, "eventos": []}

db = carregar_dados()

# --- BARRA DE STATUS SUPERIOR (HUD HEADER) ---
st.markdown(f"""
    <div style='display: grid; grid-template-columns: 1fr 2fr 1fr; align-items: center; border-bottom: 1px solid rgba(0, 240, 255, 0.3); padding-bottom: 8px; margin-bottom: 20px;'>
        <div style='font-family: "Orbitron"; font-size: 18px; font-weight: 800; letter-spacing: 2px;'>
            JARVIS <span style='color: #d4af37;'>OS</span>
        </div>
        <div style='text-align: center; font-size: 13px; letter-spacing: 4px; color: rgba(0, 240, 255, 0.7);'>
            SISTEMA CORE: <span style='color: #fff;'>SYS_ACTIVE</span> | OPERADOR: <span style='color: #d4af37;'>{name}</span>
        </div>
        <div style='text-align: right; font-family: "Orbitron"; font-size: 12px; color: #ff3b3b;'>
            SEC_LEVEL_04
        </div>
    </div>
""", unsafe_allow_html=True)

# --- GRID TÁTICO TRIDIMENSIONAL (BENTO BOX APEX) ---
col_esquerda, col_direita = st.columns([1.9, 1.1])

with col_esquerda:
    # Bloco Central: Terminal Neural (Chat Inteligente)
    st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-header'>[⚡] NÚCLEO COGNITIVO COMANDO DE VOZ / TEXTO</div>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Aguardando coordenadas estratégicas, {name}."}]
        
    chat_container = st.container(height=360)
    for m in st.session_state.messages:
        chat_container.chat_message(m["role"]).write(m["content"])
        
    if comando := st.chat_input("Injetar dados de telemetria..."):
        st.session_state.messages.append({"role": "user", "content": comando})
        if client:
            try:
                resposta_ia = client.chat.completions.create(
                    model=MODELO_PRINCIPAL,
                    messages=[{"role": "system", "content": "Você é o Jarvis OS, um computador de bordo tático avançado. Dê respostas curtas, precisas e militares."}, {"role": "user", "content": comando}]
                ).choices[0].message.content
            except:
                resposta_ia = "Falha no feedback do link neural."
        else:
            resposta_ia = "Link Groq offline. Execute em ambiente simulado."
        st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Bloco Inferior Esquerdo: Diretrizes Ativas (Tabela Tática)
    st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-header'>[⚙] ANÁLISE DE DIRETRIZES EM EXECUÇÃO</div>", unsafe_allow_html=True)
    for m in db["metas"]:
        st.markdown(f"""
            <div style='display: flex; justify-content: space-between; border-bottom: 1px solid rgba(0, 240, 255, 0.1); padding: 6px 0;'>
                <span>➢ {m['nome']}</span>
                <span class='gold-glow'>{m['tempo_dedicado']} MIN REPETIDOS</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_direita:
    # Bloco Superior Direito: Ciclo de Foco (Contador Holográfico)
    st.markdown("<div class='hud-box' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-header' style='justify-content: center;'>[⏱] CONTAGEM REGRESSIVA CRÍTICA</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family: \"Orbitron\", sans-serif; font-size: 55px; color: #fff; text-shadow: 0 0 20px #00f0ff; margin: 5px 0;'>25:00</h2>", unsafe_allow_html=True)
    st.button("ENGAJAR CRONÔMETRO")
    st.markdown("</div>", unsafe_allow_html=True)

    # Bloco Intermediário Direito: Consumo de Fluidos (Vitals)
    st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
    st.markdown("<div class='hud-header'>[💧] NÍVEIS OTIMIZADOS BIOMÉTRICOS</div>", unsafe_allow_html=True)
    st.markdown(f"Consumo de H2O: **{db['agua']} ml** / <span style='color:#777;'>2500 ml</span>", unsafe_allow_html=True)
    st.markdown("<div style='background: rgba(0, 240, 255, 0.1); border: 1px solid #00f0ff; height: 8px; border-radius: 4px; margin: 10px 0;'><div class='progress-bar-fill' style='width: 20%;'></div></div>", unsafe_allow_html=True)
    if st.button("INJETAR 250ML"):
        db["agua"] += 250
        with open(ARQUIVO_DADOS, "w") as f: json.dump(db, f)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Bloco Inferior Direito: Logo do Dono integrada perfeitamente sem fundo
    if os.path.exists(LOGO_PATH):
        st.markdown("<div class='hud-box' style='text-align: center; display: flex; justify-content: center; align-items: center; background: rgba(212,175,55,0.03) !important; border-color: rgba(212,175,55,0.3);'>", unsafe_allow_html=True)
        st.image(LOGO_PATH, width=90)
        st.markdown("</div>", unsafe_allow_html=True)

# Rodapé Técnico de Operações
st.markdown("<div style='text-align: center; font-size: 11px; color: rgba(0, 240, 255, 0.4); margin-top: 20px;'>JARVIS CORE ENGINE - PROTÓTIPO DE EXECUÇÃO DE ALTA PERMANÊNCIA</div>", unsafe_allow_html=True)
