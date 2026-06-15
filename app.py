import streamlit as st
from groq import Groq
import json

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Jarvis OS", page_icon="🤖", layout="wide")

ICONES = {
    "conversa": "💬",
    "calendario": "📅",
    "metas": "🎯",
    "timer": "⏱️",
    "saude": "❤️"
}

# Inicializa o cliente da Groq (Troque pela sua chave ou use Streamlit Secrets)
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "SUA_CHAVE_AQUI"))

# 2. INICIALIZAÇÃO DO SESSION STATE (MEMÓRIA DO SISTEMA)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "metas" not in st.session_state:
    st.session_state.metas = []

if "eventos_calendario" not in st.session_state:
    st.session_state.eventos_calendario = []

if "logado" not in st.session_state:
    st.session_state.logado = False

if "username" not in st.session_state:
    st.session_state.username = ""


# 3. MOTOR DE IA (PROCESSADOR COM IDENTIFICAÇÃO DE GÊNERO)
def processar_comando_e_criar_metas(texto_usuario):
    username_atual = st.session_state.get("username", "Operador")
    
    # Prompt inteligente que descobre o gênero pelo nome inserido no login
    contexto_prompt = f"""
    Você é o Jarvis, o assistente virtual ultra-eficiente e genial do sistema operacional Jarvis OS.
    O operador atual autenticado no sistema chama-se: {username_atual}.
    
    DIRETRIZES DE PERSONALIDADE E GÊNERO:
    1. Analise o nome "{username_atual}" e identifique o gênero para responder adequadamente. 
       - Se for feminino (ex: Maria, Mãe, Ana), use SEMPRE o tratamento "Senhora", "atendê-la", "comprometida", etc.
       - Se for masculino (ex: João, Pedro), use "Senhor", "atendê-lo", "comprometido", etc.
       - Se não tiver certeza, adote uma postura formal e respeitosa usando o nome diretamente de forma neutra.
    2. Responda de forma extremamente educada, prestativa e tecnológica, mantendo o tom clássico do Jarvis.

    Ação solicitada pelo operador: "{texto_usuario}"
    
    Sua resposta deve ser estritamente um objeto JSON válido, sem formatação markdown (sem ```json), com a seguinte estrutura:
    {{
        "resposta_jarvis": "Texto da sua resposta falada/escrita para o operador",
        "novas_metas": [
            {{"titulo": "Nome da Meta", "status": "Em andamento"}}
        ],
        "novas_tarefas_calendario": [
            {{"evento": "Nome do Compromisso", "data": "AAAA-MM-DD", "hora": "HH:MM"}}
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": contexto_prompt}],
            model="llama3-8b-8192",
            temperature=0.3
        )
        
        conteudo = response.choices[0].message.content.strip()
        resultado = json.loads(conteudo)
        
        # Salva as novas metas no estado da sessão
        for meta in resultado.get("novas_metas", []):
            st.session_state.metas.append(meta)
            
        # Salva os novos eventos na agenda
        for ev in resultado.get("novas_tarefas_calendario", []):
            st.session_state.eventos_calendario.append(ev)
            
        return resultado.get("resposta_jarvis", "Comando processado com sucesso.")
        
    except Exception as e:
        return f"Sistemas instáveis, não consegui processar a solicitação interna: {str(e)}"


# 4. TELA DE LOGIN / CADASTRO
if not st.session_state.logado:
    st.markdown(f'<h1>{ICONES["conversa"]} ENTRAR NO JARVIS OS</h1>', unsafe_allow_html=True)
    
    operacao = st.radio("SELECIONE A OPERAÇÃO:", ["LOGIN", "REGISTRAR NOVA CONTA"], horizontal=True)
    
    st.subheader("LOGIN DO OPERADOR")
    username_input = st.text_input("USERNAME:")
    senha_input = st.text_input("SENHA DE SEGURANÇA:", type="password")
    
    if st.button("ACESSAR PAINEL PRINCIPAL"):
        if username_input.strip() != "":
            st.session_state.logado = True
            st.session_state.username = username_input.strip()
            # Mensagem inicial personalizada de boas-vindas baseada no gênero
            st.session_state.messages = [{"role": "assistant", "content": processar_comando_e_criar_metas("Diga oi e pergunte como pode ajudar")}]
            st.rerun()
        else:
            st.error("Por favor, digite um username válido para identificação de diretrizes.")

# 5. PAINEL PRINCIPAL (PÓS-LOGIN)
else:
    # Barra Superior com botão de Sair
    col_titulo, col_sair = st.columns([9, 1])
    with col_titulo:
        st.markdown(f"<h1>🤖 JARVIS OS — <small style='color:#d4af37;'>Operador: {st.session_state.username}</small></h1>", unsafe_allow_html=True)
    with col_sair:
        if st.button("SAIR DA SESSÃO"):
            st.session_state.logado = False
            st.session_state.username = ""
            st.session_state.messages = []
            st.rerun()
            
    st.markdown("---")

    # Criação das Abas do Sistema
    aba_metas, aba_timer, aba_saude, aba_agenda = st.tabs([
        "🎯 CONVERSA & METAS", 
        "⏱️ TIMER DE FOCO", 
        "❤️ SAÚDE & FITNESS", 
        "📅 AGENDA"
    ])

    # --- ABA 1: CONVERSA & METAS ---
    with aba_metas:
        col_ia, col_lista = st.columns([1, 1])
        
        with col_ia:
            st.markdown(f'<h3>{ICONES["conversa"]} INTERFACE DE COMANDO</h3>', unsafe_allow_html=True)
            
            # Caixa do Chat histórico
            chat_container = st.container(height=380)
            with chat_container:
                for msg in st.session_state.messages:
                    st.chat_message(msg["role"]).write(msg["content"])
            
            # Campo de texto para enviar instruções
            if prompt := st.chat_input("Envie uma instrução de texto para o Jarvis..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                resposta = processar_comando_e_criar_metas(prompt)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                st.rerun()

        with col_lista:
            st.markdown(f'<h3>{ICONES["metas"]} OBJETIVOS ATIVOS</h3>', unsafe_allow_html=True)
            if not st.session_state.metas:
                st.info("Nenhuma meta ativa nos registros no momento.")
            else:
                for idx, m in enumerate(st.session_state.metas):
                    st.checkbox(f"**{m.get('titulo')}** — Status: {m.get('status', 'Em andamento')}", key=f"meta_{idx}")

    # --- ABA 2: TIMER DE FOCO ---
    with aba_timer:
        st.markdown(f'<h3>{ICONES["timer"]} TIMER DE FOCO POMODORO</h3>', unsafe_allow_html=True)
        st.write("Módulo de produtividade ativo. Use para focar nas suas metas.")

    # --- ABA 3: SAÚDE & FITNESS ---
    with aba_saude:
        st.markdown(f'<h3>{ICONES["saude"]} MONITORAMENTO DE SAÚDE</h3>', unsafe_allow_html=True)
        peso = st.number_input("Seu peso atual (kg):", value=70)
        st.write(f"Alvo de hidratação calculado pelo Jarvis: {int(peso * 35)} ml por dia.")

    # --- ABA 4: AGENDA ---
    with aba_agenda:
        st.markdown(f'<h3>{ICONES["calendario"]} COMPROMISSOS AGENDADOS</h3>', unsafe_allow_html=True)
        if not st.session_state.eventos_calendario:
            st.info("Nenhum evento na agenda para os próximos dias.")
        else:
            for ev in st.session_state.eventos_calendario:
                st.markdown(f"📆 **{ev.get('data')}** às **{ev.get('hora')}** — *{ev.get('evento')}*")
