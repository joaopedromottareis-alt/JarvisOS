import streamlit as st
import streamlit.components.v1 as components

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Jarvis OS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Toda a interface unificada (HTML + CSS Premium + JavaScript Avançado)
jarvis_interface = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jarvis OS</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #080705;
            --bg-card: #110e0a;
            --bg-card-hover: #1a150e;
            --gold-primary: #d4af37;
            --gold-secondary: #aa8416;
            --gold-gradient: linear-gradient(135deg, #ffd700 0%, #b8860b 100%);
            --text-main: #ffffff;
            --text-muted: #8e8271;
            --border-radius: 20px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Montserrat', sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            padding: 20px;
        }

        /* --- LOGO & HEADER COMPLETO --- */
        .jarvis-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px 20px 20px;
            border-bottom: 1px solid #231c12;
            margin-bottom: 30px;
        }

        .brand-wrapper {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            background: var(--gold-gradient);
            width: 14px;
            height: 14px;
            clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
        }

        .brand-title {
            font-size: 22px;
            font-weight: 700;
            letter-spacing: 2px;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-status {
            font-size: 11px;
            color: #ff4a4a;
            font-weight: 600;
            letter-spacing: 1px;
            background: rgba(255, 74, 74, 0.1);
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid rgba(255, 74, 74, 0.2);
        }

        /* --- NAVEGAÇÃO DE ABAS INTERATIVAS --- */
        .nav-container {
            background: #14110a;
            border: 1px solid #261f12;
            padding: 6px;
            border-radius: 30px;
            display: inline-flex;
            gap: 5px;
            margin-bottom: 30px;
        }

        .nav-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 10px 24px;
            border-radius: 25px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: var(--transition);
        }

        .nav-btn:hover {
            color: var(--text-main);
        }

        .nav-btn.active {
            background: var(--gold-gradient);
            color: #000000;
            font-weight: 700;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
        }

        /* --- CONTEÚDO E SEÇÕES --- */
        .content-section {
            display: none;
            animation: fadeIn 0.5s ease forwards;
        }

        .content-section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- INTERFACE MOBILE (FIEL À IMAGEM 1) --- */
        .phone-showcase {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .phone-frame {
            width: 350px;
            height: 720px;
            background: radial-gradient(circle at top, #1c160e 0%, #070604 100%);
            border-radius: 45px;
            border: 10px solid #231c12;
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            position: relative;
            box-shadow: 0 30px 60px rgba(0,0,0,0.8), inset 0 0 20px rgba(214,175,55,0.05);
        }

        .phone-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
            margin-bottom: 30px;
        }

        .phone-greeting {
            font-size: 15px;
            color: var(--text-muted);
            font-weight: 400;
        }

        .phone-username {
            font-size: 26px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 25px;
            letter-spacing: -0.5px;
        }

        /* Card de Progresso Semanal */
        .phone-card {
            background: linear-gradient(145deg, #1d170f 0%, #110e0a 100%);
            border: 1px solid #362a18;
            border-radius: 24px;
            padding: 22px;
            margin-bottom: 20px;
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }

        .phone-card-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--gold-primary);
            margin-bottom: 10px;
        }

        .phone-card-desc {
            font-size: 12px;
            color: #c9beaf;
            line-height: 1.5;
            margin-bottom: 14px;
        }

        .phone-file-tag {
            font-size: 11px;
            color: var(--text-muted);
            background: rgba(255,255,255,0.03);
            padding: 6px 12px;
            border-radius: 8px;
            display: inline-block;
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 15px;
        }

        .phone-progress-container {
            width: 100%;
            height: 6px;
            background: #231b10;
            border-radius: 10px;
            margin-bottom: 8px;
            overflow: hidden;
        }

        .phone-progress-fill {
            width: 65%;
            height: 100%;
            background: var(--gold-gradient);
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(212,175,55,0.5);
        }

        .phone-progress-labels {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--gold-primary);
            font-weight: 600;
        }

        /* Recomendações Inteligentes */
        .ai-section-title {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            display: block;
        }

        .ai-recommendation-box {
            background: rgba(20, 17, 10, 0.6);
            border: 1px solid #231b10;
            padding: 14px;
            border-radius: 16px;
            font-size: 12px;
            line-height: 1.5;
            color: #d1c7bd;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }

        .ai-check {
            color: var(--gold-primary);
            font-weight: bold;
        }

        /* Barra de Entrada de Comando Inferior */
        .phone-input-container {
            margin-top: auto;
            position: relative;
        }

        .phone-input-field {
            width: 100%;
            background: #17130c;
            border: 1px solid #3d301b;
            border-radius: 16px;
            padding: 16px 50px 16px 18px;
            color: var(--text-main);
            font-size: 13px;
            outline: none;
            transition: var(--transition);
        }

        .phone-input-field:focus {
            border-color: var(--gold-primary);
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.15);
        }

        .phone-input-submit {
            position: absolute;
            right: 16px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: var(--gold-primary);
            font-size: 18px;
            cursor: pointer;
        }

        /* --- TELA DA NOVA META (ORBE CENTRAL) --- */
        .orbe-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
            margin-bottom: 40px;
        }

        .orbe-glow {
            width: 160px;
            height: 160px;
            background: radial-gradient(circle, rgba(212,175,55,0.2) 0%, rgba(212,175,55,0.05) 50%, transparent 70%);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .orbe-core {
            width: 70px;
            height: 70px;
            background: #080705;
            border-radius: 50%;
            border: 2px solid var(--gold-primary);
            box-shadow: 0 0 30px rgba(212, 175, 55, 0.4), inset 0 0 15px rgba(212, 175, 55, 0.2);
            animation: pulseOrbe 3s infinite alternate ease-in-out;
        }

        @keyframes pulseOrbe {
            0% { transform: scale(0.95); box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
            100% { transform: scale(1.05); box-shadow: 0 0 40px rgba(212, 175, 55, 0.6); }
        }

        .orbe-title {
            font-size: 18px;
            font-weight: 600;
            text-align: center;
            margin-top: -10px;
        }

        .meta-field {
            background: #14110a;
            border: 1px solid #2d2314;
            padding: 16px;
            border-radius: 16px;
            font-size: 13px;
            margin-bottom: 12px;
        }

        .meta-label {
            color: var(--text-muted);
            font-weight: 500;
            margin-right: 5px;
        }

        /* --- CALENDÁRIO COMPACTO --- */
        .calendar-wrapper {
            max-width: 850px;
            margin: 0 auto;
            background: #110e0a;
            border: 1px solid #231c12;
            padding: 30px;
            border-radius: 24px;
        }

        .calendar-weekdays {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            text-align: center;
            font-weight: 600;
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .calendar-days-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 14px;
        }

        .calendar-cell {
            background: #0b0906;
            border: 1px solid #1f1910;
            border-radius: 14px;
            aspect-ratio: 1.4;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 12px;
            position: relative;
            transition: var(--transition);
        }

        .calendar-cell:hover {
            background: #17130c;
            border-color: #443721;
        }

        .cell-number {
            font-size: 14px;
            font-weight: 700;
            color: #706556;
        }

        /* Dia Atual Destacado com Dourado */
        .calendar-cell.active-day {
            border: 2px solid var(--gold-primary);
            background: #1c160e;
        }

        .calendar-cell.active-day .cell-number {
            color: var(--gold-primary);
        }

        /* Estilização do Evento no Dia 19 */
        .event-banner {
            background: #2b2111;
            border-left: 3px solid var(--gold-primary);
            padding: 5px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            color: #f1e5d2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-top: 6px;
        }

        .event-controls {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            background: #ffffff;
            border-radius: 4px;
            padding: 2px;
            margin-top: 4px;
        }

        .event-arrow {
            color: #888;
            font-size: 10px;
            font-weight: bold;
            text-decoration: none;
        }

        .event-indicator-pill {
            width: 35px;
            height: 6px;
            background: #cccccc;
            border-radius: 3px;
        }

        /* --- SESSÕES COMPLEMENTARES --- */
        .pomodoro-box {
            max-width: 450px;
            margin: 40px auto;
            text-align: center;
            background: var(--bg-card);
            border: 1px solid #231c12;
            padding: 40px;
            border-radius: var(--border-radius);
        }

        .timer-numeric {
            font-size: 72px;
            font-weight: 300;
            letter-spacing: -2px;
            margin: 20px 0;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .control-btn {
            background: var(--gold-gradient);
            color: #000;
            border: none;
            padding: 14px 32px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: var(--transition);
        }

        .control-btn:hover {
            box-shadow: 0 0 20px rgba(212,175,55,0.4);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <header class="jarvis-header">
        <div class="brand-wrapper">
            <div class="brand-icon"></div>
            <h1 class="brand-title">JARVIS OS</h1>
        </div>
        <div class="brand-status">SISTEMA ATIVO</div>
    </header>

    <center>
        <div class="nav-container">
            <button class="nav-btn active" onclick="navigate('conversa')">Gerenciamento</button>
            <button class="nav-btn" onclick="navigate('agenda')">Calendário</button>
            <button class="nav-btn" onclick="navigate('timer')">Foco</button>
        </div>
    </center>

    <section id="conversa" class="content-section active">
        <div class="phone-showcase">
            
            <div class="phone-frame">
                <div class="phone-top-bar">
                    <span>9:41</span>
                    <span>JARVIS v4.5</span>
                </div>
                <div class="phone-greeting">Olá,</div>
                <div class="phone-username">Alex Smith</div>
                
                <div class="phone-card">
                    <div class="phone-card-title">Relatório Semanal & Atualizações</div>
                    <div class="phone-card-desc">Eu sugiro revisar os arquivos pendentes de hoje.</div>
                    <div class="phone-file-tag">Arquivos: Relatorio_Jan.zip +5</div>
                    
                    <div class="phone-progress-container">
                        <div class="phone-progress-fill"></div>
                    </div>
                    <div class="phone-progress-labels">
                        <span>Progresso</span>
                        <span>65%</span>
                    </div>
                </div>

                <div style="margin-top: 10px; margin-bottom: 30px;">
                    <span class="ai-section-title">Recomendações da IA</span>
                    <div class="ai-recommendation-box">
                        <span class="ai-check">✓</span>
                        <span>Verificar mensagens importantes à noite.</span>
                    </div>
                </div>

                <div class="phone-input-container">
                    <input type="text" class="phone-input-field" placeholder="O que deseja gerenciar hoje?">
                    <button class="phone-input-submit">✦</button>
                </div>
            </div>

            <div class="phone-frame">
                <div class="phone-top-bar">
                    <span>9:41</span>
                    <span>Nova Meta</span>
                </div>
                
                <div class="orbe-container">
                    <div class="orbe-glow">
                        <div class="orbe-core"></div>
                    </div>
                    <h3 class="orbe-title">O que quer<br>planejar hoje?</h3>
                </div>

                <div style="display: flex; flex-direction: column; margin-top: 20px;">
                    <div class="meta-field">
                        <span class="meta-label">Tarefa:</span> Enviar relatório ao cliente
                    </div>
                    <div class="meta-field">
                        <span class="meta-label">Horário Aconselhável:</span> 20:30, Hoje
                    </div>
                </div>
            </div>

        </div>
    </section>

    <section id="agenda" class="content-section">
        <div class="calendar-wrapper">
            <h2 style="text-align: center; margin-bottom: 30px; font-weight: 500; letter-spacing: 1px;">CRONOGRAMA MENSAL</h2>
            <div class="calendar-weekdays">
                <div>Dom</div><div>Seg</div><div>Ter</div><div>Qua</div><div>Qui</div><div>Sex</div><div>Sáb</div>
            </div>
            <div class="calendar-days-grid" id="calendarGrid"></div>
        </div>
    </section>

    <section id="timer" class="content-section">
        <div class="pomodoro-box">
            <h3 style="font-weight: 600; letter-spacing: 0.5px;">PRODUTIVIDADE MÁXIMA</h3>
            <div class="timer-numeric" id="timerValue">25:00</div>
            <button class="control-btn" id="timerAction" onclick="actionTimer()">Iniciar Sessão</button>
        </div>
    </section>

    <script>
        // Sistema de abas nativo
        function navigate(sectionId) {
            document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(sectionId).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        // Construção cirúrgica do calendário
        function generateCalendar() {
            const grid = document.getElementById('calendarGrid');
            grid.innerHTML = '';
            
            // Espaçamento inicial para alinhar os dias da semana corretamente
            const offset = 1; 
            for(let i=0; i<offset; i++) {
                grid.appendChild(document.createElement('div'));
            }

            // Gerando os blocos numéricos do calendário
            for(let day=1; day<=28; day++) {
                const cell = document.createElement('div');
                cell.classList.add('calendar-cell');
                
                const num = document.createElement('div');
                num.classList.add('cell-number');
                num.textContent = day;
                cell.appendChild(num);

                // Destaque do dia 15
                if(day === 15) {
                    cell.classList.add('active-day');
                }

                // Inserção da Prova de Geografia no Dia 19
                if(day === 19) {
                    const banner = document.createElement('div');
                    banner.classList.add('event-banner');
                    banner.textContent = 'Prova de Geo...';
                    cell.appendChild(banner);

                    const controls = document.createElement('div');
                    controls.classList.add('event-controls');
                    controls.innerHTML = `
                        <a class="event-arrow" href="#">&lt;</a>
                        <div class="event-indicator-pill"></div>
                        <a class="event-arrow" href="#">&gt;</a>
                    `;
                    cell.appendChild(controls);
                }

                grid.appendChild(cell);
            }
        }

        // Cronômetro funcional do Jarvis
        let timerSeconds = 25 * 60;
        let timerActive = false;
        let countdown;

        function actionTimer() {
            const btn = document.getElementById('timerAction');
            if(timerActive) {
                clearInterval(countdown);
                btn.textContent = "Iniciar Sessão";
                timerActive = false;
            } else {
                timerActive = true;
                btn.textContent = "Pausar";
                countdown = setInterval(() => {
                    if(timerSeconds > 0) {
                        timerSeconds--;
                        let min = Math.floor(timerSeconds / 60).toString().padStart(2, '0');
                        let sec = (timerSeconds % 60).toString().padStart(2, '0');
                        document.getElementById('timerValue').textContent = min + ":" + sec;
                    } else {
                        clearInterval(countdown);
                        alert("Sessão finalizada!");
                        timerSeconds = 25 * 60;
                        document.getElementById('timerValue').textContent = "25:00";
                        btn.textContent = "Iniciar Sessão";
                        timerActive = false;
                    }
                }, 1000);
            }
        }

        window.onload = generateCalendar;
    </script>
</body>
</html>
"""

# Método seguro do Streamlit para renderizar toda a aplicação sem erros de compilação
components.html(jarvis_interface, height=850, scrolling=True)
