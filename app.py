import streamlit as st
import datetime
import time
import json
import os
import hashlib
from groq import Groq
import plotly.graph_objects as go

# --- Importações para o Calendário e OAuth Web ---
from streamlit_calendar import calendar
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# ==================== CONFIGURAÇÃO DA IA (GROQ) ====================
API_KEY = "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"
client = Groq(api_key=API_KEY)
MODELO_IA = "llama-3.3-70b-versatile" 

SCOPES = ['https://www.googleapis.com/auth/calendar']

# ==================== CONFIGURAÇÃO VISUAL MODERNA (PRETO E DOURADO MINIMALISTA) ====================
st.set_page_config(page_title="Jarvis OS", page_icon="🔱", layout="wide", initial_sidebar_state="collapsed")

# CSS Global Cirúrgico - Removendo bordas fantasmas e aplicando o conceito de calendário SCSS adaptado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* 1. PALETA BASE */
    .stApp { 
        background-color: #050505 !important; 
        color: #e5e5e5 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-image: 
            radial-gradient(circle at 50% -20%, rgba(212, 175, 55, 0.07) 0%, transparent 60%),
            radial-gradient(circle at 90% 80%, rgba(184, 134, 11, 0.03) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
    }
    
    [data-testid="stSidebarCollapsedControl"], [data-testid="stSidebar"], #MainMenu, footer, header {
        display: none !important;
    }
    
    .block-container { 
        padding: 3rem 5rem !important; 
        max-width: 100% !important; 
    }
    
    /* 2. TIPOGRAFIA */
    .custom-title {
        font-family: 'Kanit', sans-serif !important;
        background: linear-gradient(135deg, #ffffff 40%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important; 
        letter-spacing: -0.5px !important;
        margin-bottom: 25px !important;
    }
    
    .jarvis-brand {
        background: linear-gradient(45deg, #d4af37, #f3e5ab, #aa7c11);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    /* 3. REMOÇÃO DE TODAS AS BORDAS INTERNAS E EXTERNAS DOS INPUTS */
    div[data-baseweb="base-input"],
    div[data-baseweb="input"],
    div[data-baseweb="input"] > div,
    .stTextInput > div,
    .stTextInput > div > div,
    .stDateInput > div,
    .stTextArea > div,
    .stSelectbox > div {
        border: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
        outline: none !important;
    }

    /* Estilo limpo flutuante para a caixa real de digitação */
    .stTextInput input, 
    .stDateInput input,
    .stTextArea textarea,
    div[data-baseweb="select"] {
        background-color: rgba(20, 20, 20, 0.8) !important; 
        border: 1px solid rgba(212, 175, 55, 0.15) !important; 
        border-radius: 12px !important; 
        color: #ffffff !important;
        padding: 10px 16px !important;
        box-shadow: none !important;
        outline: none !important;
        transition: all 0.25s ease;
    }
    
    .stTextInput input:focus, 
    .stDateInput input:focus,
    .stTextArea textarea:focus {
        border-color: #d4af37 !important;
        background-color: #0f0f0f !important;
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.2) !important;
        outline: none !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"], 
    div[data-testid="stVerticalBlock"], 
    div[data-testid="element-container"],
    div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"],
    div[data-testid="stBlock"],
    .stElementContainer {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .titulo-card { 
        color: #d4af37 !important; 
        font-family: 'Kanit', sans-serif !important;
        font-size: 14px !important; 
        font-weight: 500 !important; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        opacity: 0.95;
        border-bottom: 1px solid rgba(212, 175, 55, 0.15) !important;
        padding-bottom: 8px;
    }

    /* Botões Dourados */
    .stButton>button { 
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important; 
        color: #000000 !important; 
        border: none !important;
        border-radius: 12px !important; 
        padding: 12px 24px !important; 
        font-weight: 700 !important; 
        font-family: 'Kanit', sans-serif !important;
        font-size: 14px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1) !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover { 
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.25) !important;
        filter: brightness(1.1);
    }
    
    /* Abas */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        margin-bottom: 30px !important;
        gap: 20px !important;
    }
    .stTabs [data-baseweb="tab"] { 
        color: #777777 !important; 
        font-family: 'Kanit', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        background-color: transparent !important;
        padding: 12px 4px !important;
        border-radius: 0px !important;
        transition: all 0.25s ease;
    }
    .stTabs [aria-selected="true"] { 
        color: #d4af37 !important; 
        border-bottom: 2px solid #d4af37 !important;
    }
    
    .stExpander {
        background-color: rgba(15, 15, 15, 0.6) !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        border-radius: 12px !important;
    }

    /* ==================== CALENDÁRIO COM CONCEITO SCSS INTEGRADO ==================== */
    .calendar-container {
        background-color: #0a0a0a !important;
        border-radius: 34px !important; /* Herdado do seu código SCSS (--border-radius) */
        padding: 24px 20px !important;  /* Herdado do seu código SCSS (--side-padding) */
        border: 1px solid rgba(212, 175, 55, 0.15) !important;
        max-width: 100%;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5) !important;
    }

    iframe[title="streamlit_calendar.calendar"] {
        border: none !important;
        background-color: transparent !important;
    }

    .fc {
        font-family: 'Kanit', sans-serif !important;
        background-color: transparent !important;
    }
    
    /* Botões Superiores do Calendário (Estilo __button do SCSS) */
    .fc .fc-button-primary {
        background-color: #141414 !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        color: #e5e5e5 !important;
        border-radius: 15px !important; /* Arredondamento secundário do SCSS */
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    .fc .fc-button-primary:hover {
        background-color: #d4af37 !important;
        color: #000000 !important;
        box-shadow: 0 8px 15px rgba(212, 175, 55, 0.2) !important;
    }

    /* Efeito Hover nas datas - Inspirado no &:hover::before do SCSS */
    .fc .fc-daygrid-day {
        transition: background-color 0.2s ease !important;
        cursor: pointer !important;
    }
    .fc .fc-daygrid-day:hover {
        background-color: rgba(212, 175, 55, 0.06) !important;
    }

    /* Elemento hoje / selecionado - Inspirado no &--selected */
    .fc .fc-day-today {
        background-color: rgba(212, 175, 55, 0.12) !important;
        border: 1px solid #d4af37 !important;
    }

    .fc .fc-col-header-cell {
        background-color: transparent !important;
        padding: 10px 0 !important;
        color: #777777 !important; /* Cor cinza do cabeçalho __days */
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.9rem;
    }

    .fc-theme-standard td, .fc-theme-standard th {
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
    }

    /* Mensagens do Chat */
    [data-testid="stChatMessage"] {
        background-color: rgba(20, 20, 20, 0.5) !important;
        border-left: 3px solid #d4af37 !important;
        border-radius: 0px 12px 12px 0px !important;
        padding: 12px 16px !important;
        margin-bottom: 16px !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-weight: 700 !important;
        font-family: 'Kanit', sans-serif !important;
        color: #d4af37 !important;
        text-shadow: 0 0 8px rgba(212, 175, 55, 0.2);
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
            if "credentials" in dados and "usernames" in dados["credentials"]:
                return dados["credentials"]["usernames"]
            if "usernames" in dados:
                return dados["usernames"]
            return dados
    return {"admin": {"name": "SENHOR ADMIN", "password": gerar_hash_sha256("admin123")}}

def salvar_novas_credenciais(dicionario_usernames):
    estrutura = {"usernames": dicionario_usernames}
    with open(ARQUIVO_CONFIG_USERS, "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=4, ensure_ascii=False)

usernames_db = carregar_credenciais_salvas()

if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "username" not in st.session_state: st.session_state.username = None

query_params = st.query_params
if "code" in query_params and st.session_state.get("aguardando_oauth_user"):
    target_user = st.session_state.aguardando_oauth_user
    try:
        client_config = {
            "web": {
                "client_id": st.secrets["google_oauth"]["client_id"],
                "client_secret": st.secrets["google_oauth"]["client_secret"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        flow = Flow.from_client_config(client_config, scopes=SCOPES, redirect_uri=st.secrets["google_oauth"]["redirect_uri"])
        flow.fetch_token(code=query_params["code"])
        
        token_path = f"token_google_{target_user}.json"
        with open(token_path, "w") as f:
            f.write(flow.credentials.to_json())
            
        st.session_state.autenticado = True
        st.session_state.username = target_user
        st.session_state.pop("aguardando_oauth_user", None)
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"ERRO DE VALIDAÇÃO: {e}")

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown("<h2 class='custom-title'>✨ ENTRAR NO <span class='jarvis-brand'>JARVIS OS</span></h2>", unsafe_allow_html=True)
    modo_tela = st.radio("SELECIONE A OPERAÇÃO:", ["LOGIN", "REGISTRAR NOVA CONTA"], horizontal=True)
    
    if modo_tela == "LOGIN":
        st.markdown("### 🔑 LOGIN DO OPERADOR")
        input_user = st.text_input("USERNAME:", key="login_username").strip().lower()
        input_senha = st.text_input("SENHA DE SEGURANÇA:", type="password", key="login_password")
        
        if st.button("ACESSAR PAINEL PRINCIPAL"):
            if input_user in usernames_db:
                hash_informado = gerar_hash_sha256(input_senha)
                hash_salvo = usernames_db[input_user]["password"]
                
                if hash_informado == hash_salvo or input_senha == hash_salvo:
                    st.session_state.autenticado = True
                    st.session_state.username = input_user
                    st.success("ACESSO LIBERADO. INICIALIZANDO...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("CHAVE DE ACESSO INCORRETA.")
            else:
                st.error("USERNAME NÃO LOCALIZADO.")
        st.stop()
            
    elif modo_tela == "REGISTRAR NOVA CONTA":
        st.markdown("### 👋 CRIAR NOVA CONTA")
        novo_nome = st.text_input("COMO O JARVIS DEVE TE CHAMAR?")
        novo_user = st.text_input("ESCOLHA UM USERNAME (SEM ESPAÇOS):").strip().lower()
        nova_senha = st.text_input("DEFINA SUA SENHA DE SEGURANÇA:", type="password")
        confirmar_senha = st.text_input("CONFIRME A SENHA:", type="password")
        
        if st.button("FINALIZAR CADASTRO DE OPERADOR"):
            if not novo_nome or not novo_user or not nova_senha:
                st.error("TODOS OS CAMPOS PRECISAM ESTAR PREENCHIDOS.")
            elif novo_user in usernames_db:
                st.error("ESTE USERNAME JÁ EXISTE.")
            elif nova_senha != confirmar_senha:
                st.error("AS SENHAS NÃO COINCIDEM.")
            else:
                usernames_db[novo_user] = {"name": novo_nome.upper(), "password": gerar_hash_sha256(nova_senha)}
                salvar_novas_credenciais(usernames_db)
                st.success(f"CONTA PARA '{novo_nome.upper()}' CRIADA COM SUCESSO!")
        st.stop()

# ==================== SESSÃO OPERACIONAL DE USUÁRIO ====================
username = st.session_state.username

if st.session_state.autenticado and username:
    name = usernames_db[username]["name"]
    ARQUIVO_DADOS = f"dados_user_{username}.json"
    ARQUIVO_TOKEN_GOOGLE = f"token_google_{username}.json"

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
        st.session_state.messages = [{"role": "assistant", "content": f"Sistemas prontos, {name}! Diga-me o que deseja planejar hoje."}]

    if "cal_version" not in st.session_state: st.session_state.cal_version = 0
    if "pomo_segundos_restantes" not in st.session_state: st.session_state.pomo_segundos_restantes = 1500
    if "pomo_rodando" not in st.session_state: st.session_state.pomo_rodando = False
    if "pomo_tempo_inicial_escolhido" not in st.session_state: st.session_state.pomo_tempo_inicial_escolhido = 25
    if "eventos_locais" not in db: db["eventos_locais"] = []

    # --- HEADER ---
    col_titulo_sistema, col_botao_logout = st.columns([4, 1])
    with col_titulo_sistema:
        st.markdown("""<h1 class='custom-title' style='margin-bottom: 0px !important;'>🔱 <span class='jarvis-brand'>JARVIS OS</span></h1>""", unsafe_allow_html=True)
    with col_botao_logout:
        if st.button("SAIR DA SESSÃO"):
            st.session_state.autenticado = False
            st.session_state.username = None
            st.rerun()

    st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: rgba(212,175,55,0.15);'>", unsafe_allow_html=True)

    def obter_servico_google_agenda():
        if not os.path.exists(ARQUIVO_TOKEN_GOOGLE):
            return None
        try:
            creds = Credentials.from_authorized_user_file(ARQUIVO_TOKEN_GOOGLE, SCOPES)
            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
                with open(ARQUIVO_TOKEN_GOOGLE, "w") as f:
                    f.write(creds.to_json())
            return build('calendar', 'v3', credentials=creds)
        except:
            return None

    service = obter_servico_google_agenda()

    def processar_comando_e_criar_metas(comando):
        data_hoje_str = datetime.date.today().isoformat()
        prompt_sistema = f"""
        Você é o Jarvis, o assistente pessoal de alta tecnologia do usuário.
        Seu objetivo é analisar a mensagem do usuário e decidir se deve criar uma meta no painel e/ou eventos no Google Agenda.
        Considere que a data de HOJE é {data_hoje_str}.
        
        Você DEVE responder ESTRITAMENTE no formato JSON padrão.
        """
        try:
            completion = client.chat.completions.create(
                model=MODELO_IA,
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": comando}],
                temperature=0.3,
                response_format={ "type": "json_object" }
            )
            resultado = json.loads(completion.choices[0].message.content)
            
            if resultado.get("criar_meta") and resultado.get("novas_metas"):
                for nova_m in resultado["novas_metas"]:
                    db["metas"].append({
                        "id": str(time.time() + len(db["metas"])), "nome": nova_m["nome"],
                        "categoria": nova_m["categoria"], "concluida": False, "tempo_dedicado": 0
                    })
                salvar_dados(db)
                st.toast("🎯 Novas metas adicionadas!")
            return resultado.get("resposta_chat", "Comando processado com sucesso!")
        except:
            return "Sistemas operando localmente."

    # ==================== INTERFACE INTERATIVA ====================
    aba_metas, aba_pomodoro, aba_saude, aba_calendario, aba_graficos = st.tabs([
        "💬 CONVERSA & METAS", "⏱️ TIMER DE FOCO", "🥗 SAÚDE & FITNESS", "📅 AGENDA", "📊 ESTATÍSTICAS"
    ])

    # 1. ABA DE METAS
    with aba_metas:
        col_ia, col_lista = st.columns([1, 1])
        with col_ia:
            st.markdown('<div class="titulo-card">🔱 CONVERSAR COM O JARVIS</div>', unsafe_allow_html=True)
            chat_container = st.container(height=340)
            with chat_container:
                for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
            if prompt := st.chat_input("Envie uma mensagem..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                resposta = processar_comando_e_criar_metas(prompt)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                st.rerun()
        with col_lista:
            st.markdown('<div class="titulo-card">🎯 SEUS OBJETIVOS ATIVOS</div>', unsafe_allow_html=True)
            metas_ativas = [m for m in db["metas"] if not m["concluida"]]
            if not metas_ativas: st.info("Nenhuma diretriz ativa no momento.")
            else:
                for m in db["metas"]:
                    if not m["concluida"]:
                        c1, c2, c3 = st.columns([3, 1, 1])
                        c1.markdown(f"✨ **{m['nome']}**<br><span style='color:#777777; font-size:13px;'>{m['categoria']}</span>", unsafe_allow_html=True)
                        c2.markdown(f"<div style='padding-top:10px; color:#d4af37; font-weight:700;'>{m['tempo_dedicado']} min</div>", unsafe_allow_html=True)
                        if c3.button("✓", key=m["id"]):
                            m["concluida"] = True
                            salvar_dados(db)
                            st.rerun()

    # 2. ABA POMODORO
    with aba_pomodoro:
        st.markdown('<div class="titulo-card">⏱️ BLOCO DE FOCO INTEGRADO</div>', unsafe_allow_html=True)
        metas_validas = [m for m in db["metas"] if not m["concluida"]]
        if not metas_validas: st.warning("Crie uma meta com o Jarvis primeiro!")
        else:
            cp1, cp2 = st.columns(2)
            with cp1:
                meta_alvo = st.selectbox("Vincular foco atual à meta:", [m["nome"] for m in metas_validas])
                minutos_slider = st.slider("Duração do bloco (minutos):", min_value=1, max_value=120, value=int(st.session_state.pomo_tempo_inicial_escolhido), disabled=st.session_state.pomo_rodando)
                if not st.session_state.pomo_rodando and st.session_state.pomo_tempo_inicial_escolhido != minutos_slider:
                    st.session_state.pomo_tempo_inicial_escolhido = minutos_slider
                    st.session_state.pomo_segundos_restantes = minutos_slider * 60
                b1, b2 = st.columns(2)
                if not st.session_state.pomo_rodando:
                    if b1.button("▶ INICIAR"): st.session_state.pomo_rodando = True; st.rerun()
                else:
                    if b1.button("⏸ PAUSAR"): st.session_state.pomo_rodando = False; st.rerun()
                if b2.button("Automático" if st.session_state.pomo_rodando else "🔄 RESETAR"):
                    st.session_state.pomo_rodando = False
                    st.session_state.pomo_segundos_restantes = st.session_state.pomo_tempo_inicial_escolhido * 60
                    st.rerun()
            with cp2:
                m_vis, s_vis = divmod(st.session_state.pomo_segundos_restantes, 60)
                st.markdown(f"<div style='text-align: center;';><span style='color:#777777; font-size:14px; font-weight:600; text-transform: uppercase;'>Timer Correndo</span><h1 style='font-size: 82px; font-family: 'Kanit', sans-serif; font-weight:700; margin: 10px 0; background: linear-gradient(135deg, #ffffff 40%, #d4af37 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{m_vis:02d}:{s_vis:02d}</h1><span style='color:#d4af37; font-size:16px; font-weight:700;'>🎯 {meta_alvo}</span></div>", unsafe_allow_html=True)
            
            if st.session_state.pomo_rodando and st.session_state.pomo_segundos_restantes > 0:
                time.sleep(1)
                st.session_state.pomo_segundos_restantes -= 1
                if st.session_state.pomo_segundos_restantes == 0:
                    st.session_state.pomo_rodando = False
                    for m in db["metas"]:
                        if m["nome"] == meta_alvo and not m["concluida"]: m["tempo_dedicado"] += st.session_state.pomo_tempo_inicial_escolhido
                    db["historico_pomodoro"] += st.session_state.pomo_tempo_inicial_escolhido
                    salvar_dados(db)
                    st.balloons()
                st.rerun()

    # 3. ABA SAÚDE
    with aba_saude:
        cs1, cs2 = st.columns(2)
        with cs1:
            st.markdown('<div class="titulo-card">💧 META DE HIDRATAÇÃO</div>', unsafe_allow_html=True)
            peso_texto = st.text_input("Seu peso atual (kg):", value=str(db.get("peso_usuario", 70.0)).replace('.', ','))
            try: peso_limpo = float(peso_texto.replace(',', '.'))
            except ValueError: peso_limpo = 70.0
            if peso_limpo != db.get("peso_usuario", 70.0) and peso_limpo > 0: 
                db["peso_usuario"] = peso_limpo; salvar_dados(db); st.rerun()
            alvo_calculado = int(peso_limpo * 35)
            st.metric("Consumo de Hoje", f"{db['agua']} ml", f"Alvo Recomendado: {alvo_calculado} ml")
            c_btn1, c_btn2 = st.columns(2)
            if c_btn1.button("➕ Beber Copo (250ml)"): db["agua"] += 250; salvar_dados(db); st.rerun()
            if c_btn2.button("🔄 Zerar Dia"): db["agua"] = 0; salvar_dados(db); st.rerun()
        with cs2:
            st.markdown('<div class="titulo-card">🍳 FEED DE NUTRIÇÃO</div>', unsafe_allow_html=True)
            refeicao = st.text_input("O que você consumiu na última janela?", placeholder="Ex: Patinho, arroz integral e brócolis")
            if st.button("Postar Refeição no Log"):
                if refeicao: 
                    db["refeicoes"].append({"data": str(datetime.date.today()), "item": refeicao})
                    salvar_dados(db)
                    st.toast("Refeição registrada!")

    # 4. ABA CRONOGRAMA OPERACIONAL (CORRIGIDA E LOCALIZADA)
    with aba_calendario:
        st.markdown('<div class="titulo-card">📅 SEU CRONOGRAMA DE ATIVIDADES</div>', unsafe_allow_html=True)
        col_esq_info, col_dir_cal = st.columns([1, 2])
        
        # --- Tratamento de Variáveis Antecipado para Evitar o NameError ---
        dia_num_hoje = datetime.date.today().strftime("%d")
        
        dias_semana_pt = {
            "Monday": "SEGUNDA-FEIRA", "Tuesday": "TERÇA-FEIRA", "Wednesday": "QUARTA-FEIRA",
            "Thursday": "QUINTA-FEIRA", "Friday": "SEXTA-FEIRA", "Saturday": "SÁBADO", "Sunday": "DOMINGO"
        }
        dia_en = datetime.date.today().strftime("%A")
        dia_name_hoje = dias_semana_pt.get(dia_en, dia_en.upper())
        
        with col_esq_info:
            st.markdown(f"""
                <div style='background-color: #101010; padding: 30px; border-radius: 16px; border-left: 4px solid #d4af37; margin-bottom: 20px;'>
                    <span style='color: #777777; font-size: 14px; font-weight:600; text-transform:uppercase;'>Data Atual</span>
                    <h1 style='font-size: 90px; font-family: "Kanit", sans-serif; font-weight: 700; line-height:0.9; margin: 10px 0; color: #ffffff;'>{dia_num_hoje}</h1>
                    <div style='font-size: 18px; font-family: "Kanit", sans-serif; color: #d4af37; font-weight:500; margin-bottom: 25px;'>{dia_name_hoje}</div>
                    <div style='font-size: 14px; color: #e5e5e5; font-weight: 500;'>
                        📌 <span>{len(db.get("eventos_locais", []))} compromissos</span> agendados no sistema local.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("➕ GERENCIAR EVENTOS MANUALMENTE", expanded=False):
                nome_evento = st.text_input("Título:", placeholder="Ex: Reunião Geral")
                data_evento = st.date_input("Data:", datetime.date.today())
                h_ini = st.time_input("Início:", datetime.time(14, 0))
                h_fim = st.time_input("Término:", datetime.time(15, 0))
                
                if st.button("Salvar Evento"):
                    if nome_evento:
                        start_dt = datetime.datetime.combine(data_evento, h_ini)
                        end_dt = datetime.datetime.combine(data_evento, h_fim)
                        id_unico = "jarvis_" + str(int(time.time())) + "_manual"
                        titulo_formatated = f"{h_ini.strftime('%H:%M')} - {nome_evento}"
                        
                        novo_ev = {
                            "id": id_unico, "title": titulo_formatated, "start": start_dt.isoformat(), "end": end_dt.isoformat(), 
                            "backgroundColor": "#121212", "borderColor": "#d4af37", "textColor": "#d4af37"
                        }
                        db["eventos_locais"].append(novo_ev)
                        salvar_dados(db)
                        st.rerun()

        with col_dir_cal:
            eventos_para_exibir = [{
                "title": "🎬 Dia Iniciado",
                "start": datetime.datetime.combine(datetime.date.today(), datetime.time(6, 0)).isoformat(),
                "end": datetime.datetime.combine(datetime.date.today(), datetime.time(6, 30)).isoformat(),
                "backgroundColor": "#141414", "borderColor": "rgba(212,175,55,0.2)", "textColor": "#ffffff"
            }]
            if db.get("eventos_locais"): eventos_para_exibir.extend(db["eventos_locais"])

            # Renderização com contêiner estilizado baseado no SCSS
            st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
            calendar(events=eventos_para_exibir, options={
                "initialView": "dayGridMonth",
                "headerToolbar": {"left": "prev,next today", "center": "title", "right": ""},
                "locale": "pt-br"
            }, key=f"cal_widget_{st.session_state.cal_version}")
            st.markdown('</div>', unsafe_allow_html=True)

    # 5. ABA ESTATÍSTICAS
    with aba_graficos:
        st.markdown('<div class="titulo-card">📊 SEUS RELATÓRIOS INTEGRADOS</div>', unsafe_allow_html=True)
        if db.get("metas"):
            concluidas = sum(1 for m in db["metas"] if m["concluida"])
            total = len(db["metas"])
            st.progress(concluidas / total if total > 0 else 0)
            st.metric("Metas Completadas", f"{concluidas}/{total}", f"Foco acumulado: {db.get('historico_pomodoro', 0)} min")
