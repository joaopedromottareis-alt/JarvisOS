import streamlit as st
import datetime
import time
import json
import os
from groq import Groq
import plotly.graph_objects as go

# --- Importações para o Calendário ---
from streamlit_calendar import calendar
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ==================== CONFIGURAÇÃO DA IA (GROQ) ====================
API_KEY = "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"
client = Groq(api_key=API_KEY)
MODELO_IA = "llama-3.3-70b-versatile" 

SCOPES = ['https://www.googleapis.com/auth/calendar']

# ==================== CONFIGURAÇÃO VISUAL INSPIRADA NAS REFERÊNCIAS ====================
st.set_page_config(page_title="Jarvis OS - Dashboard", page_icon="🤖", layout="wide")

# CSS Avançado anti-sobreposição e injeção de estilo em Cards Isolados
st.markdown("""
import streamlit as st
import streamlit_authenticator as stauth

# 1. CADASTRO DE USUÁRIOS E SENHAS CRIPTOGRAFADAS
# (Para testar, o usuário é "admin" e a senha é "admin123")
credentials = {
    "usernames": {
        "admin": {
            "name": "Senhor",
            "password": "$2b$12$Mco6XwCH79S452R2gB5PFeIes3G8z9q/XkW9b5iV1zYlWv8iL1PDe" # "admin123" criptografado
        }
    }
}

# 2. CONFIGURAÇÃO DO AUTENTICADOR
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="jarvis_login_cookie",
    key="jarvis_chave_secreta_assinatura",
    cookie_expiry_days=30
)

# 3. RENDERIZAR O FORMULÁRIO DE LOGIN NA TELA
name, authentication_status, username = authenticator.login(location='main')

# 4. TRATAMENTO DOS STATUS DE LOGIN
if authentication_status == False:
    st.error("❌ Usuário ou senha incorretos. Acesso negado.")
    st.stop() # Bloqueia o resto do script

elif authentication_status == None:
    st.warning("🔒 Por favor, insira suas credenciais para acessar o Jarvis OS.")
    st.stop() # Bloqueia o resto do script até digitar

# ---------------------------------------------------------
# SE CHEGAR AQUI, O LOGIN FOI UM SUCESSO!
# ---------------------------------------------------------
# Adiciona um botão de Logout discreto na barra lateral
authenticator.logout('Sair do Sistema', 'sidebar')

st.success(f"Bem-vindo de volta, {name}!")

# REVISE AQUI: Todo o restante do seu código original (Abas, Chat, Calendário)
# continua aqui para baixo, exatamente como estava funcionando antes!
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Configuração Base Clean-Dark Space */
    .stApp { 
        background-color: #0a0a0d; 
        color: #e4e4e9; 
        font-family: 'Inter', system-ui, sans-serif; 
    }
    
    /* Margens seguras para evitar quebras em telas Desktop */
    .block-container { 
        padding: 2.5rem 3.5rem !important; 
        max-width: 100% !important; 
    }
    #MainMenu, footer, header { visibility: hidden !important; }
    
    /* Títulos do Sistema */
    h1, h2, h3, h4 { 
        color: #d4af37 !important; 
        font-weight: 700; 
        letter-spacing: -0.5px;
        margin-bottom: 18px !important;
    }
    .titulo-card { 
        color: #d4af37 !important; 
        font-size: 16px; 
        font-weight: 600; 
        text-transform: uppercase;
        letter-spacing: 0.75px;
        margin-bottom: 8px;
    }

    /* Customização de containers nativos para simular os cards arredondados das fotos */
    div[data-testid="stVerticalBlock"] > div {
        gap: 1.5rem !important;
    }
    
    /* Inputs e Dropdowns com visual integrado e espaçados */
    div[data-baseweb="select"], div[data-baseweb="input"], .stTextInput>div>div>input, .stDateInput>div>div>input {
        background-color: #121218 !important; 
        border: 1px solid #22222a !important; 
        border-radius: 12px !important; 
        color: #ffffff !important;
        margin-bottom: 5px;
    }
    
    /* Botões Limpos com efeito Hover Glow das referências */
    .stButton>button { 
        background-color: #121218; 
        color: #d4af37; 
        border: 1px solid #d4af37; 
        border-radius: 12px; 
        padding: 10px 18px; 
        font-weight: 600; 
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover { 
        background-color: #d4af37; 
        color: #0a0a0d; 
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.15);
        transform: translateY(-1px);
    }
    
    /* Abas Superiores Estilo Aplicação Premium */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #121218; 
        border: 1px solid #1e1e26;
        border-radius: 14px;
        padding: 8px;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab"] { 
        color: #8e8e9a; 
        padding: 12px 24px; 
        font-size: 14px; 
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] { 
        color: #d4af37 !important; 
        background-color: #1c1c26 !important;
    }
    
    /* FORÇA O IFRAME DO CALENDÁRIO A RESPONDER À ALTURA FIXA SEM COLAPSAR */
    iframe[title="streamlit_calendar.calendar"] {
        border: 1px solid #1e1e26 !important;
        border-radius: 16px !important;
        background-color: #121218 !important;
        min-height: 800px !important;
        height: 800px !important;
        display: block !important;
    }
    
    /* Expander transparente estilizado para opções secundárias */
    .stExpander {
        background-color: #121218 !important;
        border: 1px solid #1e1e26 !important;
        border-radius: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== BANCO DE DADOS LOCAL (JSON) ====================
ARQUIVO_DADOS = "dados_jarvis.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"metas": [], "agua": 0, "peso_usuario": 70.0, "historico_pomodoro": 0, "refeicoes": [], "eventos_locais": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

if "db" not in st.session_state:
    st.session_state.db = carregar_dados()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemas online, Senhor. Defina suas diretrizes e eu cuidarei de estruturar os alvos operacionais."}]

if "cal_version" not in st.session_state:
    st.session_state.cal_version = 0

if "pomo_segundos_restantes" not in st.session_state: st.session_state.pomo_segundos_restantes = 1500
if "pomo_rodando" not in st.session_state: st.session_state.pomo_rodando = False
if "pomo_tempo_inicial_escolhido" not in st.session_state: st.session_state.pomo_tempo_inicial_escolhido = 25

db = st.session_state.db
if "eventos_locais" not in db: db["eventos_locais"] = []

# ==================== FUNÇÃO DE AUTENTICAÇÃO DO GOOGLE ====================
def obter_servico_google_agenda():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                return None
        else:
            if not os.path.exists('credentials.json'):
                return None
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception:
                return None
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        return build('calendar', 'v3', credentials=creds)
    except Exception:
        return None

service = obter_servico_google_agenda()

# ==================== CÉREBRO INTEGRADO DO JARVIS (SOLUÇÃO MULTI-DIAS) ====================
def processar_comando_e_criar_metas(comando):
    data_hoje_str = datetime.date.today().isoformat()
    
    prompt_sistema = f"""
    Você é o Jarvis, o assistente pessoal de alta tecnologia do usuário.
    Seu objetivo é analisar a mensagem do usuário e decidir se deve criar uma meta no painel e/ou eventos no Google Agenda.
    Considere que a data de HOJE é {data_hoje_str}.
    
    Se o usuário pedir para agendar algo que dure vários dias (ex: "do dia 3 ao 7"), você deve identificar a "data_inicio" e a "data_fim". 
    Se for apenas um dia, coloque a mesma data em ambos os campos.
    
    REGRA CRÍTICA PARA O TÍTULO DO EVENTO:
    Você DEVE obrigatoriamente incluir a hora de início no início do título do evento (ex: "15:00 - Ocupado"). Se não houver hora combinada, use "00:00 - Título".
    
    Você DEVE responder ESTRITAMENTE no formato JSON abaixo, sem textos fora do JSON:
    {{
        "resposta_chat": "Sua resposta elegante e motivadora falando com o usuário, tratando-o como 'Senhor'.",
        "criar_meta": true ou false,
        "novas_metas": [
            {{"nome": "Nome curto da meta", "categoria": "Estudos", "Saúde", "Alimentação" ou "Trabalho"}}
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
            st.toast("🎯 Novas diretrizes acopladas ao painel, Senhor!")
            
        if resultado.get("criar_agenda") and resultado.get("evento_agenda"):
            ev = resultado["evento_agenda"]
            try:
                d_ini = datetime.datetime.strptime(ev["data_inicio"], "%Y-%m-%d").date()
                d_fim = datetime.datetime.strptime(ev["data_fim"], "%Y-%m-%d").date()
                inicio_parsed = datetime.datetime.strptime(ev["hora_inicio"], "%H:%M").time()
                fim_parsed = datetime.datetime.strptime(ev["hora_fim"], "%H:%M").time()
                
                # Loop inteligente para preencher cada dia do intervalo sem pular datas
                dia_atual = d_ini
                timestamp_base = int(time.time())
                contador_id = 0
                
                while dia_atual <= d_fim:
                    start_dt = datetime.datetime.combine(dia_atual, inicio_parsed)
                    end_dt = datetime.datetime.combine(dia_atual, fim_parsed)
                    id_unico = f"jarvis_{timestamp_base}_{contador_id}"
                    
                    novo_ev = {
                        "id": id_unico,
                        "title": ev["titulo"],
                        "start": start_dt.isoformat(),
                        "end": end_dt.isoformat(),
                        "backgroundColor": "#1c1c26",
                        "borderColor": "#d4af37",
                        "textColor": "#ffffff"
                    }
                    db["eventos_locais"].append(novo_ev)
                    
                    if service:
                        try:
                            event_body = {
                                'id': id_unico.replace("_", ""), # O ID do Google Agenda não permite underscores
                                'summary': ev["titulo"],
                                'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
                                'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
                            }
                            service.events().insert(calendarId='primary', body=event_body).execute()
                        except Exception:
                            pass
                    
                    dia_atual += datetime.timedelta(days=1)
                    contador_id += 1
                
                salvar_dados(db)
                st.toast("📅 Cronograma multi-dias mapeado e fixado com sucesso!")
                st.session_state.cal_version += 1
            except Exception:
                pass
                
        return resultado.get("resposta_chat", "Comando processado, Senhor.")
    except Exception as e:
        return "Módulos de IA em espera. Sistemas locais em modo de contingência operante."

# ==================== INTERFACE WORKSTATION DESKTOP ====================
st.markdown("<h1 style='margin-bottom: 25px !important;'>🔱 JARVIS OPERATIONAL SYSTEM</h1>", unsafe_allow_html=True)

aba_metas, aba_pomodoro, aba_saude, aba_calendario, aba_graficos = st.tabs([
    "🎯 Painel de Diretrizes", 
    "⏱️ Módulo de Foco Temporal", 
    "💧 Parâmetros Biométricos",
    "📅 Cronograma Operacional", 
    "📊 Análise Estatística"
])

# 1. ABA DE METAS
with aba_metas:
    col_ia, col_lista = st.columns([1, 1])
    with col_ia:
        st.markdown('<div class="titulo-card">🤖 Interface de Linguagem Natural</div>', unsafe_allow_html=True)
        with st.container(border=True):
            chat_container = st.container(height=340)
            with chat_container:
                for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
            if prompt := st.chat_input("Digite o comando operacional..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                resposta = processar_comando_e_criar_metas(prompt)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                st.rerun()
    with col_lista:
        st.markdown('<div class="titulo-card">🎯 Objetivos em Execução</div>', unsafe_allow_html=True)
        with st.container(border=True):
            metas_ativas = [m for m in db["metas"] if not m["concluida"]]
            if not metas_ativas: st.info("Nenhuma diretriz ativa em andamento no momento, Senhor.")
            else:
                for m in db["metas"]:
                    if not m["concluida"]:
                        c1, c2, c3 = st.columns([3, 1, 1])
                        c1.markdown(f"⚡ **{m['nome']}**<br><span style='color:#8e8e9a; font-size:13px;'>{m['categoria']}</span>", unsafe_allow_html=True)
                        c2.markdown(f"<div style='padding-top:10px; color:#d4af37;'>⏱️ {m['tempo_dedicado']} min</div>", unsafe_allow_html=True)
                        if c3.button("Concluir", key=m["id"]):
                            m["concluida"] = True
                            salvar_dados(db)
                            st.rerun()
                        st.markdown("<hr style='margin: 12px 0; border-color: #1e1e26;'>", unsafe_allow_html=True)

# 2. ABA POMODORO
with aba_pomodoro:
    st.markdown('<div class="titulo-card">⏱️ Alocação de Ciclos de Foco</div>', unsafe_allow_html=True)
    metas_validas = [m for m in db["metas"] if not m["concluida"]]
    if not metas_validas: st.warning("Nenhum alvo ativo encontrado. Solicite a criação de metas ao Jarvis primeiro.")
    else:
        cp1, cp2 = st.columns(2)
        with cp1:
            with st.container(border=True):
                st.markdown("### Configurações de Ciclo")
                meta_alvo = st.selectbox("Vincular foco atual à meta:", [m["nome"] for m in metas_validas])
                minutos_slider = st.slider("Configurar duração do bloco (minutos):", min_value=1, max_value=120, value=int(st.session_state.pomo_tempo_inicial_escolhido), disabled=st.session_state.pomo_rodando)
                if not st.session_state.pomo_rodando and st.session_state.pomo_tempo_inicial_escolhido != minutos_slider:
                    st.session_state.pomo_tempo_inicial_escolhido = minutos_slider
                    st.session_state.pomo_segundos_restantes = minutos_slider * 60
                st.markdown("<br>", unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                if not st.session_state.pomo_rodando:
                    if b1.button("▶️ Iniciar / Retomar"): st.session_state.pomo_rodando = True; st.rerun()
                else:
                    if b1.button("⏸️ Pausar"): st.session_state.pomo_rodando = False; st.rerun()
                if b2.button("Automático" if st.session_state.pomo_rodando else "⏹️ Resetar"):
                    st.session_state.pomo_rodando = False
                    st.session_state.pomo_segundos_restantes = st.session_state.pomo_tempo_inicial_escolhido * 60
                    st.rerun()
        with cp2:
            with st.container(border=True):
                m_vis, s_vis = divmod(st.session_state.pomo_segundos_restantes, 60)
                st.markdown(f"<div style='text-align: center; padding: 15px 0;'><span style='color:#8e8e9a; font-size:13px; text-transform: uppercase; letter-spacing:1px;'>Cronômetro Ativo</span><h1 style='font-size: 78px; font-family: monospace; margin: 10px 0; color: #ffffff !important;'>{m_vis:02d}:{s_vis:02d}</h1><span style='color:#d4af37; font-size:15px; font-weight:500;'>🎯 {meta_alvo}</span></div>", unsafe_allow_html=True)
        
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
        st.markdown('<div class="titulo-card">💧 Monitoramento de Hidratação</div>', unsafe_allow_html=True)
        with st.container(border=True):
            peso_texto = st.text_input("Informe seu peso atual (kg):", value=str(db.get("peso_usuario", 70.0)).replace('.', ','))
            try:
                peso_limpo = float(peso_texto.replace(',', '.'))
            except ValueError:
                peso_limpo = 70.0
            if peso_limpo != db.get("peso_usuario", 70.0) and peso_limpo > 0: 
                db["peso_usuario"] = peso_limpo
                salvar_dados(db)
                st.rerun()
            alvo_calculado = int(peso_limpo * 35)
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Consumo Atual", f"{db['agua']} ml", f"Alvo Recomendado: {alvo_calculado} ml")
            st.markdown("<br>", unsafe_allow_html=True)
            c_btn1, c_btn2 = st.columns(2)
            if c_btn1.button("🥛 Ingerir Copo (250ml)"): db["agua"] += 250; salvar_dados(db); st.rerun()
            if c_btn2.button("♻️ Resetar Consumo"): db["agua"] = 0; salvar_dados(db); st.rerun()
    with cs2:
        st.markdown('<div class="titulo-card">🍲 Log de Nutrição</div>', unsafe_allow_html=True)
        with st.container(border=True):
            refeicao = st.text_input("O que você consumiu na última janela?", placeholder="Ex: Patinho, arroz integral e brócolis")
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Catalogar Refeição no Sistema"):
                if refeicao: db["refeicoes"].append({"data": str(datetime.date.today()), "item": refeicao}); salvar_dados(db); st.toast("Refeição arquivada com sucesso!")

# 4. ABA CRONOGRAMA OPERACIONAL
with aba_calendario:
    st.markdown('<div class="titulo-card">📅 Alocação de Rotinas e Agenda Integrada</div>', unsafe_allow_html=True)
    
    if service:
        st.markdown("<span style='color: #2ecc71; font-size: 13px; font-weight:500;'>🟢 Sincronização em tempo real com Google Agenda ativa.</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color: #e67e22; font-size: 13px; font-weight:500;'>🟡 Modo Local Operante (Google temporariamente desconectado).</span>", unsafe_allow_html=True)
    
    # Preparação da lista de eventos
    eventos_para_exibir = [{
        "title": "06:00 - Sistema Inicializado",
        "start": datetime.datetime.combine(datetime.date.today(), datetime.time(6, 0)).isoformat(),
        "end": datetime.datetime.combine(datetime.date.today(), datetime.time(6, 30)).isoformat(),
        "backgroundColor": "#121218",
        "borderColor": "#1e1e26",
        "textColor": "#8e8e9a",
        "editable": False
    }]
    if db.get("eventos_locais"):
        eventos_para_exibir.extend(db["eventos_locais"])

    # Painel Modularizado Superior
    with st.expander("🛠️ Central Operacional de Agendamentos (Clique para expandir/recolher)", expanded=False):
        c_add, c_del = st.columns(2)
        
        with c_add:
            st.markdown("### ➕ Adicionar Novo Evento")
            nome_evento = st.text_input("Título da Atividade:", placeholder="Ex: Treino de Perna")
            data_evento = st.date_input("Data Selecionada:", datetime.date.today())
            h_ini = st.time_input("Horário de Início:", datetime.time(14, 0))
            h_fim = st.time_input("Horário de Término:", datetime.time(15, 0))
            recorrente = st.checkbox("🔄 Repetir diariamente (Rotina Fixa)")
            
            if st.button("Gravar Compromisso"):
                if nome_evento:
                    start_dt = datetime.datetime.combine(data_evento, h_ini)
                    end_dt = datetime.datetime.combine(data_evento, h_fim)
                    id_unico = "jarvis_" + str(int(time.time())) + "_manual"
                    
                    titulo_formatado = f"{h_ini.strftime('%H:%M')} - {nome_evento}"
                    
                    novo_ev = {
                        "id": id_unico,
                        "title": titulo_formatado,
                        "start": start_dt.isoformat(),
                        "end": end_dt.isoformat(),
                        "backgroundColor": "#1c1c26",
                        "borderColor": "#d4af37",
                        "textColor": "#ffffff"
                    }
                    
                    if service:
                        try:
                            event_body = {
                                'id': id_unico.replace("_", ""),
                                'summary': titulo_formatado,
                                'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
                                'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
                            }
                            if recorrente: event_body['recurrence'] = ['RRULE:FREQ=DAILY']
                            service.events().insert(calendarId='primary', body=event_body).execute()
                        except Exception:
                            pass
                    
                    db["eventos_locais"].append(novo_ev)
                    salvar_dados(db)
                    st.session_state.cal_version += 1
                    st.rerun()

        with c_del:
            st.markdown("### 🗑️ Desacoplar Compromissos")
            opcoes_remocao = {}
            for idx, ev in enumerate(eventos_para_exibir):
                if ev.get("editable") != False:
                    ev_id = ev.get("id", f"antigo_{idx}")
                    opcoes_remocao[ev_id] = ev.get("title", f"Compromisso ({idx})")
            
            if opcoes_remocao:
                evento_para_remover = st.selectbox("Selecione qual compromisso remover do banco:", options=list(opcoes_remocao.keys()), format_func=lambda x: opcoes_remocao[x])
                
                if st.button("Remover Registro Selecionado"):
                    if service and not evento_para_remover.startswith("antigo_"):
                        try:
                            service.events().delete(calendarId='primary', eventId=evento_para_remover.replace("_", "")).execute()
                        except Exception:
                            pass
                    
                    if evento_para_remover.startswith("antigo_"):
                        idx_alvo = int(evento_para_remover.split("_")[1]) - 1
                        if 0 <= idx_alvo < len(db["eventos_locais"]):
                            db["eventos_locais"].pop(idx_alvo)
                    else:
                        db["eventos_locais"] = [ev for ev in db["eventos_locais"] if ev.get("id") != evento_para_remover]
                    
                    salvar_dados(db)
                    st.session_state.cal_version += 1
                    st.rerun()
            else:
                st.info("Nenhum compromisso mutável registrado na grade local.")
            
            if st.button("⚠️ Limpar Todos os Eventos do Painel Local"):
                db["eventos_locais"] = []
                salvar_dados(db)
                st.session_state.cal_version += 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        options = {
            "initialView": "dayGridMonth",
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,timeGridDay"
            },
            "editable": True,
            "selectable": True,
            "timeZone": "local",
            "contentHeight": 680,
            "handleWindowResize": True
        }
        
        calendar(events=eventos_para_exibir, options=options, key=f"jarvis_grid_mensal_estabilizado_{st.session_state.cal_version}")

# 5. ABA DE GRÁFICOS
with aba_graficos:
    st.markdown('<div class="titulo-card">📊 Gráficos de Performance Analítica</div>', unsafe_allow_html=True)
    if not db["metas"]: st.info("Nenhuma métrica encontrada para consolidar dados visuais.")
    else:
        with st.container(border=True):
            tipo_visao = st.selectbox("Escopo Analítico:", ["🎯 Alvos Atuais Em Execução", "✅ Histórico de Objetivos Concluídos"])
            if "Atuais" in tipo_visao:
                metas_filtradas = [m for m in db["metas"] if not m["concluida"] and m["tempo_dedicado"] > 0]
                cor_barra = "#d4af37"; msg_vazio = "Nenhum dos alvos atuais acumulou minutos de foco hoje."
            else:
                metas_filtradas = [m for m in db["metas"] if m["concluida"]]
                cor_barra = "#8e721a"; msg_vazio = "Nenhuma diretriz foi concluída historicamente ainda."
            if not metas_filtradas: st.info(msg_vazio)
            else:
                nomes_metas = [m["nome"] for m in metas_filtradas]; tempos_metas = [m["tempo_dedicado"] for m in metas_filtradas]
                fig = go.Figure(data=[go.Bar(x=nomes_metas, y=tempos_metas, marker_color=cor_barra, text=tempos_metas, textposition='auto', hovertemplate="<b>Alvo:</b> %{x}<br><b>Foco:</b> %{y} min<extra></extra>")])
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(0,0,0,0)", 
                    font=dict(color="#cccccc", size=12), 
                    xaxis=dict(gridcolor="#1e1e26"), 
                    yaxis=dict(gridcolor="#1e1e26"), 
                    margin=dict(l=40, r=40, t=20, b=40), 
                    height=380
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
