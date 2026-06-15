import streamlit as st
import datetime
import time
import json
import os
import hashlib
import re
import calendar as pycalendar
from groq import Groq

# ==================== CONFIGURAÇÃO DA IA ====================
API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY and "GROQ_API_KEY" in st.secrets:
    API_KEY = st.secrets["GROQ_API_KEY"]

client = None
if API_KEY:
    try:
        client = Groq(api_key=API_KEY)
    except Exception:
        client = None

MODELO_PRINCIPAL = "llama-3.3-70b-versatile" 
MODELO_EXTRATOR = "llama-3.3-70b-versatile"

# ==================== CONFIGURAÇÃO VISUAL JAVIS APEX ====================
st.set_page_config(page_title="Jarvis OS", page_icon="🔱", layout="wide", initial_sidebar_state="collapsed")

# Dicionário de Ícones SVG com o gradiente dourado executivo original
ICONES = {
    "jarvis": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="50%" stop-color="#f3e5ab"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-.4 4.25l-7.07 4.42c-.32.2-.74.2-1.06 0L4.4 8.25c-.27-.17-.4-.49-.31-.8.09-.31.35-.53.67-.53h14.48c.32 0 .58.22.67.53.09.31-.04.63-.31.8z" fill="url(#gold-grad)"/><path d="M12 14.25c-.34 0-.67-.09-.96-.26L3.1 9.05V18c0 .55.45 1 1 1h15.8c.55 0 1-.45 1-1V9.05l-7.94 4.94c-.29.17-.62.26-.96.26z" fill="url(#gold-grad)"/><circle cx="12" cy="11.5" r="1.5" fill="url(#gold-grad)"/></svg>""",
    "conversa": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z" fill="url(#gold-grad)"/></svg>""",
    "foco": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z" fill="url(#gold-grad)"/></svg>""",
    "saude": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.5 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35zM10.5 7.5H9v2H7.5v1.5H9v2h1.5v-2H12v-1.5h-1.5v-2zm6 1.5h-3v1.5h3V9z" fill="url(#gold-grad)"/></svg>""",
    "calendario": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z" fill="url(#gold-grad)"/></svg>""",
    "estatisticas": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="url(#gold-grad)"/></svg>"""
}

# CSS customizado baseado no estilo Premium Glass Card dos slides do usuário
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp { 
        background-color: #030303 !important; 
        color: #e5e5e5 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-image: 
            radial-gradient(circle at 50% -20%, rgba(212, 175, 55, 0.08) 0%, transparent 60%),
            radial-gradient(circle at 90% 80%, rgba(184, 134, 11, 0.02) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
    }
    
    [data-testid="stSidebarCollapsedControl"], [data-testid="stSidebar"], #MainMenu, footer, header {
        display: none !important;
    }
    
    .block-container { 
        padding: 1.5rem 2rem !important; 
        max-width: 98% !important; 
    }
    
    /* Bento Box Grid Containers (Glassmorphism de alta produtividade) */
    .bento-card {
        background: rgba(13, 13, 13, 0.65) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    .custom-title {
        font-family: 'Kanit', sans-serif !important;
        background: linear-gradient(135deg, #ffffff 40%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important; 
        letter-spacing: -0.5px !important;
        margin-bottom: 15px !important;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .jarvis-brand {
        background: linear-gradient(45deg, #d4af37, #f3e5ab, #aa7c11);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    .stTextInput input, .stDateInput input, .stTextArea textarea, div[data-baseweb="select"], div[role="button"], .stTimeInput input {
        background-color: #0b0b0b !important; 
        border: 1px solid rgba(212, 175, 55, 0.15) !important; 
        border-radius: 10px !important; 
        color: #ffffff !important;
        padding: 8px 14px !important;
    }

    .titulo-card { 
        color: #d4af37 !important; 
        font-family: 'Kanit', sans-serif !important;
        font-size: 13px !important; 
        font-weight: 600 !important; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.15) !important;
        padding-bottom: 6px;
    }

    .stButton>button { 
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important; 
        color: #000000 !important; 
        border: none !important;
        border-radius: 10px !important; 
        padding: 8px 16px !important; 
        font-weight: 700 !important; 
        width: 100% !important;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 0.5px;
    }
    
    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        border-bottom: 1px solid rgba(212, 175, 55, 0.15) !important;
        margin-bottom: 15px !important;
    }
    
    .stTabs [data-baseweb="tab"] { 
        color: #777777 !important; 
        font-family: 'Kanit', sans-serif !important;
        padding: 8px 16px !important;
    }
    
    .stTabs [aria-selected="true"] { 
        color: #d4af37 !important; 
        background-color: rgba(212, 175, 55, 0.05) !important;
    }
    
    [data-testid="stChatMessage"] {
        background-color: rgba(15, 15, 15, 0.6) !important;
        border-left: 3px solid #d4af37 !important;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== GERENCIADOR DE USUÁRIOS ====================
ARQUIVO_CONFIG_USERS = "usuarios_config.json"

def gerar_hash_sha256(senha_texto):
    return hashlib.sha256(senha_texto.encode('utf-8')).hexdigest()

def carregar_credenciais_salvas():
    if os.path.exists(ARQUIVO_CONFIG_USERS):
        with open(ARQUIVO_CONFIG_USERS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if "usernames" in dados: return dados["usernames"]
            return dados
    return {"admin": {"name": "SENHOR ADMIN", "password": gerar_hash_sha256("admin123")}}

def salvar_novas_credenciais(dicionario_usernames):
    with open(ARQUIVO_CONFIG_USERS, "w", encoding="utf-8") as f:
        json.dump({"usernames": dicionario_usernames}, f, indent=4, ensure_ascii=False)

usernames_db = carregar_credenciais_salvas()

if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "username" not in st.session_state: st.session_state.username = None

# --- TELA DE LOGIN ORIGINAL ---
if not st.session_state.autenticado:
    header_html = f"<h2 class='custom-title'>{ICONES['jarvis']} ENTRAR NO <span class='jarvis-brand'>JARVIS OS</span></h2>"
    st.markdown(header_html, unsafe_allow_html=True)
    modo_tela = st.radio("SELECIONE A OPERAÇÃO:", ["LOGIN", "REGISTRAR NOVA CONTA"], horizontal=True)
    
    if modo_tela == "LOGIN":
        st.markdown("### LOGIN DO OPERADOR")
        input_user = st.text_input("USERNAME:", key="login_username").strip().lower()
        input_senha = st.text_input("SENHA DE SEGURANÇA:", type="password", key="login_password")
        
        if st.button("ACESSAR PAINEL PRINCIPAL"):
            if input_user in usernames_db:
                hash_informado = gerar_hash_sha256(input_senha)
                hash_salvo = usernames_db[input_user]["password"]
                if hash_informado == hash_salvo or input_senha == hash_salvo:
                    st.session_state.autenticado = True
                    st.session_state.username = input_user
                    st.rerun()
                else: st.error("CHAVE INCORRETA.")
            else: st.error("OPERADOR NÃO ENCONTRADO.")
        st.stop()
            
    elif modo_tela == "REGISTRAR NOVA CONTA":
        st.markdown("### CRIAR NOVA CONTA")
        novo_nome = st.text_input("COMO O JARVIS DEVE TE CHAMAR?")
        novo_user = st.text_input("USERNAME (SEM ESPAÇOS):").strip().lower()
        nova_senha = st.text_input("SENHA DE SEGURANÇA:", type="password")
        confirmar_senha = st.text_input("CONFIRME A SENHA:", type="password")
        
        if st.button("FINALIZAR CADASTRO"):
            if not novo_nome or not novo_user or not nova_senha: st.error("Preencha tudo.")
            elif novo_user in usernames_db: st.error("Username já existe.")
            elif nova_senha != confirmar_senha: st.error("Senhas divergentes.")
            else:
                usernames_db[novo_user] = {"name": novo_nome.upper(), "password": gerar_hash_sha256(nova_senha)}
                salvar_novas_credenciais(usernames_db)
                st.success("Conta criada!")
        st.stop()

# ==================== SESSÃO OPERACIONAL DE USUÁRIO ====================
username = st.session_state.username

if st.session_state.autenticado and username:
    name = usernames_db[username]["name"]
    ARQUIVO_DADOS = f"dados_user_{username}.json"

    def carregar_dados():
        if os.path.exists(ARQUIVO_DADOS):
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f: return json.load(f)
        return {"metas": [], "agua": 0, "peso_usuario": 70.0, "historico_pomodoro": 0, "refeicoes": [], "eventos_locais": []}

    def salvar_dados(dados):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f: json.dump(dados, f, indent=4, ensure_ascii=False)

    if "db" not in st.session_state or st.session_state.get("atual_user") != username:
        st.session_state.db = carregar_dados()
        st.session_state.atual_user = username
        
    db = st.session_state.db
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Sistemas prontos, {name}! Como posso te ajudar hoje?"}]

    if "pomo_segundos_restantes" not in st.session_state: st.session_state.pomo_segundos_restantes = 1500
    if "pomo_rodando" not in st.session_state: st.session_state.pomo_rodando = False
    if "pomo_tempo_inicial_escolhido" not in st.session_state: st.session_state.pomo_tempo_inicial_escolhido = 25
    if "eventos_locais" not in db: db["eventos_locais"] = []

    # --- TOP HEADER CONTROL BAR ---
    col_titulo_sistema, col_botao_logout = st.columns([5, 1.2])
    with col_titulo_sistema:
        header_dashboard = f"<h1 class='custom-title' style='margin-bottom: 0px !important;'>{ICONES['jarvis']} <span class='jarvis-brand'>JARVIS OS</span> <small style='font-size:12px; color:#777; letter-spacing:2px; margin-left:15px;'>COCKPIT INTERFACE MK4</small></h1>"
        st.markdown(header_dashboard, unsafe_allow_html=True)
    with col_botao_logout:
        if st.button("SAIR DA SESSÃO ✕"):
            st.session_state.autenticado = False
            st.session_state.username = None
            st.rerun()

    st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: rgba(212,175,55,0.15);'>", unsafe_allow_html=True)

    # --- MOTOR DE INTELIGÊNCIA DUPLO ORIGINAL (PRESERVADO) ---
    def processar_comando_e_criar_metas(comando):
        data_hoje_str = datetime.date.today().isoformat()
        if not API_KEY or client is None:
            return " Falha nos Sistemas: Nenhuma chave configurada. Por favor, adicione a variável GROQ_API_KEY."

        prompt_sistema_chat = (
            f"Você é o Jarvis, o assistente virtual executivo de Tony Stark (agora servindo ao usuário {name}). Hoje é {data_hoje_str}.\n"
            "Responda ao usuário com extrema imponência, elegância e eficiência britânica. "
            "Se o usuário pediu para marcar uma atividade, confirme elegantemente na resposta."
        )
        
        try:
            conversa_principal = client.chat.completions.create(
                model=MODELO_PRINCIPAL,
                messages=[{"role": "system", "content": prompt_sistema_chat}, {"role": "user", "content": comando}],
                temperature=0.7
            )
            resposta_texto_jarvis = conversa_principal.choices[0].message.content.strip()
        except Exception as e:
            if "401" in str(e) or "invalid_api_key" in str(e).lower():
                return " Falha Crítica: A chave configurada nos Secrets foi considerada INVÁLIDA pelo Groq."
            return f" Instabilidade nos Servidores: {str(e)}"

        try:
            prompt_sistema_extrator = (
                f"Você é uma inteligência de extração de dados e automação estruturada. Hoje é exatamente {data_hoje_str}.\n"
                "Analise minuciosamente o comando enviado pelo usuário e tome ações estruturadas em formato JSON.\n\n"
                "Regras Obrigatórias:\n"
                "1. Se o usuário pediu para adicionar, marcar, estudar, fazer, lembrar de algo, ou criar uma tarefa/meta, mude 'criar_meta' para true e inclua o objeto dentro de 'novas_metas'.\n"
                "2. Se o comando contiver referências de tempo ou data, você também deve mudar 'criar_evento' para true e gerar o item in 'novos_eventos' contendo a data YYYY-MM-DD and o horário HH:MM correspondentes.\n\n"
                "Esquema JSON estrito:\n"
                "{\n"
                "  \"criar_meta\": true/false,\n"
                "  \"novas_metas\": [ {\"nome\": \"Estudar Geografia\", \"categoria\": \"Estudos\"} ],\n"
                "  \"criar_evento\": true/false,\n"
                "  \"novos_eventos\": [ {\"title\": \"Estudar Geografia\", \"date\": \"YYYY-MM-DD\", \"time\": \"HH:MM\"} ]\n"
                "}"
            )
            
            extracao_dados = client.chat.completions.create(
                model=MODELO_EXTRATOR,
                messages=[{"role": "system", "content": prompt_sistema_extrator}, {"role": "user", "content": comando}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            dados_brutos = extracao_dados.choices[0].message.content.strip()
            resultado = json.loads(dados_brutos)
            
            if resultado.get("criar_meta") and resultado.get("novas_metas"):
                for nova_m in resultado.get("novas_metas", []):
                    if isinstance(nova_m, dict) and "nome" in nova_m:
                        db["metas"].append({
                            "id": str(time.time() + len(db["metas"])), 
                            "nome": nova_m["nome"],
                            "categoria": nova_m.get("categoria", "Geral"), 
                            "concluida": False, 
                            "tempo_dedicado": 0
                        })
                salvar_dados(db)
                
            if resultado.get("criar_evento") and resultado.get("novos_eventos"):
                for novo_ev in resultado.get("novos_eventos", []):
                    if isinstance(novo_ev, dict) and "title" in novo_ev:
                        db["eventos_locais"].append({
                            "id": f"ia_{int(time.time())}_{len(db['eventos_locais'])}",
                            "title": novo_ev["title"],
                            "date": novo_ev.get("date", data_hoje_str),
                            "time": novo_ev.get("time", "12:00")
                        })
                salvar_dados(db)
                
        except Exception as e:
            print(f"[Erro de Extração]: {str(e)}")
            
        return resposta_texto_jarvis

    # ==================== GRID BENTO BOX CENTRAL (ESQUERDA vs DIREITA) ====================
    col_painel_esquerdo, col_painel_direito = st.columns([1.6, 1.4])

    # --- PAINEL OPERACIONAL ESQUERDO ---
    with col_painel_esquerdo:
        
        # Módulo 1: Chat de Comando e IA Integrado
        st.markdown(f'<div class="bento-card">', unsafe_allow_html=True)
        card_html = f'<div class="titulo-card">{ICONES["conversa"]} TERMINAL CENTRAL DE DIRETRIZES</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        
        chat_container = st.container(height=300)
        with chat_container:
            for msg in st.session_state.messages: 
                st.chat_message(msg["role"]).write(msg["content"])
                
        if prompt := st.chat_input("Insira comando de voz ou texto..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            resposta = processar_comando_e_criar_metas(prompt)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Módulo 2: Objetivos Ativos Inteligentes
        st.markdown(f'<div class="bento-card">', unsafe_allow_html=True)
        card_html = f'<div class="titulo-card">{ICONES["jarvis"]} OBJETIVOS E DIRETRIZES ATIVAS</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        
        metas_ativas = [m for m in db["metas"] if not m["concluida"]]
        if not metas_ativas: 
            st.info("Nenhum objetivo prioritário em execução no momento.")
        else:
            for m in db["metas"]:
                if not m["concluida"]:
                    c1, c2, c3 = st.columns([2.5, 1, 0.8])
                    c1.markdown(f"**{m['nome']}**<br><span style='color:#777777; font-size:11px;'>{m['categoria']}</span>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='padding-top:6px; color:#d4af37; font-weight:600;'>{m['tempo_dedicado']} min</div>", unsafe_allow_html=True)
                    if c3.button("✓ Concluir", key=m["id"]):
                        m["concluida"] = True
                        salvar_dados(db)
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PAINEL OPERACIONAL DIREITO ---
    with col_painel_direito:
        
        # Módulo 3: Timer de Foco Pomodoro
        st.markdown(f'<div class="bento-card">', unsafe_allow_html=True)
        card_html = f'<div class="titulo-card">{ICONES["foco"]} TIMER DE CRONOMETRAGEM TÁTICA</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        
        metas_validas = [m for m in db["metas"] if not m["concluida"]]
        if not metas_validas: 
            st.warning("Defina uma tarefa ativa conversando com o Jarvis para liberar o Timer.")
        else:
            cp1, cp2 = st.columns([1.1, 0.9])
            with cp1:
                meta_alvo = st.selectbox("Focar em:", [m["nome"] for m in metas_validas])
                minutos_slider = st.slider("Duração do ciclo:", 1, 120, int(st.session_state.pomo_tempo_inicial_escolhido), disabled=st.session_state.pomo_rodando)
                
                if not st.session_state.pomo_rodando and st.session_state.pomo_tempo_inicial_escolhido != minutos_slider:
                    st.session_state.pomo_tempo_inicial_escolhido = minutos_slider
                    st.session_state.pomo_segundos_restantes = minutos_slider * 60
                    
                b1, b2 = st.columns([1, 1])
                if not st.session_state.pomo_rodando:
                    if b1.button("▶ INICIAR"): 
                        st.session_state.pomo_rodando = True
                        st.rerun()
                else:
                    if b1.button("⏸ PAUSAR"): 
                        st.session_state.pomo_rodando = False
                        st.rerun()
                if b2.button("Automático" if st.session_state.pomo_rodando else "🔄 RESET"):
                    st.session_state.pomo_rodando = False
                    st.session_state.pomo_segundos_restantes = st.session_state.pomo_tempo_inicial_escolhido * 60
                    st.rerun()
            with cp2:
                m_vis, s_vis = divmod(st.session_state.pomo_segundos_restantes, 60)
                st.markdown(f"<div style='text-align: center; display: flex; flex-direction: column; justify-content: center; background: rgba(0,0,0,0.3); padding: 10px; border-radius:12px; border: 1px solid rgba(212,175,55,0.05);'><h1 style='font-size: 45px; font-family: \"Kanit\"; color:#ffffff; margin: 0; font-weight:700;'>{m_vis:02d}:{s_vis:02d}</h1><span style='color:#d4af37; font-weight: 500; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top:5px;'> {meta_alvo}</span></div>", unsafe_allow_html=True)
            
            if st.session_state.pomo_rodando and st.session_state.pomo_segundos_restantes > 0:
                time.sleep(1)
                st.session_state.pomo_segundos_restantes -= 1
                if st.session_state.pomo_segundos_restantes == 0:
                    st.session_state.pomo_rodando = False
                    for m in db["metas"]:
                        if m["nome"] == meta_alvo and not m["concluida"]: 
                            m["tempo_dedicado"] += st.session_state.pomo_tempo_inicial_escolhido
                    db["historico_pomodoro"] += st.session_state.pomo_tempo_inicial_escolhido
                    salvar_dados(db)
                    st.balloons()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Módulo 4: Saúde, Fluidos & Fitness Integrado
        st.markdown(f'<div class="bento-card">', unsafe_allow_html=True)
        card_html = f'<div class="titulo-card">{ICONES["saude"]} MONITOR BIOMÉTRICO (V_VITALS)</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        
        cs1, cs2 = st.columns([1, 1])
        with cs1:
            peso_texto = st.text_input("Peso corporal (kg):", value=str(db.get("peso_usuario", 70.0)))
            try: peso_limpo = float(peso_texto.replace(',', '.'))
            except: peso_limpo = 70.0
            db["peso_usuario"] = peso_limpo
            alvo_calc = int(peso_limpo * 35)
            
            st.metric("Consumido", f"{db['agua']} ml", f"Alvo: {alvo_calc} ml")
            cb1, cb2 = st.columns([1, 1])
            if cb1.button("➕ Copo"): 
                db["agua"] += 250
                salvar_dados(db)
                st.rerun()
            if cb2.button("🔄 Limpar"): 
                db["agua"] = 0
                salvar_dados(db)
                st.rerun()
        with cs2:
            refeicao = st.text_input("Catalogar refeição:", placeholder="Ex: Whey protein")
            if st.button("Registrar Macro"):
                if refeicao:
                    db["refeicoes"].append({"data": str(datetime.date.today()), "item": refeicao})
                    salvar_dados(db)
                    st.toast("Nutrientes Catalogados!")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== SEÇÃO INFERIOR PARA COMPROMISSOS E RELATÓRIOS ====================
    st.markdown("<br>", unsafe_allow_html=True)
    
    aba_calendario, aba_graficos = st.tabs(["[📆] AGENDA E CRONOGRAMA", "[📊] ANÁLISE OPERACIONAL"])
    
    # 4. AGENDA COMPLETA ORIGINAL
    with aba_calendario:
        st.markdown(f'<div class="bento-card">', unsafe_allow_html=True)
        col_esq_info, col_dir_cal = st.columns([1, 1.5])
        
        hoje = datetime.date.today()
        dia_num_hoje = hoje.strftime("%d")
        dias_traduzidos = {
            "Monday": "SEGUNDA-FEIRA", "Tuesday": "TERÇA-FEIRA", "Wednesday": "QUARTA-FEIRA",
            "Thursday": "QUINTA-FEIRA", "Friday": "SEXTA-FEIRA", "Saturday": "SÁBADO", "Sunday": "DOMINGO"
        }
        dia_name_hoje = dias_traduzidos.get(hoje.strftime("%A"), "HOJE")
        
        with col_esq_info:
            st.markdown(
                f"<div style='background-color: #0b0b0b; padding: 20px; border-radius: 12px; border-left: 4px solid #d4af37; margin-bottom: 15px; border: 1px solid rgba(212,175,55,0.1);'>"
                f"<span style='color: #777777; font-size: 11px; font-weight:600; text-transform:uppercase;'>Data de Telemetria</span>"
                f"<h1 style='font-size: 60px; font-family: \"Kanit\", sans-serif; font-weight: 700; line-height:1; margin: 5px 0; color: #ffffff;'>{dia_num_hoje}</h1>"
                f"<div style='font-size: 13px; font-family: \"Kanit\", sans-serif; color: #d4af37; font-weight:500; text-transform: uppercase;'>{dia_name_hoje}</div>"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            with st.expander("➕ AGENDAR COMPROMISSO MANUAL", expanded=False):
                nome_ev = st.text_input("Título:")
                data_ev = st.date_input("Data:", hoje)
                h_ini = st.time_input("Horário:", datetime.time(9, 0))
                
                if st.button("Salvar Evento"):
                    if nome_ev:
                        id_unico = f"manual_{int(time.time())}"
                        db["eventos_locais"].append({
                            "id": id_unico, "title": nome_ev, "date": data_ev.isoformat(), "time": h_ini.strftime('%H:%M')
                        })
                        salvar_dados(db)
                        st.rerun()

        with col_dir_cal:
            mes_atual = hoje.month
            ano_atual = hoje.year
            dias_semana_headers = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
            
            cal_objeto = pycalendar.Calendar(firstweekday=6)
            mes_dias = cal_objeto.monthdayscalendar(ano_atual, mes_atual)
            
            dict_eventos = {}
            for ev in db.get("eventos_locais", []):
                ev_date_str = ev.get("date")
                if ev_date_str:
                    if ev_date_str not in dict_eventos: dict_eventos[ev_date_str] = []
                    dict_eventos[ev_date_str].append(ev)

            meses_nomes = {1: "JANEIRO", 2: "FEVEREIRO", 3: "MARÇO", 4: "ABRIL", 5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO", 9: "SETEMBRO", 10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"}
            nome_do_mes = meses_nomes.get(mes_atual, "CRONOGRAMA")
            
            html_estilos_calendario = """
            <style>
                .jarvis-calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; background-color: #0a0a0a; padding: 10px; border-radius: 12px; border: 1px solid rgba(212, 175, 55, 0.15); width: 100%; box-sizing: border-box; }
                .calendar-header-day { text-align: center; font-weight: 600; font-size: 11px; color: #777777; text-transform: uppercase; }
                .calendar-cell { background-color: rgba(16, 16, 16, 0.7); border: 1px solid rgba(255, 255, 255, 0.02); border-radius: 8px; min-height: 55px; padding: 4px; display: flex; flex-direction: column; }
                .calendar-cell.cell-today { background-color: rgba(212, 175, 55, 0.06); border: 1px solid #d4af37; }
                .calendar-cell.cell-empty { background-color: transparent; border: none; }
                .cell-number { font-weight: 700; font-size: 12px; color: #555; align-self: flex-end; }
                .cell-today .cell-number { color: #d4af37; }
                .events-wrapper { width: 100%; display: flex; flex-direction: column; gap: 2px; }
                .event-tag { background-color: rgba(212, 175, 55, 0.12); color: #f3e5ab; font-size: 9px; padding: 2px 4px; border-radius: 4px; border-left: 2px solid #d4af37; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
            </style>
            """
            
            html_corpo = f"<div style='text-align: center; margin-bottom: 8px; font-size: 13px; color: #ffffff; font-weight: 600; letter-spacing: 1px;'>{nome_do_mes} {ano_atual}</div>"
            html_corpo += "<div class='jarvis-calendar-grid'>"
            
            for hd in dias_semana_headers:
                html_corpo += f"<div class='calendar-header-day'>{hd}</div>"
                
            for semana in mes_dias:
                for dia_num in semana:
                    if dia_num == 0:
                        html_corpo += "<div class='calendar-cell cell-empty'></div>"
                    else:
                        data_corrente = datetime.date(ano_atual, mes_atual, dia_num)
                        data_corrente_str = data_corrente.isoformat()
                        classe_hoje = "cell-today" if data_corrente == hoje else ""
                        
                        conteudo_eventos = ""
                        if data_corrente_str in dict_eventos:
                            conteudo_eventos += "<div class='events-wrapper'>"
                            for ev in dict_eventos[data_corrente_str]:
                                titulo_limpo = ev.get("title", "Compromisso")
                                conteudo_eventos += f"<div class='event-tag' title='{titulo_limpo}'>{titulo_limpo}</div>"
                            conteudo_eventos += "</div>"
                                
                        html_corpo += f"<div class='calendar-cell {classe_hoje}'>"
                        html_corpo += f"<div class='cell-number'>{dia_num}</div>"
                        html_corpo += conteudo_eventos
                        html_corpo += "</div>"
                        
            html_corpo += "</div>"
            st.components.v1.html(html_estilos_calendario + html_corpo, height=360, scrolling=False)

        # Listagem Completa de Remoção Mecânica
        eventos_cadastrados = db.get("eventos_locais", [])
        if eventos_cadastrados:
            st.markdown("<hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            eventos_ordenados = sorted(eventos_cadastrados, key=lambda x: (x.get("date", ""), x.get("time", "")))
            for idx, ev in enumerate(eventos_ordenados):
                try: data_convertida = datetime.date.fromisoformat(ev["date"]).strftime("%d/%m/%Y")
                except: data_convertida = ev["date"]
                
                co1, co2 = st.columns([5, 1])
                co1.markdown(f"• **{ev['title']}** — `{data_convertida}` às `{ev['time']}`")
                if co2.button("Remover", key=f"del_{ev.get('id', idx)}"):
                    db["eventos_locais"] = [item for item in db["eventos_locais"] if item.get("id") != ev.get("id")]
                    salvar_dados(db)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. ESTATÍSTICAS E GRÁFICOS ORIGINAIS (PRESERVAÇÃO DO TRUNCAMENTO ANTERIOR)
    with aba_graficos:
        st.markdown(f'<div class="bento-card">', unsafe_allow_html=True)
        st.markdown(f"### Histórico cumulativo de foco: {db.get('historico_pomodoro', 0)} minutos dedicação.")
        if db.get("metas"):
            for m in db["metas"]:
                st.write(f"- {m['nome']}: {m['tempo_dedicado']} minutos consolidados.")
        else:
            st.info("Nenhum dado analítico gerado ainda.")
        st.markdown('</div>', unsafe_allow_html=True)
