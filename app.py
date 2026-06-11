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
                    if ev_date_str not in dict_eventos:
                        dict_eventos[ev_date_str] = []
                    dict_eventos[ev_date_str].append(ev)

            meses_nomes = {1: "JANEIRO", 2: "FEVEREIRO", 3: "MARÇO", 4: "ABRIL", 5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO", 9: "SETEMBRO", 10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"}
            nome_do_mes = meses_nomes.get(mes_atual, "CRONOGRAMA")
            
            html_calendario = "<div style='text-align: center; margin-bottom: 15px; font-family: \"Kanit\", sans-serif; font-size: 16px; color: #ffffff; font-weight: 600; letter-spacing: 2px;'>" + nome_do_mes + " " + str(ano_atual) + "</div>"
            html_calendario += "<div class='jarvis-calendar-grid'>"
            
            for hd in dias_semana_headers:
                html_calendario += f"<div class='calendar-header-day'>{hd}</div>"
                
            # O loop corrigido acessa os dias de forma limpa e direta
            for semana in mes_dias:
                for dia in semana:
                    if dia == 0:
                        html_calendario += "<div class='calendar-cell cell-empty'></div>"
                    else:
                        data_corrente = datetime.date(ano_atual, mes_atual, dia)
                        data_corrente_str = data_corrente.isoformat()
                        classe_hoje = "cell-today" if data_corrente == hoje else ""
                        
                        html_tags_eventos = ""
                        if data_corrente_str in dict_eventos:
                            for ev in dict_eventos[data_corrente_str]:
                                html_tags_eventos += f"<div class='calendar-event-tag' title='{ev['time']} - {ev['title']}'>{ev['time']} - {ev['title']}</div>"
                                
                        html_calendario += f"""
                            <div class='calendar-cell {classe_hoje}'>
                                <div class='cell-number'>{dia}</div>
                                <div class='cell-events-container'>
                                    {html_tags_eventos}
                                </div>
                            </div>
                        """
                        
            html_calendario += "</div>"
            st.markdown(html_calendario, unsafe_allow_html=True)
