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

# CSS Customizado Estabilizado e Nivelado
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
    
    div[data-testid="stHorizontalBlock"] {
        gap: 2rem !important;
        width: 100% !important;
    }

    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
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
    
    .stTextInput input, .stDateInput input, .stTextArea textarea, div[data-baseweb="select"], div[role="button"], .stNumberInput input {
        background-color: #0b0b0b !important; 
        border: 1px solid rgba(212, 175, 55, 0.3) !important; 
        border-radius: 12px !important; 
        color: #ffffff !important;
        padding: 10px 16px !important;
        width: 100% !important;
    }
    
    div[data-testid="stTextInput"] label {
        display: none !important;
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
        gap: 10px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.15) !important;
        padding-bottom: 8px;
    }

    .btn-seta-enviar button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important; 
        color: #000000 !important; 
        border: none !important;
        border-radius: 12px !important; 
        padding: 10px 0px !important; 
        font-weight: 700 !important; 
        width: 100% !important;
        font-size: 18px !important;
    }

    .stButton>button { 
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%) !important; 
        color: #000000 !important; 
        border: none !important;
        border-radius: 12px !important; 
        padding: 12px 24px !important; 
        font-weight: 700 !important; 
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        margin-bottom: 30px !important;
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab"] { 
        color: #777777 !important; 
        font-family: 'Kanit', sans-serif !important;
        flex-grow: 1 !important;
        text-align: center !important;
    }
    
    .stTabs [aria-selected="true"] { 
        color: #d4af37 !important; 
    }
    
    [data-testid="stChatMessage"] {
        background-color: rgba(20, 20, 20, 0.5) !important;
        border-left: 3px solid #d4af37 !important;
    }

    /* ESTE TRUQUE EXPULSA O ESPAÇO VAZIO SUPERIOR DO BOTÃO DE ATUALIZAR DA AGENDA */
    .subir-bloco-agenda {
        margin-top: -66px !important;
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
                
            st.success("✓ Integração com o Google Agenda realizada com sucesso durante o registro!")
            st.info("Faça o login agora para acessar sua conta integrada.")
            st.query_params.clear() 
            time.sleep(2)
        except Exception as e:
            st.error(f"Erro ao salvar token do Google: {e}")

# --- TELA DE LOGIN / REGISTRO ---
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
        st.markdown("### CRIAR NOVA CONTA INTEGRADA COM GOOGLE")
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
                
                st.success("Conta Local criada! Redirecionando para a Google para ativação do Calendário...")
                st.markdown(f'<meta http-equiv="refresh" content="1;url={auth_url}">', unsafe_allow_html=True)
                st.markdown(f"[Se não for redirecionado automaticamente, clique aqui para Autenticar]({auth_url})")
        st.stop()

# ==================== SESSÃO OPERACIONAL DE USUÁRIO ====================
username = st.session_state.username

if st.session_state.autenticado and username:
    name = usernames_db[username]["name"]
    ARQUIVO_DADOS = f"dados_user_{username}.json"
    TOKEN_GOOGLE_USER = f"token_user_{username}.json"

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
        st.session_state.messages = [{"role": "assistant", "content": f"Sistemas online, {name}! Sua Agenda Google vinculada está ativa."}]

    if "pomo_segundos_restantes" not in st.session_state: st.session_state.pomo_segundos_restantes = 1500
    if "pomo_rodando" not in st.session_state: st.session_state.pomo_rodando = False
    if "pomo_tempo_inicial_escolhido" not in st.session_state: st.session_state.pomo_tempo_inicial_escolhido = 25
    if "eventos_locais" not in db: db["eventos_locais"] = []

    def obter_servico_google_calendar():
        creds = None
        if os.path.exists(TOKEN_GOOGLE_USER):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_GOOGLE_USER, SCOPES)
            except Exception:
                creds = None
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(TOKEN_GOOGLE_USER, 'w') as token:
                        token.write(creds.to_json())
                except Exception:
                    creds = None
            
            if not creds:
                st.warning("⚠️ Seu Google Agenda não está vinculado a este operador. Vá até a aba da Agenda para configurar.")
                return None
        
        return build('calendar', 'v3', credentials=creds)

    def enviar_evento_para_google(titulo, data_str, horario_str):
        service = obter_servico_google_calendar()
        if not service: return False
        try:
            start_datetime = f"{data_str}T{horario_str}:00"
            horas, minutos = map(int, horario_str.split(':'))
            fim_horas = (horas + 1) % 24
            end_datetime = f"{data_str}T{fim_horas:02d}:{minutos:02d}:00"
            
            event = {
                'summary': titulo,
                'description': 'Agendado automaticamente via Jarvis OS',
                'start': {'dateTime': start_datetime, 'timeZone': 'America/Sao_Paulo'},
                'end': {'dateTime': end_datetime, 'timeZone': 'America/Sao_Paulo'},
            }
            service.events().insert(calendarId='primary', body=event).execute()
            return True
        except Exception as e:
            print(f"[Erro Google Calendar]: {e}")
            return False

    def puxar_eventos_do_google():
        service = obter_servico_google_calendar()
        if not service: return
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=20, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            
            db["eventos_locais"] = []
            for ev in events:
                start = ev['start'].get('dateTime', ev['start'].get('date'))
                data_limpa = start[:10]
                hora_limpa = start[11:16] if 'T' in start else "00:00"
                
                db["eventos_locais"].append({
                    "id": ev['id'],
                    "title": ev.get('summary', 'Compromisso Sem Título'),
                    "date": data_limpa,
                    "time": hora_limpa
                })
            salvar_dados(db)
        except Exception as e:
            print(f"[Erro ao puxar dados do Google]: {e}")

    # --- HEADER ---
    col_titulo_sistema, col_botao_logout = st.columns([5, 1])
    with col_titulo_sistema:
        header_dashboard = f"<h1 class='custom-title' style='margin-bottom: 0px !important;'>{ICONES['jarvis']} <span class='jarvis-brand'>JARVIS OS</span></h1>"
        st.markdown(header_dashboard, unsafe_allow_html=True)
    with col_botao_logout:
        if st.button("SAIR DA SESSÃO"):
            st.session_state.autenticado = False
            st.session_state.username = None
            st.rerun()

    st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: rgba(212,175,55,0.15);'>", unsafe_allow_html=True)

    def analisar_nutrientes_refeicao(descricao_refeicao):
        if not API_KEY or client is None:
            return {"calorias": 0, "carboidratos": 0, "proteinas": 0, "gorduras": 0}
            
        prompt_nutricional = (
            "Você é uma inteligência artificial especialista em nutrição e mapeamento de macroalimentos.\n"
            f"Sua tarefa é analisar a refeição descrita pelo usuário: '{descricao_refeicao}'.\n"
            "Estime os valores nutricionais gerais dessa porção padrão de forma assertiva e realista.\n\n"
            "Retorne OBRIGATORIAMENTE apenas um objeto JSON limpo com as seguintes chaves numéricas inteiras:\n"
            "{\n"
            "  \"calorias\": 150,\n"
            "  \"carboidratos\": 20,\n"
            "  \"proteinas\": 5,\n"
            "  \"gorduras\": 3\n"
            "}"
        )
        try:
            resposta_ia = client.chat.completions.create(
                model=MODELO_EXTRATOR,
                messages=[{"role": "system", "content": prompt_nutricional}, {"role": "user", "content": descricao_refeicao}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            return json.loads(resposta_ia.choices[0].message.content.strip())
        except Exception:
            return {"calorias": 0, "carboidratos": 0, "proteinas": 0, "gorduras": 0}

    def processar_comando_e_criar_metas(comando):
        data_hoje_str = datetime.date.today().isoformat()
        
        if not API_KEY or client is None:
            return " Falha nos Sistemas: Nenhuma chave configurada. Por favor, adicione a variável GROQ_API_KEY."

        prompt_sistema_chat = (
            f"Você é o Jarvis, um assistente executivo altamente avançado e refinado. O operador da account principal está registrado como: '{name}'. Hoje é {data_hoje_str}.\n"
            f"DIRETRIZES OBRIGATÓRIAS E CRÍTICAS DE IDENTIFICAÇÃO DE GÊNERO:\n"
            f"Antes de responder, analise o text digitado pelo usuário ('{comando}') E o nome da conta ('{name}').\n"
            f"1. Se o comando atual contiver referências explícitas à mãe do usuário, se o usuário disser que quem está falando é a mãe, uma mulher, ou usar saudações femininas, ou se o próprio nome '{name}' for feminino (ex: Maria, Ana, Paula, Mãe), você deve mudar IMEDIATAMENTE os pronomes para o FEMININO.\n"
            f"   - Sob condição feminina, use sempre: 'Senhora', 'atendê-la', 'pronta', 'minha senhora', 'comissionada'. Nunca, sob hipótese alguma, use 'Senhor' ou pronomes masculinos.\n"
            f"2. Caso o comando ou o nome sugiram gênero masculino (ex: João, admin, ou referências ao 'pai' ou 'filho'), use: 'Senhorn', 'atendê-lo', 'pronto', 'meu senhor'.\n"
            f"3. Responda com extrema imponência, elegance corporativa e formalidade britânica.\n"
            f"4. Se for solicitado o agendamento real de um evento, confirme de forma extremamente polida que a diretriz foi gravada na nuvem do Google Agenda."
        )
        
        try:
            conversa_principal = client.chat.completions.create(
                model=MODELO_PRINCIPAL,
                messages=[{"role": "system", "content": prompt_sistema_chat}, {"role": "user", "content": comando}],
                temperature=0.7
            )
            resposta_texto_jarvis = conversa_principal.choices[0].message.content.strip()
        except Exception as e:
            return f" Instabilidade nos Servidores: {str(e)}"

        try:
            prompt_sistema_extrator = (
                f"Você é uma inteligência de extração de dados and automação estruturada. Hoje é exatamente {data_hoje_str}.\n"
                "Analise minuciosamente o comando enviado pelo usuário e tome ações estruturadas in formato JSON.\n\n"
                "Regras Obrigatórias:\n"
                "1. Se o usuário pediu para adicionar, marcar, estudar, fazer, lembrar de algo, ou criar uma tarefa/meta, mude 'criar_meta' para true and inclua o objeto dentro de 'novas_metas'.\n"
                "2. Se o comando contiver referências de tempo ou data, você também deve mudar 'criar_evento' para true e gerar o item in 'novos_eventos' contendo a data YYYY-MM-DD e o horário HH:MM correspondentes.\n\n"
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
                for ev in resultado.get("novos_eventos", []):
                    if isinstance(ev, dict) and "title" in ev:
                        data_ev = ev.get("date", data_hoje_str)
                        hora_ev = ev.get("time", "12:00")
                        enviar_evento_para_google(ev["title"], data_ev, hora_ev)
                puxar_eventos_do_google()
                
        except Exception:
            pass
            
        return resposta_texto_jarvis

# ==================== DEFINIÇÃO GLOBAL DE DATAS ====================
    hoje = datetime.date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

# ==================== NAVEGAÇÃO POR ABAS ====================
    aba_metas, aba_pomodoro, aba_saude, aba_calendario = st.tabs([
        "CONVERSA & METAS", "TIMER DE FOCO", "SAÚDE & FITNESS", "AGENDA"
    ])

    # 1. CONVERSA & METAS (NIVELADO E SIMÉTRICO)
    with aba_metas:
        col_ia, col_lista = st.columns([1, 1.3])
        with col_ia:
            card_html = f'<div class="titulo-card">{ICONES["conversa"]} CONVERSAR COM O JARVIS</div>'
            st.markdown(card_html, unsafe_allow_html=True)
            
            chat_container = st.container(height=315)
            with chat_container:
                for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
            
            with st.container():
                c_txt, c_btn = st.columns([5.2, 0.8])
                with c_txt:
                    prompt = st.text_input("Envie uma instrução...", key="chat_prompt_input", label_visibility="collapsed", placeholder="Envie uma instrução...")
                with c_btn:
                    st.markdown('<div class="btn-seta-enviar">', unsafe_allow_html=True)
                    enviou_botao = st.button("▲", key="btn_enviar_chat")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if (prompt and st.session_state.get("ultimo_prompt_enviado") != prompt) or (enviou_botao and prompt):
                    st.session_state.ultimo_prompt_enviado = prompt
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    resposta = processar_comando_e_criar_metas(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                    st.rerun()
                    
        with col_lista:
            card_html = f'<div class="titulo-card">{ICONES["metas_caderno"]} OBJETIVOS ATIVOS</div>'
            st.markdown(card_html, unsafe_allow_html=True)
            
            metas_container = st.container(height=380)
            with metas_container:
                metas_ativas = [m for m in db["metas"] if not m["concluida"]]
                if not metas_ativas: st.info("Sem diretrizes ativas.")
                else:
                    for m in db["metas"]:
                        if not m["concluida"]:
                            c1, c2, c3 = st.columns([3, 1, 1])
                            c1.markdown(f"**{m['nome']}**<br><span style='color:#777777;'>{m['categoria']}</span>", unsafe_allow_html=True)
                            c2.markdown(f"<div style='padding-top:10px; color:#d4af37;'>{m['tempo_dedicado']} min</div>", unsafe_allow_html=True)
                            if c3.button("✓", key=m["id"]):
                                m["concluida"] = True; salvar_dados(db); st.rerun()

    # 2. POMODORO
    with aba_pomodoro:
        card_html = f'<div class="titulo-card">{ICONES["foco"]} TIMER DE FOCO</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        metas_validas = [m for m in db["metas"] if not m["concluida"]]
        if not metas_validas: st.warning("Nenhum objectivo ativo encontrado. Defina uma tarefa conversando com o Jarvis primeiro.")
        else:
            cp1, cp2 = st.columns([1, 1.3])
            with cp1:
                meta_alvo = st.selectbox("Selecione a tarefa ativa para focar:", [m["nome"] for m in metas_validas])
                
                minutos_digitados = st.number_input(
                    "Duração (em minutos):", 
                    min_value=1, 
                    max_value=120, 
                    value=int(st.session_state.pomo_tempo_inicial_escolhido), 
                    step=1,
                    disabled=st.session_state.pomo_rodando
                )
                
                if not st.session_state.pomo_rodando and st.session_state.pomo_tempo_inicial_escolhido != minutos_digitados:
                    st.session_state.pomo_tempo_inicial_escolhido = minutos_digitados
                    st.session_state.pomo_segundos_restantes = minutos_digitados * 60
                    
            b1, b2 = st.columns([1, 1])
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
                st.markdown(f"<div style='text-align: center; display: flex; flex-direction: column; justify-content: center; height: 100%; padding-top: 20px;'><h1 style='font-size: 75px; color:#ffffff; margin: 0;'>{m_vis:02d}:{s_vis:02d}</h1><span style='color:#d4af37; font-weight: 600; font-size: 16px; margin-top: 10px;'> {meta_alvo}</span></div>", unsafe_allow_html=True)
            
            if st.session_state.pomo_rodando and st.session_state.pomo_segundos_restantes > 0:
                time.sleep(1)
                st.session_state.pomo_segundos_restantes -= 1
                if st.session_state.pomo_segundos_restantes == 0:
                    st.session_state.pomo_rodando = False
                    for m in db["metas"]:
                        if m["nome"] == meta_alvo and not m["concluida"]: m["tempo_dedicado"] += st.session_state.pomo_tempo_inicial_escolhido
                    db["historico_pomodoro"] += st.session_state.pomo_tempo_inicial_escolhido
                    salvar_dados(db); st.balloons()
                st.rerun()

    # 3. SAÚDE & FITNESS 
    with aba_saude:
        cs1, cs2 = st.columns([1, 1.3])
        with cs1:
            card_html = f'<div class="titulo-card">{ICONES["saude"]} DIRETRIZES DE HIDRATAÇÃO</div>'
            st.markdown(card_html, unsafe_allow_html=True)
            peso_texto = st.text_input("Seu peso atual (kg):", value=str(db.get("peso_usuario", 70.0)))
            try: peso_limpo = float(peso_texto.replace(',', '.'))
            except: peso_limpo = 70.0
            db["peso_usuario"] = peso_limpo
            alvo_calc = int(peso_limpo * 35)
            st.metric("Consumido", f"{db['agua']} ml", f"Alvo do Jarvis: {alvo_calc} ml")
            cb1, cb2 = st.columns([1, 1])
            if cb1.button("➕ Copo (250ml)"): db["agua"] += 250; salvar_dados(db); st.rerun()
            if cb2.button("🔄 Limpar Registro"): db["agua"] = 0; salvar_dados(db); st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="titulo-card">{ICONES["saude"]} ACUMULADO NUTRICIONAL DO DIA</div>', unsafe_allow_html=True)
            
            refeicoes_hoje = [r for r in db.get("refeicoes", []) if r.get("data") == str(datetime.date.today())]
            
            total_cal = sum(int(r.get("calorias", 0)) for r in refeicoes_hoje)
            total_carbs = sum(int(r.get("carboidratos", 0)) for r in refeicoes_hoje)
            total_prot = sum(int(r.get("proteinas", 0)) for r in refeicoes_hoje)
            total_gord = sum(int(r.get("gorduras", 0)) for r in refeicoes_hoje)
            
            cm1, cm2 = st.columns([1, 1])
            cm1.metric("Energia Total", f"{total_cal} kcal")
            cm2.metric("Carboidratos", f"{total_carbs} g")
            
            cm3, cm4 = st.columns([1, 1])
            cm3.metric("Proteínas", f"{total_prot} g")
            cm4.metric("Gorduras", f"{total_gord} g")
            
        with cs2:
            card_html = f'<div class="titulo-card">{ICONES["saude"]} REFEIÇÕES DO DIA (ANÁLISE POR IA)</div>'
            st.markdown(card_html, unsafe_allow_html=True)
            
            refeicao = st.text_input("O que você consumiu?", placeholder="Ex: Sopa de abóbora, ou 2 ovos e pão integral")
            porcao = st.text_input("Quantidade estimada (opcional):", placeholder="Ex: 1 prato cheio, 200g, etc.")
            
            if st.button("Mapear Prato e Nutrientes com o Jarvis"):
                if refeicao:
                    with st.spinner("O Jarvis está analisando os componentes do seu prato..."):
                        p_limpa = porcao if porcao else "1 porção"
                        macros = analisar_nutrientes_refeicao(f"{refeicao} - quantidade: {p_limpa}")
                        
                        id_refeicao_unico = f"food_{int(time.time())}_{len(db.get('refeicoes', []))}"
                        
                        db["refeicoes"].append({
                            "id": id_refeicao_unico,
                            "data": str(datetime.date.today()), 
                            "item": refeicao,
                            "porcao": p_limpa,
                            "calorias": macros.get("calorias", 0),
                            "carboidratos": macros.get("carboidratos", 0),
                            "proteinas": macros.get("proteinas", 0),
                            "gorduras": macros.get("gorduras", 0)
                        })
                        salvar_dados(db)
                        st.toast("Análise MacroNutricional Concluída com Sucesso!")
                        st.rerun()
            
            st.markdown("<div style='margin-top: 20px; font-size: 13px; color: #777777; font-weight: 600; text-transform: uppercase;'>Banco de Dados de Refeições Registradas</div>", unsafe_allow_html=True)
            
            if not refeicoes_hoje:
                st.markdown("<p style='color: #777777; font-style: italic; margin-top: 10px;'>Nenhum componente alimentar catalogado.</p>", unsafe_allow_html=True)
            else:
                for idx, ref in enumerate(refeicoes_hoje):
                    nome_ref = ref.get("item", "Alimento")
                    detalhe_ref = ref.get("porcao", "1 porção")
                    cal_ref = ref.get("calorias", "0")
                    carbs_ref = ref.get("carboidratos", "0")
                    prot_ref = ref.get("proteinas", "0")
                    gord_ref = ref.get("gorduras", "0")
                    id_ref = ref.get("id", f"antigo_{idx}")
                    
                    container_box = st.container()
                    with container_box:
                        c_info, c_cal, c_del = st.columns([2.5, 1.5, 1])
                        with c_info:
                            st.markdown(f"<p style='font-size: 1.05rem; font-weight: 700; color: #ffffff; margin: 0;'>{nome_ref.capitalize()}</p><p style='font-size: 0.85rem; color: #ffd700; margin: 0;'>{detalhe_ref}</p>", unsafe_allow_html=True)
                        with c_cal:
                            st.markdown(f"<p style='font-size: 1.1rem; font-weight: 800; color: #ffffff; margin: 0; text-align:right;'>{cal_ref} <span style='font-size:0.75rem; color:#a0aec0;'>kcal</span></p><p style='font-size: 0.75rem; color: #a0aec0; margin: 0; text-align:right;'>C: {carbs_ref}g | P: {prot_ref}g | G: {gord_ref}g</p>", unsafe_allow_html=True)
                        with c_del:
                            if st.button("Remover", key=f"del_food_{id_ref}"):
                                item_para_remover = next((x for x in db["refeicoes"] if x.get("id") == id_ref), None)
                                if item_para_remover:
                                    db["refeicoes"].remove(item_para_remover)
                                    salvar_dados(db)
                                    st.rerun()
                    st.markdown("<hr style='margin: 4px 0; border-color: rgba(212,175,55,0.05);'>", unsafe_allow_html=True)

    # 4. AGENDA (ALINHAMENTO PROPORCIONAL E CORRETO)
    with aba_calendario:
        card_html = f'<div class="titulo-card">{ICONES["calendario"]} SEU CRONOGRAMA DE ATIVIDADES DE VERDADE</div>'
        st.markdown(card_html, unsafe_allow_html=True)

        col_esq_info, col_dir_cal = st.columns([1, 1.3])
        
        dia_num_hoje = hoje.strftime("%d")
        dias_traduzidos = {
            "Monday": "SEGUNDA-FEIRA", "Tuesday": "TERÇA-FEIRA", "Wednesday": "QUARTA-FEIRA",
            "Thursday": "QUINTA-FEIRA", "Friday": "SEXTA-FEIRA", "Saturday": "SÁBADO", "Sunday": "DOMINGO"
        }
        dia_name_hoje = dias_traduzidos.get(hoje.strftime("%A"), "HOJE")
        
        with col_esq_info:
            st.markdown(
                f"<div style='background-color: #0b0b0b; padding: 25px; border-radius: 16px; border-left: 4px solid #d4af37; margin-bottom: 25px; border: 1px solid rgba(212,175,55,0.1);'>"
                f"<span style='color: #777777; font-size: 13px; font-weight:600; text-transform:uppercase;'>Data Actual</span>"
                f"<h1 style='font-size: 75px; font-family: \"Kanit\", sans-serif; font-weight: 700; line-height:1; margin: 5px 0; color: #ffffff;'>{dia_num_hoje}</h1>"
                f"<div style='font-size: 15px; font-family: \"Kanit\", sans-serif; color: #d4af37; font-weight:500; text-transform: uppercase; letter-spacing: 1px;'>{dia_name_hoje}</div>"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            with st.expander("➕ ENVIAR NOVO COMPROMISSO MANUAL PARA O GOOGLE", expanded=True):
                nome_ev = st.text_input("Título do compromisso:")
                data_ev = st.date_input("Data do evento:", hoje)
                h_ini = st.time_input("Início da atividade:", datetime.time(9, 0))
                
                if st.button("Agendar na Nuvem"):
                    if nome_ev:
                        with st.spinner("A enviar evento para o Google..."):
                            sucesso = enviar_evento_para_google(nome_ev, data_ev.isoformat(), h_ini.strftime('%H:%M'))
                            if sucesso:
                                puxar_eventos_do_google()
                                st.toast("Evento salvo no Google Agenda!")
                                st.rerun()
                            else:
                                st.error("Falha ao salvar. Verifique se o arquivo credentials.json está correto.")

        # --- AQUI ESTÁ O SEGREDO: ENVOLVEMOS A COLUNA DIREITA NUM CONTAINER HTML PARA SUBIR TUDO JUNTO ---
        with col_dir_cal:
            st.markdown('<div class="subir-bloco-agenda">', unsafe_allow_html=True)
                    
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
                @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;500;600;700&display=swap');
                body { background-color: transparent; margin: 0; padding: 0; font-family: 'Kanit', sans-serif; color: #ffffff; }
                
                .jarvis-calendar-grid { 
                    display: grid; 
                    grid-template-columns: repeat(7, 1fr); 
                    gap: 6px; 
                    background-color: #0a0a0a; 
                    padding: 12px; 
                    border-radius: 20px; 
                    border: 1px solid rgba(212, 175, 55, 0.15); 
                    width: 100%; 
                    box-sizing: border-box;
                    margin-top: 5px; /* Margem limpa e zerada aqui */
                }
                
                .calendar-header-day { text-align: center; font-weight: 600; font-size: 13px; color: #777777; text-transform: uppercase; padding-bottom: 6px; }
                .calendar-cell { background-color: rgba(16, 16, 16, 0.7); border: 1px solid rgba(255, 255, 255, 0.02); border-radius: 12px; min-height: 85px; padding: 8px; display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start; position: relative; overflow: hidden; }
                .calendar-cell.cell-today { background-color: rgba(212, 175, 55, 0.06); border: 1px solid #d4af37; }
                .calendar-cell.cell-empty { background-color: transparent; border: none; }
                .cell-number { font-weight: 700; font-size: 15px; color: #666666; margin-bottom: 6px; align-self: flex-end; }
                .cell-today .cell-number { color: #d4af37; font-size: 16px; }
                .events-wrapper { width: 100%; display: flex; flex-direction: column; gap: 4px; overflow-y: auto; max-height: 55px; }
                .event-tag { background-color: rgba(212, 175, 55, 0.15); color: #f3e5ab; font-size: 10px; font-weight: 500; padding: 4px 6px; border-radius: 6px; border-left: 2px solid #d4af37; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 92%; box-sizing: border-box; }
            </style>
            """
            
            html_corpo = f"<div style='text-align: center; margin-bottom: 12px; font-size: 18px; color: #ffffff; font-weight: 600; letter-spacing: 2px; margin-top: 10px;'>{nome_do_mes} {ano_atual}</div>"
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
            st.components.v1.html(html_estilos_calendario + html_corpo, height=560, scrolling=False)
            
            st.markdown('</div>', unsafe_allow_html=True) # Fecha a div que empurra tudo pra cima
            
        st.markdown("<br>", unsafe_allow_html=True)
        card_html = f'<div class="titulo-card">{ICONES["calendario"]} EVENTOS PRÓXIMOS SINCRONIZADOS DA NUVEM</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        
        eventos_cadastrados = db.get("eventos_locais", [])
        if not eventos_cadastrados:
            st.info("Pressione 'Atualizar Dados' acima para carregar as informações do servidor.")
        else:
            eventos_ordenados = sorted(eventos_cadastrados, key=lambda x: (x.get("date", ""), x.get("time", "")))
            for idx, ev in enumerate(eventos_ordenados):
                try:
                    data_convertida = datetime.date.fromisoformat(ev["date"]).strftime("%d/%m/%Y")
                except:
                    data_convertida = ev["date"]
                st.markdown(f"🗓️ **{ev['title']}** —  `{data_convertida}` às  `{ev['time']}`")
