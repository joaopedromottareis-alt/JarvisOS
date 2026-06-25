import streamlit as st
import datetime
import time
import json
import os
import hashlib
import re
import calendar as pycalendar
from groq import Groq

# Bibliotecas Oficiais do Google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Escopo necessário para ler e escrever no Google Agenda
SCOPES = ['https://www.googleapis.com/auth/calendar']

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

# ==================== CONFIGURAÇÃO VISUAL MODERNA ====================
LOGO_JARVIS_URL = "https://img.icons8.com/ios-filled/510/ffffff/artificial-intelligence.png"

st.set_page_config(
    page_title="Jarvis OS", 
    page_icon=LOGO_JARVIS_URL,
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Dicionário de Ícones SVG
ICONES = {
    "jarvis": """<svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffd700"/>
                <stop offset="50%" stop-color="#d4af37"/>
                <stop offset="100%" stop-color="#8a6d1c"/>
            </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="42" stroke="url(#gold-grad)" stroke-width="5" stroke-dasharray="4 2" fill="none" />
        <circle cx="50" cy="50" r="28" stroke="url(#gold-grad)" stroke-width="3" fill="none" opacity="0.8"/>
        <path d="M50 32 L66 60 L34 60 Z" stroke="url(#gold-grad)" stroke-width="3" fill="none"/>
        <circle cx="50" cy="52" r="6" fill="url(#gold-grad)"/>
    </svg>""",
    "conversa": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z" fill="url(#gold-grad)"/></svg>""",
    "foco": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z" fill="url(#gold-grad)"/></svg>""",
    "saude": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.5 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35zM10.5 7.5H9v2H7.5v1.5H9v2h1.5v-2H12v-1.5h-1.5v-2zm6 1.5h-3v1.5h3V9z" fill="url(#gold-grad)"/></svg>""",
    "calendario": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z" fill="url(#gold-grad)"/></svg>""",
    "metas_caderno": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="gold-grad-caderno" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffd700"/>
                <stop offset="50%" stop-color="#d4af37"/>
                <stop offset="100%" stop-color="#aa7c11"/>
            </linearGradient>
        </defs>
        <path d="M3 5c0-.55.45-1 1-1h1v16H4c-.55 0-1-.45-1-1V5zm4-1h10c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H7V4zm14 2h-1v12h1c.55 0 1-.45 1-1V7c0-.55-.45-1-1-1zm-11 3h6v1.5h-6V9zm0 3.5h6V14h-6v-1.5zm0 3.5h4v1.5h-4V16z" fill="url(#gold-grad-caderno)"/>
        <path d="M18.5 3.5l2 2-11 11H7.5v-2l11-11z" fill="url(#gold-grad-caderno)"/>
    </svg>"""
}

# CSS Customizado Estabilizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp { 
        background-color: #050505 !important; 
        color: #e5e5e5 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-image: linear-gradient(135deg, #050505 0%, #0c0a05 50%, #141002 100%) !important;
        background-attachment: fixed !important;
    }
    
    [data-testid="stSidebarCollapsedControl"], [data-testid="stSidebar"], #MainMenu, footer, header {
        display: none !important;
    }
    
    .block-container { 
        padding: 2rem 3rem !important; 
        max-width: 100% !important; 
    }
    
    .custom-title {
        font-family: 'Kanit', sans-serif !important;
        background: linear-gradient(135deg, #ffffff 40%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important; 
        letter-spacing: -0.5px !important;
        margin-bottom: 25px !important;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .jarvis-brand {
        background: linear-gradient(45deg, #d4af37, #f3e5ab, #aa7c11);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    .instrucao-card {
        background-color: rgba(212, 175, 55, 0.05) !important;
        border: 1px dashed rgba(212, 175, 55, 0.3) !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== GERENCIADOR DE USUÁRIOS FÍSICO ====================
ARQUIVO_CONFIG_USERS = "usuarios_config.json"

def gerar_hash_sha256(senha_texto):
    return hashlib.sha256(senha_texto.encode('utf-8')).hexdigest()

def carregar_credenciais_salvas():
    if os.path.exists(ARQUIVO_CONFIG_USERS):
        try:
            with open(ARQUIVO_CONFIG_USERS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if "usernames" in dados: return dados["usernames"]
                return dados
        except Exception:
            pass
    return {"admin": {"name": "SENHOR ADMIN", "password": gerar_hash_sha256("admin123")}}

def salvar_novas_credenciais(dicionario_usernames):
    with open(ARQUIVO_CONFIG_USERS, "w", encoding="utf-8") as f:
        json.dump({"usernames": dicionario_usernames}, f, indent=4, ensure_ascii=False)

usernames_db = carregar_credenciais_salvas()

if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "username" not in st.session_state: st.session_state.username = None

# --- CAPTURA DE RETORNO DO OAUTH DO GOOGLE ---
parametros_url = st.query_params
if "code" in parametros_url and "state" in parametros_url:
    codigo_google = parametros_url["code"]
    usuario_registro = parametros_url["state"] 
    
    if os.path.exists('credentials.json'):
        try:
            redirecionamento_uri = "http://localhost:8501" 
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES, redirect_uri=redirecionamento_uri)
            flow.fetch_token(code=codigo_google)
            creds = flow.credentials
            
            token_path = f"token_user_{usuario_registro}.json"
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
                
            st.success("✓ Integração com o Google Agenda realizada com sucesso!")
            st.info("Sua conta está ativa. Use a aba LOGIN para acessar.")
            st.query_params.clear() 
            time.sleep(3)
        except Exception as e:
            st.error(f"Erro ao salvar token do Google: {e}")

# --- TELA DE LOGIN / REGISTRO COM INSTRUÇÕES ---
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
                if hash_informado == hash_salvo:
                    st.session_state.autenticado = True
                    st.session_state.username = input_user
                    st.rerun()
                else: st.error("CHAVE INCORRETA.")
            else: st.error("OPERADOR NÃO ENCONTRADO.")
        st.stop()
            
    elif modo_tela == "REGISTRAR NOVA CONTA":
        st.markdown("### CRIAR NOVA CONTA INTEGRADA")
        
        # Bloco explicativo de Instruções requisitado
        st.markdown("""
        <div class="instrucao-card">
            <h4 style="color: #d4af37; margin-top: 0;">📋 INSTRUÇÕES DE CADASTRO:</h4>
            <ol style="font-size: 14px; margin-bottom: 0;">
                <li>Escolha como o Jarvis se referirá a você e defina um <b>Username</b> único (sem espaços).</li>
                <li>Ao clicar no botão de confirmação, você será levado à página de consentimento do <b>Google Agenda</b>.</li>
                <li>Permita o acesso para que seus compromissos e rotinas fiquem salvos na nuvem automaticamente.</li>
                <li>Após conceder a permissão, você retornará para cá e poderá efetuar o Login.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        novo_nome = st.text_input("COMO O JARVIS DEVE TE CHAMAR?")
        novo_user = st.text_input("USERNAME (SEM ESPAÇOS, CURTO):").strip().lower()
        nova_senha = st.text_input("SENHA DE SEGURANÇA:", type="password")
        confirmar_senha = st.text_input("CONFIRME A SENHA:", type="password")
        
        if st.button("VINCULAR GOOGLE CALENDAR E FINALIZAR CADASTRO"):
            if not novo_nome or not novo_user or not nova_senha: 
                st.error("Preencha todos os campos obrigatórios.")
            elif novo_user in usernames_db: 
                st.error("Username já existe no banco de dados.")
            elif nova_senha != confirmar_senha: 
                st.error("As senhas informadas divergem.")
            elif not os.path.exists('credentials.json'):
                st.error("Arquivo 'credentials.json' ausente na raiz do servidor!")
            else:
                usernames_db[novo_user] = {"name": novo_nome.upper(), "password": gerar_hash_sha256(nova_senha)}
                salvar_novas_credenciais(usernames_db)
                
                redirecionamento_uri = "http://localhost:8501" 
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES, redirect_uri=redirecionamento_uri)
                auth_url, _ = flow.authorization_url(prompt='consent', state=novo_user)
                
                st.success("Conta Local criada! Redirecionando para a Google...")
                st.markdown(f'<meta http-equiv="refresh" content="1;url={auth_url}">', unsafe_allow_html=True)
                st.stop()

# ==================== SESSÃO OPERACIONAL DE USUÁRIO ====================
username = st.session_state.username

if st.session_state.autenticado and username:
    name = usernames_db[username]["name"]
    ARQUIVO_DADOS = f"dados_user_{username}.json"
    TOKEN_GOOGLE_USER = f"token_user_{username}.json"

    def carregar_dados():
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f: 
                    return json.load(f)
            except Exception:
                pass
        return {"metas": [], "agua": 0, "peso_usuario": 70.0, "historico_pomodoro": 0, "refeicoes": [], "eventos_locais": [], "conversas": {}}

    def salvar_dados(dados):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f: 
            json.dump(dados, f, indent=4, ensure_ascii=False)

    if "db" not in st.session_state or st.session_state.get("atual_user") != username:
        st.session_state.db = carregar_dados()
        st.session_state.atual_user = username
        
    db = st.session_state.db
    if "conversas" not in db: db["conversas"] = {}
    if "eventos_locais" not in db: db["eventos_locais"] = []
    if "pomo_segundos_restantes" not in st.session_state: st.session_state.pomo_segundos_restantes = 1500
    if "pomo_rodando" not in st.session_state: st.session_state.pomo_rodando = False
    if "pomo_tempo_inicial_escolhido" not in st.session_state: st.session_state.pomo_tempo_inicial_escolhido = 25

    def obter_servico_google_calendar():
        creds = None
        if os.path.exists(TOKEN_GOOGLE_USER):
            try: creds = Credentials.from_authorized_user_file(TOKEN_GOOGLE_USER, SCOPES)
            except: creds = None
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(TOKEN_GOOGLE_USER, 'w') as token: token.write(creds.to_json())
                except: creds = None
        return build('calendar', 'v3', credentials=creds) if creds else None

    def enviar_evento_para_google(titulo, data_str, horario_str):
        service = obter_servico_google_calendar()
        if not service: return False
        try:
            start_datetime = f"{data_str}T{horario_str}:00"
            horas, minutos = map(int, horario_str.split(':'))
            end_datetime = f"{data_str}T{(horas + 1) % 24:02d}:{minutos:02d}:00"
            event = {
                'summary': titulo,
                'description': 'Agendado via Jarvis OS',
                'start': {'dateTime': start_datetime, 'timeZone': 'America/Sao_Paulo'},
                'end': {'dateTime': end_datetime, 'timeZone': 'America/Sao_Paulo'},
            }
            service.events().insert(calendarId='primary', body=event).execute()
            return True
        except: return False

    def puxar_eventos_do_google():
        service = obter_servico_google_calendar()
        if not service: return
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=20, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
            db["eventos_locais"] = []
            for ev in events:
                start = ev['start'].get('dateTime', ev['start'].get('date'))
                db["eventos_locais"].append({
                    "id": ev['id'], "title": ev.get('summary', 'Sem Título'),
                    "date": start[:10], "time": start[11:16] if 'T' in start else "00:00"
                })
            salvar_dados(db)
        except: pass

    # --- HEADER ---
    col_titulo_sistema, col_botao_logout = st.columns([5, 1])
    with col_titulo_sistema:
        st.markdown(f"<h1 class='custom-title'>{ICONES['jarvis']} <span class='jarvis-brand'>JARVIS OS</span></h1>", unsafe_allow_html=True)
    with col_botao_logout:
        if st.button("SAIR DA SESSÃO"):
            st.session_state.autenticado = False
            st.session_state.username = None
            st.rerun()

    st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: rgba(212,175,55,0.15);'>", unsafe_allow_html=True)

    # --- NAVEGAÇÃO POR ABAS ---
    aba_metas, aba_pomodoro, aba_saude, aba_calendario = st.tabs(["CONVERSA & METAS", "TIMER DE FOCO", "SAÚDE & FITNESS", "AGENDA"])

    # 1. CONVERSA & METAS
    with aba_metas:
        col_ia, col_lista = st.columns([1, 1.3])
        with col_ia:
            st.markdown(f'<div class="titulo-card">{ICONES["conversa"]} GERENCIADOR DE CONVERSAS</div>', unsafe_allow_html=True)
            opcoes_conversas = ["➕ Iniciar Nova Conversa"] + list(db["conversas"].keys())
            conversa_selecionada = st.selectbox("Selecione o chat:", opcoes_conversas, label_visibility="collapsed")
            
            chat_container = st.container(height=300)
            with chat_container:
                msgs = db["conversas"].get(conversa_selecionada, [{"role": "assistant", "content": f"Sistemas prontos, {name}."}])
                for msg in msgs: st.chat_message(msg["role"]).write(msg["content"])
            
            prompt = st.chat_input("Envie sua instrução...")
            if prompt:
                if conversa_selecionada == "➕ Iniciar Nova Conversa":
                    conversa_alvo = f"Conversa {int(time.time())}"
                    db["conversas"][conversa_alvo] = []
                else: conversa_alvo = conversa_selecionada
                
                db["conversas"][conversa_alvo].append({"role": "user", "content": prompt})
                # Simulação básica/resposta da IA
                db["conversas"][conversa_alvo].append({"role": "assistant", "content": "Diretrizes anotadas com sucesso."})
                salvar_dados(db)
                st.rerun()
                    
        with col_lista:
            st.markdown(f'<div class="titulo-card">{ICONES["metas_caderno"]} OBJETIVOS ATIVOS</div>', unsafe_allow_html=True)
            with st.container(height=380):
                if not db["metas"]: st.info("Nenhuma meta cadastrada.")
                for m in db["metas"]:
                    if not m["concluida"]:
                        c1, c2, c3 = st.columns([3, 1, 1])
                        c1.markdown(f"**{m['nome']}**")
                        c2.write(f"{m['tempo_dedicado']} min")
                        if c3.button("✓", key=m["id"]):
                            m["concluida"] = True; salvar_dados(db); st.rerun()

    # 2. TIMER DE FOCO
    with aba_pomodoro:
        st.markdown(f'<div class="titulo-card">{ICONES["foco"]} TIMER DE FOCO</div>', unsafe_allow_html=True)
        m_vis, s_vis = divmod(st.session_state.pomo_segundos_restantes, 60)
        st.metric("Tempo Restante", f"{m_vis:02d}:{s_vis:02d}")
        if st.button("▶ INICIAR" if not st.session_state.pomo_rodando else "⏸ PAUSAR"):
            st.session_state.pomo_rodando = not st.session_state.pomo_rodando
            st.rerun()

    # 3. SAÚDE & FITNESS
    with aba_saude:
        st.markdown(f'<div class="titulo-card">{ICONES["saude"]} HIDRATAÇÃO</div>', unsafe_allow_html=True)
        st.metric("Água Consumida", f"{db['agua']} ml")
        if st.button("➕ Beber Copo (250ml)"):
            db["agua"] += 250; salvar_dados(db); st.rerun()

    # 4. AGENDA 
    with aba_calendario:
        st.markdown(f'<div class="titulo-card">{ICONES["calendario"]} CRONOGRAMA</div>', unsafe_allow_html=True)
        col_esq, col_dir = st.columns([1, 1.3])
        with col_esq:
            nome_ev = st.text_input("Nome do compromisso:")
            data_ev = st.date_input("Data:", datetime.date.today())
            if st.button("Agendar Evento"):
                if nome_ev:
                    db["eventos_locais"].append({"id": str(time.time()), "title": nome_ev, "date": data_ev.isoformat(), "time": "09:00"})
                    salvar_dados(db)
                    enviar_evento_para_google(nome_ev, data_ev.isoformat(), "09:00")
                    st.success("Agendado!")
                    st.rerun()
        with col_dir:
            # Renderização correta com correção de corte aplicada
            st.components.v1.html(f"<div style='color: white; background:#111; padding:20px; border-radius:10px;'>Calendário Ativo ({len(db['eventos_locais'])} eventos mapeados)</div>", height=650, scrolling=True)
