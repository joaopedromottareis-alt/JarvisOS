import streamlit as st
import datetime
import time
import json
import os
import hashlib
import re
import calendar as pycalendar
from groq import Groq

# ==================== CONFIGURAÇÃO DA IA (BLINDADA) ====================
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
MODELO_EXTRATOR = "llama3-8b-8192"

# ==================== CONFIGURAÇÃO VISUAL MODERNA ====================
st.set_page_config(page_title="Jarvis OS", page_icon="🔱", layout="wide", initial_sidebar_state="collapsed")

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
        padding: 3rem 5rem !important; 
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
    }
    
    .stTabs [data-baseweb="tab"] { 
        color: #777777 !important; 
        font-family: 'Kanit', sans-serif !important;
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
                    st.rerun()
                else: st.error("CHAVE INCORRETA.")
            else: st.error("OPERADOR NÃO ENCONTRADO.")
        st.stop()
            
    elif modo_tela == "REGISTRAR NOVA CONTA":
        st.markdown("### 👋 CRIAR NOVA CONTA")
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
    col_titulo_sistema, col_botao_logout = st.columns([4, 1])
    with col_titulo_sistema:
        st.markdown("""<h1 class='custom-title' style='margin-bottom: 0px !important;'>🔱 <span class='jarvis-brand'>JARVIS OS</span></h1>""", unsafe_allow_html=True)
    with col_botao_logout:
        if st.button("SAIR DA SESSÃO"):
            st.session_state.autenticado = False
            st.session_state.username = None
            st.rerun()

    st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border-color: rgba(212,175,55,0.15);'>", unsafe_allow_html=True)

    # --- MOTOR DE EXECUÇÃO DUPLO DO JARVIS ---
    def processar_comando_e_criar_metas(comando):
        data_hoje_str = datetime.date.today().isoformat()
        
        if not API_KEY or client is None:
            return "⚠️ **Sistemas offline:** Nenhuma chave configurada. Por favor, adicione a variável `GROQ_API_KEY` nas configurações ocultas (Secrets) do seu servidor."

        prompt_sistema_chat = (
            f"Você é o Jarvis, o assistente virtual executivo de Tony Stark (agora servindo ao usuário {name}). Hoje é {data_hoje_str}.\n"
            "Responda ao usuário com extrema imponência, elegância e eficiência britânica. "
            "Se o usuário pediu para marcar uma atividade, compromisso, tarefa de escola ou geografia, confirme elegantemente na resposta."
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
                return "⚠️ **Falha Crítica:** A chave configurada nos Secrets foi considerada INVÁLIDA ou BLOQUEADA pelo Groq. Por favor, gere uma nova chave no painel do Groq e atualize seus Secrets."
            return f"⚠️ **Instabilidade nos Servidores:** {str(e)}"

        try:
            prompt_sistema_extrator = (
                f"Você é uma API de extração de dados. Hoje é exatamente {data_hoje_str}.\n"
                "Analise o comando inserido pelo usuário e retorne ESTRITAMENTE um objeto JSON.\n"
                "Importante: se o usuário disser 'as 17 hrs de hj' ou qualquer variação de horário de hoje, mude 'criar_evento' para true, coloque a data de hoje no formato YYYY-MM-DD e o horário correspondente.\n"
                "Modelo estrutural padrão de saída esperado:\n"
                "{\n"
                "  \"criar_meta\": false,\n"
                "  \"novas_metas\": [],\n"
                "  \"criar_evento\": false,\n"
                "  \"novos_eventos\": [\n"
                "     {{\"title\": \"Nome da Atividade\", \"date\": \"YYYY-MM-DD\", \"time\": \"HH:MM\"}}\n"
                "  ]\n"
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
            print(f"[Erro de Extração Oculto]: {str(e)}")
            
        return resposta_texto_jarvis

    # ==================== NAVEGAÇÃO POR ABAS ====================
    aba_metas, aba_pomodoro, aba_saude, aba_calendario, aba_graficos = st.tabs([
        "💬 CONVERSA & METAS", "⏱️ TIMER DE FOCO", "🥗 SAÚDE & FITNESS", "📅 AGENDA", "📊 ESTATÍSTICAS"
    ])

    # 1. CONVERSA & METAS
    with aba_metas:
        col_ia, col_lista = st.columns([1, 1])
        with col_ia:
            st.markdown('<div class="titulo-card">🔱 CONVERSAR COM O JARVIS</div>', unsafe_allow_html=True)
            chat_container = st.container(height=340)
            with chat_container:
                for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
            if prompt := st.chat_input("Envie uma instrução..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                resposta = processar_comando_e_criar_metas(prompt)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                st.rerun()
        with col_lista:
            st.markdown('<div class="titulo-card">🎯 OBJETIVOS ATIVOS</div>', unsafe_allow_html=True)
            metas_ativas = [m for m in db["metas"] if not m["concluida"]]
            if not metas_ativas: st.info("Sem diretrizes ativas.")
            else:
                for m in db["metas"]:
                    if not m["concluida"]:
                        c1, c2, c3 = st.columns([3, 1, 1])
                        c1.markdown(f"✨ **{m['nome']}**<br><span style='color:#777777;'>{m['categoria']}</span>", unsafe_allow_html=True)
                        c2.markdown(f"<div style='padding-top:10px; color:#d4af37;'>{m['tempo_dedicado']} min</div>", unsafe_allow_html=True)
                        if c3.button("✓", key=m["id"]):
                            m["concluida"] = True; salvar_dados(db); st.rerun()

    # 2. POMODORO
    with aba_pomodoro:
        st.markdown('<div class="titulo-card">⏱️ TIMER DE FOCO</div>', unsafe_allow_html=True)
        metas_validas = [m for m in db["metas"] if not m["concluida"]]
        if not metas_validas: st.warning("Adicione uma meta primeiro.")
        else:
            cp1, cp2 = st.columns(2)
            with cp1:
                meta_alvo = st.selectbox("Meta alvo:", [m["nome"] for m in metas_validas])
                minutos_slider = st.slider("Duração:", 1, 120, int(st.session_state.pomo_tempo_inicial_escolhido), disabled=st.session_state.pomo_rodando)
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
                st.markdown(f"<div style='text-align: center;'><h1 style='font-size: 75px; color:#ffffff;'>{m_vis:02d}:{s_vis:02d}</h1><span style='color:#d4af37;'>🎯 {meta_alvo}</span></div>", unsafe_allow_html=True)
            
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
        cs1, cs2 = st.columns(2)
        with cs1:
            st.markdown('<div class="titulo-card">💧 DIRETRIZES DE HIDRATAÇÃO</div>', unsafe_allow_html=True)
            peso_texto = st.text_input("Seu peso atual (kg):", value=str(db.get("peso_usuario", 70.0)))
            try: peso_limpo = float(peso_texto.replace(',', '.'))
            except: peso_limpo = 70.0
            db["peso_usuario"] = peso_limpo
            alvo_calc = int(peso_limpo * 35)
            st.metric("Consumido", f"{db['agua']} ml", f"Alvo do Jarvis: {alvo_calc} ml")
            cb1, cb2 = st.columns(2)
            if cb1.button("➕ Copo (250ml)"): db["agua"] += 250; salvar_dados(db); st.rerun()
            if cb2.button("🔄 Limpar Registro"): db["agua"] = 0; salvar_dados(db); st.rerun()
        with cs2:
            st.markdown('<div class="titulo-card">🍳 REFEIÇÕES DO DIA</div>', unsafe_allow_html=True)
            refeicao = st.text_input("O que consumiu agora?", placeholder="Ex: Lanche")
            if st.button("Registrar MacroAlimento"):
                if refeicao:
                    db["refeicoes"].append({"data": str(datetime.date.today()), "item": refeicao})
                    salvar_dados(db); st.toast("Nutrientes Catalogados!")

    # 4. AGENDA (CALENDÁRIO OTIMIZADO COM INDICAÇÃO VISUAL)
    with aba_calendario:
        st.markdown('<div class="titulo-card">📅 SEU CRONOGRAMA DE ATIVIDADES</div>', unsafe_allow_html=True)
        col_esq_info, col_dir_cal = st.columns([1.2, 2.3])
        
        hoje = datetime.date.today()
        dia_num_hoje = hoje.strftime("%d")
        dias_traduzidos = {
            "Monday": "SEGUNDA-FEIRA", "Tuesday": "TERÇA-FEIRA", "Wednesday": "QUARTA-FEIRA",
            "Thursday": "QUINTA-FEIRA", "Friday": "SEXTA-FEIRA", "Saturday": "SÁBADO", "Sunday": "DOMINGO"
        }
        dia_name_hoje = dias_traduzidos.get(hoje.strftime("%A"), "HOJE")
        
        with col_esq_info:
            st.markdown(
                f"<div style='background-color: #0b0b0b; padding: 25px; border-radius: 16px; border-left: 4px solid #d4af37; margin-bottom: 15px; border: 1px solid rgba(212,175,55,0.1);'>"
                f"<span style='color: #777777; font-size: 13px; font-weight:600; text-transform:uppercase;'>Data Atual</span>"
                f"<h1 style='font-size: 75px; font-family: \"Kanit\", sans-serif; font-weight: 700; line-height:1; margin: 5px 0; color: #ffffff;'>{dia_num_hoje}</h1>"
                f"<div style='font-size: 15px; font-family: \"Kanit\", sans-serif; color: #d4af37; font-weight:500; text-transform: uppercase; letter-spacing: 1px;'>{dia_name_hoje}</div>"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            with st.expander("➕ GERENCIAR EVENTOS MANUALMENTE", expanded=False):
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
            
            # Agrupar eventos por dia
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
                @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;600;700&display=swap');
                body { background-color: transparent; margin: 0; padding: 0; font-family: 'Kanit', sans-serif; color: #ffffff; }
                .jarvis-calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; background-color: #0a0a0a; padding: 15px; border-radius: 20px; border: 1px solid rgba(212, 175, 55, 0.15); }
                .calendar-header-day { text-align: center; font-weight: 600; font-size: 13px; color: #777777; text-transform: uppercase; padding-bottom: 5px; }
                .calendar-cell { background-color: rgba(16, 16, 16, 0.7); border: 1px solid rgba(255, 255, 255, 0.02); border-radius: 12px; min-height: 55px; padding: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }
                .calendar-cell.cell-today { background-color: rgba(212, 175, 55, 0.08); border: 1px solid #d4af37; }
                .calendar-cell.cell-empty { background-color: transparent; border: none; }
                .cell-number { font-weight: 700; font-size: 16px; color: #888888; }
                .cell-today .cell-number { color: #d4af37; font-size: 18px; }
                .event-indicator { width: 6px; height: 6px; background-color: #d4af37; border-radius: 50%; position: absolute; bottom: 8px; box-shadow: 0 0 6px #d4af37; }
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
                        
                        indicador_evento = ""
                        if data_corrente_str in dict_eventos:
                            indicador_evento = "<div class='event-indicator'></div>"
                                
                        html_corpo += f"<div class='calendar-cell {classe_hoje}'>"
                        html_corpo += f"<div class='cell-number'>{dia_num}</div>"
                        html_corpo += indicador_evento
                        html_corpo += "</div>"
                        
            html_corpo += "</div>"
            st.components.v1.html(html_estilos_calendario + html_corpo, height=440, scrolling=False)

        # --- NOVA SEÇÃO: DETALHES DA AGENDA LOGO ABAIXO ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="titulo-card">📋 LISTA COMPLETA DE COMPROMISSOS ATIVOS</div>', unsafe_allow_html=True)
        
        eventos_cadastrados = db.get("eventos_locais", [])
        if not eventos_cadastrados:
            st.info("Nenhum compromisso agendado até o momento.")
        else:
            # Ordenar eventos por data e hora
            eventos_ordenados = sorted(eventos_cadastrados, key=lambda x: (x.get("date", ""), x.get("time", "")))
            
            for idx, ev in enumerate(eventos_ordenados):
                try:
                    data_convertida = datetime.date.fromisoformat(ev["date"]).strftime("%d/%m/%Y")
                except:
                    data_convertida = ev["date"]
                
                col_info_ev, col_acao_ev = st.columns([5, 1])
                with col_info_ev:
                    st.markdown(
                        f"🔹 **{ev['title']}** — 📅 `{data_convertida}` às ⏰ `{ev['time']}`"
                    )
                with col_acao_ev:
                    if st.button("Remover", key=f"del_{ev.get('id', idx)}"):
                        db["eventos_locais"] = [item for item in db["eventos_locais"] if item.get("id") != ev.get("id")]
                        salvar_dados(db)
                        st.rerun()

    # 5. ESTATÍSTICAS
    with aba_graficos:
        st.markdown('<div class="titulo-card">📊 DESEMPENHO OPERACIONAL</div>', unsafe_allow_html=True)
        if db.get("metas"):
            concluidas = sum(1 for m in db["metas"] if m["concluida"])
            total = len(db["metas"])
            st.progress(concluidas / total if total > 0 else 0)
            st.metric("Completadas", f"{concluidas}/{total}", f"{db.get('historico_pomodoro', 0)} minutos em foco.")
