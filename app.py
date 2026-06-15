<<<<<<< HEAD
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

# ==================== CONFIGURAÇÃO VISUAL MODERNA ====================
st.set_page_config(page_title="Jarvis OS", page_icon="🔱", layout="wide", initial_sidebar_state="collapsed")

# Dicionário de Ícones SVG Atualizado
ICONES = {
    "jarvis": """<svg width="45" height="45" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
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
    "conversa": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z" fill="url(#gold-grad)"/>/svg>""",
    "foco": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z" fill="url(#gold-grad)"/>/svg>""",
    "saude": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.5 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35zM10.5 7.5H9v2H7.5v1.5H9v2h1.5v-2H12v-1.5h-1.5v-2zm6 1.5h-3v1.5h3V9z" fill="url(#gold-grad)"/>/svg>""",
    "calendario": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d4af37"/><stop offset="100%" stop-color="#aa7c11"/></linearGradient></defs><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z" fill="url(#gold-grad)"/>/svg>""",
    # Novo ícone de caderno/bloco de notas com lápis em degradê dourado para a seção de metas
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

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
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
    
    .stTextInput input, .stDateInput input, .stTextArea textarea, div[data-baseweb="select"], div[role="button"] {
        background-color: #0b0b0b !important; 
        border: 1px solid rgba(212, 175, 55, 0.15) !important; 
        border-radius: 12px !important; 
        color: #ffffff !important;
        padding: 10px 16px !important;
        width: 100% !important;
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

# --- TELA DE LOGIN ---
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

    # --- MOTOR DE EXECUÇÃO DUPLO ---
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
                        db["eventos_locais"].append({
                            "id": f"ia_{int(time.time())}_{len(db['eventos_locais'])}",
                            "title": ev["title"],
                            "date": ev.get("date", data_hoje_str),
                            "time": ev.get("time", "12:00")
                        })
                salvar_dados(db)
                
        except Exception as e:
            print(f"[Erro de Extração]: {str(e)}")
            
        return resposta_texto_jarvis

# ==================== NAVEGAÇÃO POR ABAS ====================
    aba_metas, aba_pomodoro, aba_saude, aba_calendario = st.tabs([
        "CONVERSA & METAS", "TIMER DE FOCO", "SAÚDE & FITNESS", "AGENDA"
    ])

    # 1. CONVERSA & METAS
    with aba_metas:
        col_ia, col_lista = st.columns([1, 1])
        with col_ia:
            card_html = f'<div class="titulo-card">{ICONES["conversa"]} CONVERSAR COM O JARVIS</div>'
            st.markdown(card_html, unsafe_allow_html=True)
            chat_container = st.container(height=340)
            with chat_container:
                for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
            if prompt := st.chat_input("Envie uma instrução..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                resposta = processar_comando_e_criar_metas(prompt)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                st.rerun()
        with col_lista:
            # SINALIZAÇÃO ATUALIZADA: Trocado aqui para o ícone de bloco de notas/caderno solicitado
            card_html = f'<div class="titulo-card">{ICONES["metas_caderno"]} OBJETIVOS ATIVOS</div>'
            st.markdown(card_html, unsafe_allow_html=True)
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
        if not metas_validas: st.warning("Nenhum objetivo ativo encontrado. Defina uma tarefa conversando com o Jarvis primeiro.")
        else:
            cp1, cp2 = st.columns([1, 1])
            with cp1:
                meta_alvo = st.selectbox("Selecione a tarefa ativa para focar:", [m["nome"] for m in metas_validas])
                minutos_slider = st.slider("Duração:", 1, 120, int(st.session_state.pomo_tempo_inicial_escolhido), disabled=st.session_state.pomo_rodando)
                if not st.session_state.pomo_rodando and st.session_state.pomo_tempo_inicial_escolhido != minutos_slider:
                    st.session_state.pomo_tempo_inicial_escolhido = minutos_slider
                    st.session_state.pomo_segundos_restantes = minutos_slider * 60
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
        cs1, cs2 = st.columns([1, 1])
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
        with cs2:
            card_html = f'<div class="titulo-card">{ICONES["saude"]} REFEIÇÕES DO DIA</div>'
            st.markdown(card_html, unsafe_allow_html=True)
            refeicao = st.text_input("O que consumiu agora?", placeholder="Ex: Lanche")
            if st.button("Registrar MacroAlimento"):
                if refeicao:
                    db["refeicoes"].append({"data": str(datetime.date.today()), "item": refeicao})
                    salvar_dados(db); st.toast("Nutrientes Catalogados!")

    # 4. AGENDA
    with aba_calendario:
        card_html = f'<div class="titulo-card">{ICONES["calendario"]} SEU CRONOGRAMA DE ATIVIDADES</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        col_esq_info, col_dir_cal = st.columns([1, 1])
        
        hoje = datetime.date.today()
        dia_num_hoje = hoje.strftime("%d")
        dias_traduzidos = {
            "Monday": "SEGUNDA-FEIRA", "Tuesday": "TERÇA-FEIRA", "Wednesday": "QUARTA-FEIRA",
            "Thursday": "QUINTA-FEIRA", "Friday": "SEXTA-FEIRA", "Saturday": "SÁBADO", "Sunday": "DOMINGO"
        }
        dia_name_hoje = dias_traduzidos.get(hoje.strftime("%A"), "HOJE")
        
        with col_esq_info:
            st.markdown(
                f"<div style='background-color: #0b0b0b; padding: 25px; border-radius: 16px; border-left: 4px solid #d4af37; margin-bottom: 25px; border: 1px solid rgba(212,175,55,0.1);'>"
                f"<span style='color: #777777; font-size: 13px; font-weight:600; text-transform:uppercase;'>Data Atual</span>"
                f"<h1 style='font-size: 75px; font-family: \"Kanit\", sans-serif; font-weight: 700; line-height:1; margin: 5px 0; color: #ffffff;'>{dia_num_hoje}</h1>"
                f"<div style='font-size: 15px; font-family: \"Kanit\", sans-serif; color: #d4af37; font-weight:500; text-transform: uppercase; letter-spacing: 1px;'>{dia_name_hoje}</div>"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            with st.expander("➕ GERENCIAR EVENTOS MANUALMENTE", expanded=True):
                nome_ev = st.text_input("Título do compromisso:")
                data_ev = st.date_input("Data do evento:", hoje)
                h_ini = st.time_input("Início da atividade:", datetime.time(9, 0))
                
                if st.button("Agendar Evento"):
                    if nome_ev:
                        id_unico = f"manual_{int(time.time())}"
                        db["eventos_locais"].append({
                            "id": id_unico, "title": nome_ev, "date": data_ev.isoformat(), "time": h_ini.strftime('%H:%M')
                        })
                        salvar_dados(db); st.rerun()

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
                @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;500;600;700&display=swap');
                body { background-color: transparent; margin: 0; padding: 0; font-family: 'Kanit', sans-serif; color: #ffffff; }
                .jarvis-calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; background-color: #0a0a0a; padding: 12px; border-radius: 20px; border: 1px solid rgba(212, 175, 55, 0.15); width: 100%; box-sizing: border-box; }
                .calendar-header-day { text-align: center; font-weight: 600; font-size: 12px; color: #777777; text-transform: uppercase; padding-bottom: 3px; }
                .calendar-cell { background-color: rgba(16, 16, 16, 0.7); border: 1px solid rgba(255, 255, 255, 0.02); border-radius: 12px; min-height: 65px; padding: 6px; display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start; position: relative; overflow: hidden; }
                .calendar-cell.cell-today { background-color: rgba(212, 175, 55, 0.06); border: 1px solid #d4af37; }
                .calendar-cell.cell-empty { background-color: transparent; border: none; }
                .cell-number { font-weight: 700; font-size: 14px; color: #666666; margin-bottom: 4px; align-self: flex-end; }
                .cell-today .cell-number { color: #d4af37; font-size: 15px; }
                .events-wrapper { width: 100%; display: flex; flex-direction: column; gap: 3px; overflow-y: auto; max-height: 42px; }
                .event-tag { background-color: rgba(212, 175, 55, 0.15); color: #f3e5ab; font-size: 10px; font-weight: 500; padding: 4px 6px; border-radius: 6px; border-left: 2px solid #d4af37; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 90%; box-sizing: border-box; }
            </style>
            """
            
            html_corpo = f"<div style='text-align: center; margin-bottom: 12px; font-size: 16px; color: #ffffff; font-weight: 600; letter-spacing: 2px;'>{nome_do_mes} {ano_atual}</div>"
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
            st.components.v1.html(html_estilos_calendario + html_corpo, height=480, scrolling=False)

        st.markdown("<br>", unsafe_allow_html=True)
        card_html = f'<div class="titulo-card">{ICONES["calendario"]} LISTA COMPLETA DE COMPROMISSOS ATIVOS</div>'
        st.markdown(card_html, unsafe_allow_html=True)
        
        eventos_cadastrados = db.get("eventos_locais", [])
        if not eventos_cadastrados:
            st.info("Nenhum compromisso agendado até o momento.")
        else:
            eventos_ordenados = sorted(eventos_cadastrados, key=lambda x: (x.get("date", ""), x.get("time", "")))
            
            for idx, ev in enumerate(eventos_ordenados):
                try:
                    data_convertida = datetime.date.fromisoformat(ev["date"]).strftime("%d/%m/%Y")
                except:
                    data_convertida = ev["date"]
                
                col_info_ev, col_acao_ev = st.columns([5, 1])
                with col_info_ev:
                    st.markdown(f"**{ev['title']}** —  `{data_convertida}` às  `{ev['time']}`")
                with col_acao_ev:
                    if st.button("Remover", key=f"del_{ev.get('id', idx)}"):
                        db["eventos_locais"] = [item for item in db["eventos_locais"] if item.get("id") != ev.get("id")]
                        salvar_dados(db)
                        st.rerun()
=======
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
    if "GOOGLE_CREDENTIALS" in st.secrets:
        import google.auth.transport.requests
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        
        try:
            # Remove quebras de linha acidentais ou espaços extras das bordas
            raw_credentials = st.secrets["GOOGLE_CREDENTIALS"].strip()
            cred_data = json.loads(raw_credentials)
            
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception:
                        return None
                else:
                    try:
                        flow = InstalledAppFlow.from_client_config(cred_data, SCOPES)
                        creds = flow.run_local_server(port=0, open_browser=False)
                    except Exception:
                        return None
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            return build('calendar', 'v3', credentials=creds)
        except Exception as e:
            return None
    return None
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
            "contentHeight": 680, # Altura fixa para as células
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
>>>>>>> c5a0e94 (Ajuste na leitura do Google Agenda)

