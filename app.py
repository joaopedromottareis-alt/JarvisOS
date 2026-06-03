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

# ==================== CONFIGURAÇÃO VISUAL MODERNA (ESTILO REDES SOCIAIS) ====================
st.set_page_config(page_title="Jarvis OS", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# CSS Global Unificado - Estilo TikTok, Instagram e YouTube Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Configuração Base do Sistema com Efeito de Luzes em Degradê Borrado no Fundo */
    .stApp { 
        background-color: #0b0c10; 
        color: #f3f4f6; 
        font-family: 'Plus Jakarta Sans', sans-serif;
        position: relative;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: "";
        position: absolute;
        width: 400px;
        height: 400px;
        top: -150px;
        left: -150px;
        background: radial-gradient(circle, rgba(255,0,128,0.2) 0%, rgba(0,0,0,0) 70%);
        filter: blur(160px);
        z-index: -1;
    }

    .stApp::after {
        content: "";
        position: absolute;
        width: 500px;
        height: 500px;
        bottom: -100px;
        right: -100px;
        background: radial-gradient(circle, rgba(122,0,255,0.18) 0%, rgba(0,0,0,0) 70%);
        filter: blur(160px);
        z-index: -1;
    }
    
    /* Ocultar elementos nativos desnecessários */
    [data-testid="stSidebarCollapsedControl"], [data-testid="stSidebar"], #MainMenu, footer, header {
        display: none !important;
    }
    
    .block-container { 
        padding: 2.5rem 4rem !important; 
        max-width: 100% !important; 
    }
    
    /* Títulos Estilo "Pop/Cartoonizado" e Amigável */
    h1, h2, h3, h4 { 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: linear-gradient(45deg, #ff007f, #7a00ff, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important; 
        letter-spacing: -0.5px !important;
        margin-bottom: 20px !important;
    }
    
    /* Cards de Seções Estilo Aplicativo Moderno (Glassmorphism Suave) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(22, 24, 35, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }

    .titulo-card { 
        color: #fe2c55 !important; /* Cor assinatura TikTok */
        font-size: 14px !important; 
        font-weight: 700 !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Inputs Arredondados e menos Secos */
    div[data-baseweb="select"], 
    div[data-baseweb="input"], 
    .stTextInput>div>div>input, 
    .stDateInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #1e1f24 !important; 
        border: 2px solid transparent !important; 
        border-radius: 14px !important; 
        color: #ffffff !important;
        padding: 4px 8px !important;
        transition: all 0.3s ease;
    }
    
    div[data-baseweb="input"]:focus-within, .stTextInput>div>div>input:focus {
        border-color: #7a00ff !important;
        box-shadow: 0 0 12px rgba(122, 0, 255, 0.4) !important;
    }

    /* Botões Pílula (Estilo Instagram/YouTube) */
    .stButton>button { 
        background: linear-gradient(45deg, #7a00ff, #ff007f) !important; 
        color: #ffffff !important; 
        border: none !important;
        border-radius: 50px !important; 
        padding: 12px 24px !important; 
        font-weight: 700 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(255, 0, 127, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .stButton>button:hover { 
        transform: scale(1.03) !important;
        box-shadow: 0 6px 20px rgba(255, 0, 127, 0.5) !important;
    }
    .stButton>button:active {
        transform: scale(0.98) !important;
    }
    
    /* Abas Superiores Estilo Cápsulas do YouTube */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: rgba(255, 255, 255, 0.03) !important; 
        border-radius: 50px !important;
        padding: 6px !important;
        gap: 10px !important;
        border-bottom: none !important;
        margin-bottom: 35px !important;
    }
    .stTabs [data-baseweb="tab"] { 
        color: #a6a7ab !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        border: none !important;
        background-color: transparent !important;
        padding: 10px 22px !important;
        border-radius: 50px !important;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] { 
        color: #ffffff !important; 
        background-color: #2a2b36 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    .stExpander {
        background-color: #161823 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 16px !important;
    }

    /* Moldura Suave do Calendário */
    .calendar-container {
        background-color: #121318 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 24px !important;
        padding: 25px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4) !important;
    }

    iframe[title="streamlit_calendar.calendar"] {
        border: none !important;
        background-color: transparent !important;
        min-height: 700px !important;
        height: 700px !important;
    }

    .logout-container {
        display: flex;
        justify-content: flex-end;
    }
    
    /* Estilização Amigável dos Chats */
    [data-testid="stChatMessage"] {
        background-color: #1e1f24 !important;
        border-radius: 16px !important;
        padding: 12px !important;
        margin-bottom: 10px !important;
    }
    
    /* Balão de Métrica */
    div[data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: #00f2fe !important;
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

# Captura de retorno do OAuth do Google na URL
query_params = st.query_params
if "code" in query_params and "state" in st.session_state and st.session_state.get("aguardando_oauth_user"):
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

if not st.session_state.autenticado:
    st.markdown("<h2>✨ ENTRAR NO JARVIS OS</h2>", unsafe_allow_html=True)
    modo_tela = st.radio("SELECIONE A OPERAÇÃO:", ["LOGIN", "REGISTRAR NOVA CONTA"], horizontal=True)
    
    if modo_tela == "LOGIN":
        with st.container(border=True):
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
        with st.container(border=True):
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

# ==================== INÍCIO DA SESSÃO DO USUÁRIO LOGADO ====================
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

    # ==================== HEADER OPERACIONAL COM LOGOUT ====================
    col_titulo_sistema, col_botao_logout = st.columns([4, 1])
    with col_titulo_sistema:
        st.markdown("""<h1 style='margin-bottom: 0px !important;'>🚀 JARVIS OS</h1>""", unsafe_allow_html=True)
    with col_botao_logout:
        st.markdown("<div class='logout-container'></div>", unsafe_allow_html=True)
        if st.button("SAIR DA SESSÃO"):
            st.session_state.autenticado = False
            st.session_state.username = None
            st.rerun()

    st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

    # ==================== MOTOR DE AGENDA MULTIUSUÁRIO WEB ====================
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

    # ==================== CÉREBRO INTEGRADO DO JARVIS ====================
    def processar_comando_e_criar_metas(comando):
        data_hoje_str = datetime.date.today().isoformat()
        prompt_sistema = f"""
        Você é o Jarvis, o assistente pessoal de alta tecnologia do usuário.
        Seu objetivo é analisar a mensagem do usuário e decidir se deve criar uma meta no painel e/ou eventos no Google Agenda.
        Considere que a data de HOJE é {data_hoje_str}.
        
        Se o usuário pedir para agendar algo que dure vários dias, identifique a "data_inicio" e a "data_fim". 
        Se for apenas um dia, coloque a mesma data em ambos os campos.
        
        REGRA CRÍTICA PARA O TÍTULO DO EVENTO:
        Você DEVE obrigatoriamente incluir a hora de início no início do título do evento (ex: "15:00 - Ocupado"). Se não houver hora combinada, use "00:00 - Título".
        
        Você DEVE responder ESTRITAMENTE no formato JSON abaixo:
        {{
            "resposta_chat": "Sua resposta estilosa e amigável.",
            "criar_meta": true ou false,
            "novas_metas": [
                {{ "nome": "Nome curto da meta", "categoria": "Estudos", "Saúde", "Alimentação" ou "Trabalho" }}
            ],
            "criar_agenda": true ou false,
            "evento_agenda": {{
                "titulo": "HH:MM - Título do compromisso",
                "data_inicio": "AAAA-MM-DD",
                "data_fim": "AAAA-MM-DD",
                "hora_inicio": "HH:MM",
                "hora_fim": "HH:MM"
            }}
        }}
        Mensagem do usuário: "{comando}"
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
                        "id": str(time.time() + len(db["metas"])),
                        "nome": nova_m["nome"],
                        "categoria": nova_m["categoria"],
                        "concluida": False,
                        "tempo_dedicado": 0
                    })
                salvar_dados(db)
                st.toast("🎯 Novas metas adicionadas ao seu feed!")
                
            if resultado.get("criar_agenda") and resultado.get("evento_agenda"):
                ev = resultado["evento_agenda"]
                try:
                    d_ini = datetime.datetime.strptime(ev["data_inicio"], "%Y-%m-%d").date()
                    d_fim = datetime.datetime.strptime(ev["data_fim"], "%Y-%m-%d").date()
                    inicio_parsed = datetime.datetime.strptime(ev["hora_inicio"], "%H:%M").time()
                    fim_parsed = datetime.datetime.strptime(ev["hora_fim"], "%H:%M").time()
                    
                    dia_atual = d_ini
                    timestamp_base = int(time.time())
                    contador_id = 0
                    
                    while dia_atual <= d_fim:
                        start_dt = datetime.datetime.combine(dia_atual, inicio_parsed)
                        end_dt = datetime.datetime.combine(dia_atual, fim_parsed)
                        id_unico = f"jarvis_{timestamp_base}_{contador_id}"
                        
                        novo_ev = {
                            "id": id_unico, "title": ev["titulo"], "start": start_dt.isoformat(), 
                            "end": end_dt.isoformat(), "backgroundColor": "#7a00ff", "borderColor": "#ff007f", "textColor": "#ffffff"
                        }
                        db["eventos_locais"].append(novo_ev)
                        
                        if service:
                            try:
                                event_body = {
                                    'id': id_unico.replace("_", ""), 'summary': ev["titulo"],
                                    'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
                                    'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
                                }
                                service.events().insert(calendarId='primary', body=event_body).execute()
                            except: pass
                        
                        dia_atual += datetime.timedelta(days=1)
                        contador_id += 1
                    
                    salvar_dados(db)
                    st.toast("📅 Cronograma atualizado com sucesso!")
                    st.session_state.cal_version += 1
                except: pass
                    
            return resultado.get("resposta_chat", "Comando processado com sucesso!")
        except Exception as e:
            return "Conexão offline. Sistemas operando localmente."

    # ==================== INTERFACE WORKSTATION INTERATIVA ====================
    aba_metas, aba_pomodoro, aba_saude, aba_calendario, aba_graficos = st.tabs([
        "💬 CONVERSA & METAS", "⏱️ TIMER DE FOCO", "🥗 SAÚDE & FITNESS", "📅 AGENDA", "📊 ESTATÍSTICAS"
    ])

    # 1. ABA DE METAS
    with aba_metas:
        col_ia, col_lista = st.columns([1, 1])
        with col_ia:
            st.markdown('<div class="titulo-card">🤖 CONVERSAR COM O JARVIS</div>', unsafe_allow_html=True)
            with st.container(border=True):
                chat_container = st.container(height=340)
                with chat_container:
                    for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
                if prompt := st.chat_input("Envie uma mensagem ou peça para agendar algo..."):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    resposta = processar_comando_e_criar_metas(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                    st.rerun()
        with col_lista:
            st.markdown('<div class="titulo-card">🎯 SEUS OBJETIVOS ATIVOS</div>', unsafe_allow_html=True)
            with st.container(border=True):
                metas_ativas = [m for m in db["metas"] if not m["concluida"]]
                if not metas_ativas: st.info("Nenhuma diretriz ativa no momento. Que tal começar uma nova?")
                else:
                    for m in db["metas"]:
                        if not m["concluida"]:
                            c1, c2, c3 = st.columns([3, 1, 1])
                            c1.markdown(f"🔥 **{m['nome']}**<br><span style='color:#a6a7ab; font-size:13px;'>{m['categoria']}</span>", unsafe_allow_html=True)
                            c2.markdown(f"<div style='padding-top:10px; color:#00f2fe; font-weight:700;'>{m['tempo_dedicado']} min</div>", unsafe_allow_html=True)
                            if c3.button("✓", key=m["id"]):
                                m["concluida"] = True
                                salvar_dados(db)
                                st.rerun()
                            st.markdown("<hr style='margin: 12px 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

    # 2. ABA POMODORO
    with aba_pomodoro:
        st.markdown('<div class="titulo-card">⏱️ BLOCO DE FOCO ESTILO TIME-LAPSE</div>', unsafe_allow_html=True)
        metas_validas = [m for m in db["metas"] if not m["concluida"]]
        if not metas_validas: st.warning("Nenhum alvo ativo encontrado. Crie uma meta com o Jarvis primeiro!")
        else:
            cp1, cp2 = st.columns(2)
            with cp1:
                with st.container(border=True):
                    st.markdown("### ⚙️ Ajustar Foco")
                    meta_alvo = st.selectbox("Vincular foco atual à meta:", [m["nome"] for m in metas_validas])
                    minutos_slider = st.slider("Duração do bloco (minutos):", min_value=1, max_value=120, value=int(st.session_state.pomo_tempo_inicial_escolhido), disabled=st.session_state.pomo_rodando)
                    if not st.session_state.pomo_rodando and st.session_state.pomo_tempo_inicial_escolhido != minutos_slider:
                        st.session_state.pomo_tempo_inicial_escolhido = minutos_slider
                        st.session_state.pomo_segundos_restantes = minutos_slider * 60
                    st.markdown("<br>", unsafe_allow_html=True)
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
                with st.container(border=True):
                    m_vis, s_vis = divmod(st.session_state.pomo_segundos_restantes, 60)
                    st.markdown(f"<div style='text-align: center; padding: 15px 0;'><span style='color:#a6a7ab; font-size:14px; font-weight:600; text-transform: uppercase;'>Timer Correndo</span><h1 style='font-size: 82px; font-family: system-ui; font-weight:800; margin: 10px 0; background: linear-gradient(45deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{m_vis:02d}:{s_vis:02d}</h1><span style='color:#ff007f; font-size:16px; font-weight:700;'>🎯 {meta_alvo}</span></div>", unsafe_allow_html=True)
            
            if st.session_state.pomo_rodando and st.session_state.pomo_segundos_restantes > 0:
                time.sleep(1); st.session_state.pomo_segundos_restantes -= 1
                if st.session_state.pomo_segundos_restantes == 0:
                    st.session_state.pomo_rodando = False
                    tempo_minutos_ganhos = st.session_state.pomo_tempo_inicial_escolhido
                    for m in db["metas"]:
                        if m["nome"] == meta_alvo and not m["concluida"]: m["tempo_dedicado"] += tempo_minutos_ganhos
                    db["historico_pomodoro"] += tempo_minutos_ganhos
                    salvar_dados(db); st.balloons()
                st.rerun()

    # 3. ABA BIOMETRIA
    with aba_saude:
        cs1, cs2 = st.columns(2)
        with cs1:
            st.markdown('<div class="titulo-card">💧 META DE HIDRATAÇÃO (STREAK)</div>', unsafe_allow_html=True)
            with st.container(border=True):
                peso_texto = st.text_input("Seu peso atual (kg):", value=str(db.get("peso_usuario", 70.0)).replace('.', ','))
                try: peso_limpo = float(peso_texto.replace(',', '.'))
                except ValueError: peso_limpo = 70.0
                if peso_limpo != db.get("peso_usuario", 70.0) and peso_limpo > 0: 
                    db["peso_usuario"] = peso_limpo; salvar_dados(db); st.rerun()
                alvo_calculado = int(peso_limpo * 35)
                st.markdown("<br>", unsafe_allow_html=True)
                st.metric("Consumo de Hoje", f"{db['agua']} ml", f"Alvo Recomendado: {alvo_calculado} ml")
                st.markdown("<br>", unsafe_allow_html=True)
                c_btn1, c_btn2 = st.columns(2)
                if c_btn1.button("➕ Beber Copo (250ml)"): db["agua"] += 250; salvar_dados(db); st.rerun()
                if c_btn2.button("🔄 Zerar Dia"): db["agua"] = 0; salvar_dados(db); st.rerun()
        with cs2:
            st.markdown('<div class="titulo-card">🍳 FEED DE NUTRIÇÃO</div>', unsafe_allow_html=True)
            with st.container(border=True):
                refeicao = st.text_input("O que você comeu agora?", placeholder="Ex: Panqueca de aveia e whey")
                st.markdown("<br><br>", unsafe_allow_html=True)
                if st.button("Postar Refeição no Log"):
                    if refeicao: 
                        db["refeicoes"].append({"data": str(datetime.date.today()), "item": refeicao})
                        salvar_dados(db)
                        st.toast("Refeição registrada!")

    # 4. ABA CRONOGRAMA OPERACIONAL
    with aba_calendario:
        st.markdown('<div class="titulo-card">📅 SEU CRONOGRAMA DE ATIVIDADES</div>', unsafe_allow_html=True)
        
        if service:
            st.markdown("<span style='color: #00f2fe; font-size: 14px; font-weight:600; margin-bottom:10px; display:inline-block;'>⚡ Google Agenda Sincronizado</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: #ff007f; font-size: 14px; font-weight:600; margin-bottom:10px; display:inline-block;'>⚠️ Modo Offline Local</span>", unsafe_allow_html=True)
            
            if st.button("CONECTAR COM GOOGLE AGENDA"):
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
                    auth_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
                    
                    st.session_state.aguardando_oauth_user = username
                    st.markdown(f'<a href="{auth_url}" target="_self"><input type="button" value="Autorizar Google" style="background:linear-gradient(45deg, #7a00ff, #ff007f); color:#ffffff; border:none; padding:12px 24px; border-radius:50px; font-weight:bold; cursor:pointer; width:100%;"></a>', unsafe_allow_html=True)
                except Exception as e:
                    st.error("Configure os Secrets do Streamlit para ativar a API.")

        eventos_para_exibir = [{
            "title": "🎬 Dia Iniciado",
            "start": datetime.datetime.combine(datetime.date.today(), datetime.time(6, 0)).isoformat(),
            "end": datetime.datetime.combine(datetime.date.today(), datetime.time(6, 30)).isoformat(),
            "backgroundColor": "#1e1f24", "borderColor": "#rgba(255,255,255,0.1)", "textColor": "#a6a7ab", "editable": False
        }]
        if db.get("eventos_locais"): eventos_para_exibir.extend(db["eventos_locais"])

        with st.expander("➕ CRIAR OU EXCLUIR COMPROMISSOS MANUALMENTE", expanded=False):
            c_add, c_del = st.columns(2)
            with c_add:
                st.markdown("#### Adicionar Evento")
                nome_evento = st.text_input("Título do compromisso:", placeholder="Ex: Gravar conteúdo", key="cal_nome_ev")
                data_evento = st.date_input("Data:", datetime.date.today(), key="cal_data_ev")
                h_ini = st.time_input("Início:", datetime.time(14, 0), key="cal_hini_ev")
                h_fim = st.time_input("Término:", datetime.time(15, 0), key="cal_hfim_ev")
                recorrente = st.checkbox("Repetir diariamente", key="cal_rec_ev")
                
                if st.button("Salvar na Agenda", key="cal_save_btn"):
                    if nome_evento:
                        start_dt = datetime.datetime.combine(data_evento, h_ini)
                        end_dt = datetime.datetime.combine(data_evento, h_fim)
                        id_unico = "jarvis_" + str(int(time.time())) + "_manual"
                        titulo_formatado = f"{h_ini.strftime('%H:%M')} - {nome_evento}"
                        
                        novo_ev = {"id": id_unico, "title": titulo_formatado, "start": start_dt.isoformat(), "end": end_dt.isoformat(), "backgroundColor": "#7a00ff", "borderColor": "#ff007f", "textColor": "#ffffff"}
                        
                        if service:
                            try:
                                event_body = {'id': id_unico.replace("_", ""), 'summary': titulo_formatado, 'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'}, 'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'}}
                                if recorrente: event_body['recurrence'] = ['RRULE:FREQ=DAILY']
                                service.events().insert(calendarId='primary', body=event_body).execute()
                            except: pass
                        
                        db["eventos_locais"].append(novo_ev); salvar_dados(db); st.session_state.cal_version += 1; st.rerun()

            with c_del:
                st.markdown("#### Remover Evento")
                opcoes_remocao = {}
                for idx, ev in enumerate(eventos_para_exibir):
                    if ev.get("editable") != False:
                        ev_id = ev.get("id", f"antigo_{idx}")
                        opcoes_remocao[ev_id] = ev.get("title", f"Compromisso ({idx})")
                
                if opcoes_remocao:
                    evento_para_remover = st.selectbox("Escolha qual deseja remover:", options=list(opcoes_remocao.keys()), format_func=lambda x: opcoes_remocao[x], key="cal_del_select")
                    if st.button("Apagar Evento Selecionado", key="cal_del_btn"):
                        if service and not evento_para_remover.startswith("antigo_"):
                            try: service.events().delete(calendarId='primary', eventId=evento_para_remover.replace("jarvis_", "").split("_")[0]).execute()
                            except: pass
                        db["eventos_locais"] = [e for e in db["eventos_locais"] if e.get("id") != evento_para_remover]
                        salvar_dados(db); st.session_state.cal_version += 1; st.rerun()
                else:
                    st.info("Nenhum evento customizado para remover.")

        st.markdown("<div class='calendar-container'>", unsafe_allow_html=True)
        calendar(events=eventos_para_exibir, options={"initialView": "dayGridMonth", "headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek,timeGridDay"}}, key=f"calendar_widget_{st.session_state.cal_version}")
        st.markdown("</div>", unsafe_allow_html=True)

    # 5. ABA DE GRÁFICOS E METRICAS INTERATIVAS
    with aba_graficos:
        st.markdown('<div class="titulo-card">📊 SEUS ANALYTICS INTERATIVOS</div>', unsafe_allow_html=True)
        
        cg1, cg2 = st.columns(2)
        with cg1:
            with st.container(border=True):
                st.markdown("### 🔥 Produtividade (Minutos de Foco)")
                total_pomo = db.get("historico_pomodoro", 0)
                st.metric("Total Acumulado", f"{total_pomo} min", "Foco Contínuo")
                
                metas_nome = [m["nome"] for m in db["metas"]]
                metas_valores = [m["tempo_dedicado"] for m in db["metas"]]
                
                if any(metas_valores):
                    fig_pomo = go.Figure(data=[go.Bar(
                        x=metas_nome, y=metas_valores,
                        marker_color=['#7a00ff', '#ff007f', '#00f2fe', '#00ff7f'][:len(metas_nome)]
                    )])
                    fig_pomo.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig_pomo, use_container_width=True)
                else:
                    st.info("Gere dados completando ciclos no cronômetro.")
                    
        with cg2:
            with st.container(border=True):
                st.markdown("### 🏆 Conclusão de Metas")
                concluidas = len([m for m in db["metas"] if m["concluida"]])
                total_metas = len(db["metas"])
                
                if total_metas > 0:
                    fig_meta = go.Figure(data=[go.Pie(
                        labels=["Concluídas", "Pendentes"], 
                        values=[concluidas, total_metas - concluidas],
                        hole=.6,
                        marker_colors=['#00f2fe', '#1e1f24']
                    )])
                    fig_meta.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig_meta, use_container_width=True)
                else:
                    st.info("Peça ao Jarvis para listar objetivos estratégicos para você.")
