<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jarvis OS</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* ==========================================================================
           1. VARIÁVEIS DE DESIGN & RESET
           ========================================================================== */
        :root {
            --bg-main: #0a0a0a;
            --bg-card: #121212;
            --bg-card-hover: #1a1a1a;
            --gold-primary: #d4af37;
            --gold-secondary: #aa8416;
            --gold-gradient: linear-gradient(135deg, #ffd700 0%, #b8860b 100%);
            --text-main: #ffffff;
            --text-muted: #888888;
            --border-radius: 16px;
            --transition: all 0.3s ease;
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
        }

        /* ==========================================================================
           2. CABEÇALHO & NAVEGAÇÃO (Tabs superiores no estilo Jarvis OS)
           ========================================================================== */
        header {
            background-color: rgba(10, 10, 10, 0.95);
            border-bottom: 1px solid #222;
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 15px 5%;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }

        .brand-logo {
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 1px;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-sub {
            font-size: 14px;
            color: var(--text-main);
            font-weight: 500;
        }

        nav .nav-tabs {
            display: flex;
            gap: 25px;
            list-style: none;
            overflow-x: auto;
            padding-bottom: 5px;
        }

        nav .nav-tabs::-webkit-scrollbar {
            height: 4px;
        }

        nav .nav-tabs::-webkit-scrollbar-thumb {
            background: #333;
            border-radius: 2px;
        }

        .tab-item {
            color: var(--text-muted);
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 8px 0;
            position: relative;
            transition: var(--transition);
            white-space: nowrap;
        }

        .tab-item:hover {
            color: var(--text-main);
        }

        .tab-item.active {
            color: var(--gold-primary);
        }

        .tab-item.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: #ff4a4a; /* Linha de realce vermelha sob o menu ativo conforme a imagem */
        }

        /* ==========================================================================
           3. CONTAINER PRINCIPAL & SEÇÕES
           ========================================================================== */
        main {
            flex: 1;
            padding: 30px 5%;
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
        }

        .app-section {
            display: none;
            animation: fadeIn 0.4s ease forwards;
        }

        .app-section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Grid Layout para Painéis Mistos */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
        }

        .card {
            background-color: var(--bg-card);
            border-radius: var(--border-radius);
            padding: 25px;
            border: 1px solid #1e1e1e;
            transition: var(--transition);
        }

        .card:hover {
            border-color: #2a2a2a;
            background-color: var(--bg-card-hover);
        }

        /* ==========================================================================
           4. COMPONENTE: CALENDÁRIO COMPACTO (Fiel à Imagem 1 e 5)
           ========================================================================== */
        .calendar-container {
            max-width: 900px;
            margin: 0 auto;
        }

        .calendar-header-days {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            text-align: center;
            font-weight: 600;
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 15px;
            text-transform: uppercase;
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 12px;
        }

        .calendar-day {
            background-color: #0f0f0f;
            border: 1px solid #1a1a1a;
            border-radius: 12px;
            aspect-ratio: 1.5;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 10px;
            position: relative;
            cursor: pointer;
            transition: var(--transition);
        }

        .calendar-day:hover {
            background-color: #161616;
            border-color: #333;
        }

        .calendar-day .day-number {
            font-size: 14px;
            font-weight: 700;
            color: #a0a0a0;
        }

        /* Destaque do Dia Atual (Dia 15 na imagem) */
        .calendar-day.current-day {
            border: 2px solid var(--gold-primary);
            background-color: #14130e;
        }

        .calendar-day.current-day .day-number {
            color: var(--gold-primary);
        }

        /* Evento Especial (Dia 19 na imagem) */
        .calendar-event {
            background-color: #221d11;
            border-left: 3px solid var(--gold-primary);
            padding: 4px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            color: #e0d0b0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-top: 5px;
        }

        .event-indicator-dot {
            width: 6px;
            height: 6px;
            background-color: var(--gold-primary);
            border-radius: 50%;
            margin: 4px auto 0 auto;
        }

        /* ==========================================================================
           5. COMPONENTE: INTERFACE DE GERENCIAMENTO (Estilo App Mobile Gold/Space)
           ========================================================================== */
        .mobile-preview-container {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .mock-phone {
            width: 340px;
            height: 680px;
            background: linear-gradient(180deg, #16120b 0%, #0c0a07 100%);
            border-radius: 40px;
            border: 8px solid #222;
            padding: 25px 18px;
            display: flex;
            flex-direction: column;
            position: relative;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);
            overflow: hidden;
        }

        .phone-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 25px;
        }

        .phone-user-greeting {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }

        .phone-user-name {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 20px;
        }

        .phone-card-highlight {
            background: linear-gradient(135deg, #2c2213 0%, #17120a 100%);
            border: 1px solid #42331c;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            position: relative;
        }

        .phone-card-title {
            font-size: 13px;
            font-weight: 600;
            color: #d4af37;
            margin-bottom: 8px;
        }

        .progress-bar-container {
            width: 100%;
            height: 6px;
            background-color: #2a2217;
            border-radius: 3px;
            margin: 12px 0;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            width: 65%;
            background: var(--gold-gradient);
            border-radius: 3px;
        }

        .phone-input-wrapper {
            margin-top: auto;
            position: relative;
        }

        .phone-input {
            width: 100%;
            background-color: #1a150e;
            border: 1px solid #3a2f1c;
            border-radius: 14px;
            padding: 14px 45px 14px 16px;
            color: var(--text-main);
            font-size: 12px;
            outline: none;
        }

        .phone-input-icon {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gold-primary);
            cursor: pointer;
        }

        /* ==========================================================================
           6. OUTROS MÓDULOS (Timer, Saúde e Estatísticas)
           ========================================================================== */
        /* Timer de Foco */
        .timer-display {
            font-size: 64px;
            font-weight: 700;
            text-align: center;
            margin: 30px 0;
            font-variant-numeric: tabular-nums;
            background: var(--gold-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .timer-controls {
            display: flex;
            justify-content: center;
            gap: 15px;
        }

        .btn {
            background: #1a1a1a;
            color: var(--text-main);
            border: 1px solid #333;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: var(--transition);
        }

        .btn:hover {
            background-color: #222;
            border-color: var(--gold-primary);
        }

        .btn-primary {
            background: var(--gold-gradient);
            color: #000;
            border: none;
        }

        .btn-primary:hover {
            background: #e5bf43;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        }

        /* Saúde & Métrica Cardíaca */
        .heart-rate-box {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-top: 15px;
        }

        .heart-icon-svg {
            width: 45px;
            height: 45px;
            fill: none;
            stroke: #ff4a4a;
            stroke-width: 2;
            animation: pulse 1s infinite alternate;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.08); }
        }

        .metric-value {
            font-size: 32px;
            font-weight: 700;
        }
    </style>
</head>
<body>

    <header>
        <div class="brand-container">
            <span class="brand-logo">A JARVIS OS</span>
            <span class="brand-sub">// SISTEMA OPERACIONAL ATIVO</span>
        </div>
        <nav>
            <ul class="nav-tabs">
                <li class="tab-item active" onclick="switchTab('conversa')">Conversa & Metas</li>
                <li class="tab-item" onclick="switchTab('timer')">Timer de Foco</li>
                <li class="tab-item" onclick="switchTab('saude')">Saúde & Fitness</li>
                <li class="tab-item" onclick="switchTab('agenda')">Agenda</li>
                <li class="tab-item" onclick="switchTab('estatisticas')">Estatísticas</li>
            </ul>
        </nav>
    </header>

    <main>

        <section id="conversa" class="app-section active">
            <h2 style="margin-bottom: 20px; font-weight: 600;">Painel de Controle Inteligente</h2>
            <div class="mobile-preview-container">
                
                <div class="mock-phone">
                    <div class="phone-header">
                        <span>9:41</span>
                        <span>JARVIS v4.2</span>
                    </div>
                    <div class="phone-user-greeting">Olá,</div>
                    <div class="phone-user-name">Alex Smith</div>
                    
                    <div class="phone-card-highlight">
                        <div class="phone-card-title">Relatório Semanal & Atualizações</div>
                        <p style="font-size: 11px; color: #bba27a; line-height: 1.4;">Eu sugiro revisar os arquivos pendentes de hoje.</p>
                        <div style="font-size: 10px; color: var(--text-muted); margin-top: 8px;">Arquivos: Relatorio_Jan.zip +5</div>
                        
                        <div class="progress-bar-container">
                            <div class="progress-bar-fill"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 10px; color: #d4af37;">
                            <span>Progresso</span>
                            <span>65%</span>
                        </div>
                    </div>

                    <div style="margin-top: 10px;">
                        <span style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Recomendações da IA</span>
                        <div style="background-color: #14110a; border: 1px solid #261f12; padding: 12px; border-radius: 12px; margin-top: 8px; font-size: 11px;">
                            ✔️ Verificar mensagens importantes à noite.
                        </div>
                    </div>

                    <div class="phone-input-wrapper">
                        <input type="text" class="phone-input" placeholder="O que deseja gerenciar hoje?">
                        <span class="phone-input-icon">✦</span>
                    </div>
                </div>

                <div class="mock-phone">
                    <div class="phone-header">
                        <span>9:41</span>
                        <span>Nova Meta</span>
                    </div>
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div style="width: 130px; height: 130px; background: radial-gradient(circle, #d4af37 0%, transparent 70%); margin: 0 auto; opacity: 0.6; filter: blur(5px);"></div>
                        <h3 style="font-size: 18px; margin-top: -80px; position: relative; z-index: 2;">O que quer planejar?</h3>
                    </div>
                    
                    <div style="margin-top: 60px; display: flex; flex-direction: column; gap: 12px;">
                        <div style="background: #1c170f; border: 1px solid #3a2f1c; padding: 15px; border-radius: 14px; font-size: 12px;">
                            <span style="color: var(--text-muted);">Tarefa:</span> Enviar relatório ao cliente
                        </div>
                        <div style="background: #1c170f; border: 1px solid #3a2f1c; padding: 15px; border-radius: 14px; font-size: 12px;">
                            <span style="color: var(--text-muted);">Horário Aconselhável:</span> 20:30, Hoje
                        </div>
                    </div>
                </div>

            </div>
        </section>

        <section id="timer" class="app-section">
            <div class="card" style="max-width: 500px; margin: 0 auto; text-align: center;">
                <h3>Timer de Foco Jarvis</h3>
                <p style="color: var(--text-muted); font-size: 14px; margin-top: 5px;">Mantenha a produtividade máxima</p>
                <div class="timer-display" id="timerDisplay">25:00</div>
                <div class="timer-controls">
                    <button class="btn btn-primary" id="startBtn" onclick="toggleTimer()">Iniciar</button>
                    <button class="btn" onclick="resetTimer()">Resetar</button>
                </div>
            </div>
        </section>

        <section id="saude" class="app-section">
            <div class="dashboard-grid">
                <div class="card">
                    <h3>Frequência Cardíaca</h3>
                    <div class="heart-rate-box">
                        <svg class="heart-icon-svg" viewBox="0 0 24 24">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                        </svg>
                        <div>
                            <span class="metric-value" id="bpmValue">72</span> <span style="color: var(--text-muted); font-size: 14px;">BPM</span>
                        </div>
                    </div>
                    <p style="color: var(--text-muted); font-size: 12px; margin-top: 15px;">// Monitoramento em tempo real ativo</p>
                </div>
            </div>
        </section>

        <section id="agenda" class="app-section">
            <div class="calendar-container">
                <h2 style="margin-bottom: 25px; font-weight: 600; text-align: center;">Calendário Mensal</h2>
                
                <div class="calendar-header-days">
                    <div>Dom</div>
                    <div>Seg</div>
                    <div>Ter</div>
                    <div>Qua</div>
                    <div>Qui</div>
                    <div>Sex</div>
                    <div>Sáb</div>
                </div>

                <div class="calendar-grid" id="calendarGrid">
                    </div>
            </div>
        </section>

        <section id="estatisticas" class="app-section">
            <div class="card">
                <h3>Análise de Desempenho</h3>
                <p style="color: var(--text-muted); margin-top: 10px;">Todos os sistemas operando dentro dos parâmetros ideais estabelecidos.</p>
                <div style="margin-top: 20px; height: 150px; background-color: #151515; border-radius: 8px; display: flex; align-items: flex-end; padding: 10px; gap: 10px;">
                    <div style="width: 100%; height: 40%; background: var(--gold-gradient); border-radius: 4px;"></div>
                    <div style="width: 100%; height: 65%; background: var(--gold-gradient); border-radius: 4px;"></div>
                    <div style="width: 100%; height: 85%; background: var(--gold-gradient); border-radius: 4px;"></div>
                    <div style="width: 100%; height: 60%; background: var(--gold-gradient); border-radius: 4px;"></div>
                </div>
            </div>
        </section>

    </main>

    <script>
        // --- GERENCIADOR DE ABAS ---
        function switchTab(tabId) {
            // Remove classe active de todas as abas e seções
            document.querySelectorAll('.tab-item').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.app-section').forEach(sec => sec.classList.remove('active'));
            
            // Adiciona classe active na aba clicada
            const targetTab = Array.from(document.querySelectorAll('.tab-item')).find(tab => tab.textContent.toLowerCase().includes(tabId.substring(0,4)));
            if(targetTab) targetTab.classList.add('active');
            
            // Mostra a seção correspondente
            document.getElementById(tabId).classList.add('active');
        }

        // --- GERADOR DO CALENDÁRIO MENSAL DIRETORIZADO ---
        function buildCalendar() {
            const grid = document.getElementById('calendarGrid');
            grid.innerHTML = '';

            // O mês da imagem começa na segunda-feira (Seg = 1). Deixamos o primeiro espaço vazio para o Domingo.
            const emptySpaces = 1;
            for (let i = 0; i < emptySpaces; i++) {
                const emptyDiv = document.createElement('div');
                grid.appendChild(emptyDiv);
            }

            // Renderizar os dias de 1 a 28 (conforme visível na imagem)
            for (let day = 1; day <= 27; day++) {
                const dayCard = document.createElement('div');
                dayCard.classList.add('calendar-day');

                // Div do Número
                const numDiv = document.createElement('div');
                numDiv.classList.add('day-number');
                numDiv.textContent = day;
                dayCard.appendChild(numDiv);

                // Destaque condicional do Dia Atual (Dia 15)
                if (day === 15) {
                    dayCard.classList.add('current-day');
                }

                // Inserção da Meta/Prova do Dia 19
                if (day === 19) {
                    const eventDiv = document.createElement('div');
                    eventDiv.classList.add('calendar-event');
                    eventDiv.textContent = 'Prova de Geo...';
                    dayCard.appendChild(eventDiv);

                    const dot = document.createElement('div');
                    dot.classList.add('event-indicator-dot');
                    dayCard.appendChild(dot);
                }

                grid.appendChild(dayCard);
            }
        }

        // --- TIMER DE FOCO (POMODORO EXTRA) ---
        let timerInterval;
        let isRunning = false;
        let timeRemaining = 25 * 60;

        function toggleTimer() {
            const startBtn = document.getElementById('startBtn');
            if (isRunning) {
                clearInterval(timerInterval);
                startBtn.textContent = 'Iniciar';
                isRunning = false;
            } else {
                isRunning = true;
                startBtn.textContent = 'Pausar';
                timerInterval = setInterval(() => {
                    if (timeRemaining > 0) {
                        timeRemaining--;
                        updateTimerDisplay();
                    } else {
                        clearInterval(timerInterval);
                        alert("Sessão de foco concluída com sucesso!");
                        resetTimer();
                    }
                }, 1000);
            }
        }

        function resetTimer() {
            clearInterval(timerInterval);
            isRunning = false;
            timeRemaining = 25 * 60;
            document.getElementById('startBtn').textContent = 'Iniciar';
            updateTimerDisplay();
        }

        function updateTimerDisplay() {
            const minutes = Math.floor(timeRemaining / 60).toString().padStart(2, '0');
            const seconds = (timeRemaining % 60).toString().padStart(2, '0');
            document.getElementById('timerDisplay').textContent = `${minutes}:${seconds}`;
        }

        // --- SIMULADOR DE FREQUÊNCIA CARDÍACA ---
        setInterval(() => {
            if(document.getElementById('saude').classList.contains('active')) {
                const randomBpm = Math.floor(Math.random() * (85 - 68 + 1)) + 68;
                document.getElementById('bpmValue').textContent = randomBpm;
            }
        }, 3000);

        // Inicialização do sistema
        window.onload = () => {
            buildCalendar();
        };
    </script>
</body>
</html>
