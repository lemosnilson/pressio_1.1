import math

# --- FUNÇÕES DE CÁLCULO INDIVIDUAIS (SEM ALTERAÇÃO) ---
def calcular_metodo_capacidade_solo(p_newtons, w_newtons, qa_pascals, B, C, H, Fb_pascals, Fv_pascals, modulo_de_seccao):
    a_reqd = (p_newtons + w_newtons) / qa_pascals if qa_pascals > 0 else float('inf')
    l_reqd = a_reqd / B if B > 0 else float('inf')
    lc = (l_reqd - C) / 2.0 if l_reqd > C else 0
    q_p = p_newtons / (l_reqd * B) if l_reqd * B > 0 else 0
    m = (q_p * B) * (lc ** 2) / 2
    f_b_calc = m / modulo_de_seccao if modulo_de_seccao > 0 else 0
    fb_percent = (f_b_calc / Fb_pascals) * 100 if Fb_pascals > 0 else 0
    v = (q_p * B) * (lc - H) if lc > H else 0
    f_v_calc = (1.5 * v) / (B * H) if (B * H) > 0 else 0
    fv_percent = (f_v_calc / Fv_pascals) * 100 if Fv_pascals > 0 else 0
    status = "RESISTE" if fb_percent <= 100 and fv_percent <= 100 else "NÃO RESISTE"
    fb_status = 'danger' if fb_percent > 100 else 'success'
    fv_status = 'danger' if fv_percent > 100 else 'success'
    return {
        "l_reqd": f"{l_reqd:.2f}", "fb_calc_mpa": f"{(f_b_calc / 1e6):.2f}",
        "fb_admissivel_mpa": f"{(Fb_pascals / 1e6):.2f}", "fv_calc_mpa": f"{(f_v_calc / 1e6):.2f}",
        "fv_admissivel_mpa": f"{(Fv_pascals / 1e6):.2f}", "fb_percent": f"{fb_percent:.1f}",
        "fv_percent": f"{fv_percent:.1f}", "status": status, "fb_status": fb_status, "fv_status": fv_status
    }

def calcular_metodo_resistencia_base(p_newtons, w_newtons, qa_pascals, B, C, H, Fb_pascals, Fv_pascals, modulo_de_seccao):
    m_max = Fb_pascals * modulo_de_seccao
    a_flex = p_newtons
    b_flex = -2 * p_newtons * C - 8 * m_max
    c_flex = p_newtons * C ** 2
    discriminante_flex = b_flex ** 2 - 4 * a_flex * c_flex
    leff_flexao = float('inf')
    if discriminante_flex >= 0 and a_flex != 0:
        leff_flexao = (-b_flex + math.sqrt(discriminante_flex)) / (2 * a_flex)
    vn_max = (Fv_pascals * B * H) / 1.5
    leff_cisalhamento = float('inf')
    if p_newtons > 2 * vn_max:
        leff_cisalhamento = (p_newtons * (C + 2 * H)) / (p_newtons - 2 * vn_max)
    leff = min(leff_flexao, leff_cisalhamento)
    modo_de_falha = "Flexão" if leff == leff_flexao else "Cisalhamento"
    q_t = (p_newtons + w_newtons) / (leff * B) if leff * B > 0 else 0
    qt_percent = (q_t / qa_pascals) * 100 if qa_pascals > 0 else 0
    status = "RESISTE" if qt_percent <= 100 else "NÃO RESISTE"
    qt_status = 'danger' if qt_percent > 100 else 'success'
    return {
        "leff": f"{leff:.2f}", "modo_falha": modo_de_falha, "qt_mpa": f"{(q_t / 1e6):.2f}",
        "qa_mpa": f"{(qa_pascals / 1e6):.2f}", "qt_percent": f"{qt_percent:.1f}",
        "status": status, "qt_status": qt_status
    }

# --- ALTERAÇÃO AQUI ---
def calcular_metodo_leff_efetivo(qa_pascals, w_newtons, L, B, H, C, Fb_pascals, Fv_pascals, E_pascals, modulo_de_seccao, momento_de_inercia):
    mn = Fb_pascals * modulo_de_seccao
    vn = (Fv_pascals * B * H) / 1.5
    a_flexao = qa_pascals * B
    b_flexao = (-2 * qa_pascals * B * C) - w_newtons
    c_flexao = (qa_pascals * B * C ** 2) + (2 * C * w_newtons) - (8 * mn)
    discriminante_flexao = b_flexao ** 2 - 4 * a_flexao * c_flexao
    leff_flexao = float('inf')
    if discriminante_flexao >= 0 and a_flexao !=0:
        leff_flexao = (-b_flexao + math.sqrt(discriminante_flexao)) / (2 * a_flexao)
    a_cisalhamento = qa_pascals * B
    b_cisalhamento = (-2 * vn) - (qa_pascals * B * C) - (2 * qa_pascals * B * H) - w_newtons
    c_cisalhamento = (w_newtons * C) + (2 * w_newtons * H)
    discriminante_cisalhamento = b_cisalhamento ** 2 - 4 * a_cisalhamento * c_cisalhamento
    leff_cisalhamento = float('inf')
    if discriminante_cisalhamento >= 0 and a_cisalhamento != 0:
        leff_cisalhamento = (-b_cisalhamento + math.sqrt(discriminante_cisalhamento)) / (2 * a_cisalhamento)
    termo_interno = (0.06 * E_pascals * momento_de_inercia) / (0.9 * qa_pascals * B) if (0.9 * qa_pascals * B) > 0 else 0
    lc_deflexao = termo_interno ** (1 / 3.0)
    leff_deflexao = (2 * lc_deflexao) + C
    
    # --- MUDANÇA IMPORTANTE: Calculamos o leff mínimo necessário, sem limitá-lo por L ---
    leff_minimo_calculado = min(leff_flexao, leff_cisalhamento, leff_deflexao)
    
    return {
        "leff_flexao": leff_flexao, "leff_cisalhamento": leff_cisalhamento,
        "leff_deflexao": leff_deflexao, "l_real": L, 
        "leff_minimo_calculado": leff_minimo_calculado # Retornamos o valor "sem teto"
    }

# --- FUNÇÕES DE RESUMO (SEM ALTERAÇÃO) ---
def calcular_metricas_resumo(perc_comprimento_ativo, qt_operacao, qa_pascals):
    perc_capacidade_solo = (qt_operacao / qa_pascals) * 100 if qa_pascals > 0 else 0
    return {
        'perc_comprimento_ativo': f"{perc_comprimento_ativo:.1f}",
        'perc_capacidade_solo': f"{perc_capacidade_solo:.1f}"
    }

def calcular_comparativos_pressao(p_newtons, w_newtons, L_real, B, C, H):
    area_total = L_real * B
    pressao_total_pa = (p_newtons + w_newtons) / area_total if area_total > 0 else 0
    pressao_total_kgf = pressao_total_pa / 98066.5
    largura_dispersa = C + 2 * H
    comprimento_disperso = C + 2 * H
    area_dispersa = largura_dispersa * comprimento_disperso
    pressao_dispersa_pa = (p_newtons + w_newtons) / area_dispersa if area_dispersa > 0 else 0
    pressao_dispersa_kgf = pressao_dispersa_pa / 98066.5
    return {
        'pressao_total_kgf': f"{pressao_total_kgf:.2f}",
        'pressao_dispersa_kgf': f"{pressao_dispersa_kgf:.2f}"
    }

# --- FUNÇÃO PRINCIPAL (COM ALTERAÇÕES SIGNIFICATIVAS) ---
# Substitua a sua função principal por esta versão
def realizar_analise_completa(dados_entrada):
    try:
        # --- Coleta e conversão de dados ---
        C = float(dados_entrada.get('c', 0).replace(',', '.'))
        F = float(dados_entrada.get('p_tf', 0).replace(',', '.'))
        S_soil = float(dados_entrada.get('qa', 0).replace(',', '.'))
        L = float(dados_entrada.get('l_real', 0).replace(',', '.'))
        B = float(dados_entrada.get('b', 0).replace(',', '.'))
        H = float(dados_entrada.get('d', 0).replace(',', '.'))
        rho = float(dados_entrada.get('densidade', 0).replace(',', '.'))
        Fb = float(dados_entrada.get('fb', 0).replace(',', '.'))
        Fv = float(dados_entrada.get('fv', 0).replace(',', '.'))
        E_gpa = float(dados_entrada.get('e_gpa', 0).replace(',', '.'))
        
        volume = L * B * H
        w_newtons = (volume * rho) * 9.81
        p_newtons = F * 9810
        qa_pascals = S_soil * 98100
        Fb_pascals = Fb * 1e6
        Fv_pascals = Fv * 1e6
        E_pascals = E_gpa * 1e9
        modulo_de_seccao = (B * H ** 2) / 6
        momento_de_inercia = (B * H ** 3) / 12

        # --- Cálculos dos métodos ---
        resultados_m3 = calcular_metodo_leff_efetivo(qa_pascals, w_newtons, L, B, H, C, Fb_pascals, Fv_pascals, E_pascals, modulo_de_seccao, momento_de_inercia)
        
        leff_minimo_calculado = resultados_m3['leff_minimo_calculado']
        leff_operacional = min(leff_minimo_calculado, L)
        qt_operacao = (p_newtons + w_newtons) / (leff_operacional * B) if (leff_operacional * B) > 0 else 0
        perc_comprimento_ativo = (leff_minimo_calculado / L) * 100 if L > 0 else 0
        
        metricas = calcular_metricas_resumo(perc_comprimento_ativo, qt_operacao, qa_pascals)
        comparativos = calcular_comparativos_pressao(p_newtons, w_newtons, L, B, C, H)
        resumo_comparativo = {**metricas, **comparativos}

        # --- Lógica de verificação de aprovação/reprovação ---
        condicao_falha_comprimento = leff_minimo_calculado > L
        perc_solo_float = float(resumo_comparativo['perc_capacidade_solo'])
        condicao_falha_solo = perc_solo_float > 100.0
        
        resumo_comparativo['falha_por_comprimento'] = condicao_falha_comprimento
        resumo_comparativo['falha_por_solo'] = condicao_falha_solo
        resumo_comparativo['excesso_comprimento_perc'] = 0
        resumo_comparativo['excesso_solo_perc'] = 0

        if condicao_falha_comprimento or condicao_falha_solo:
            resumo_comparativo['status_geral'] = "REPROVADO"
            if condicao_falha_comprimento and L > 0:
                excesso = ((leff_minimo_calculado / L) - 1) * 100
                resumo_comparativo['excesso_comprimento_perc'] = f"{excesso:.1f}"
            if condicao_falha_solo:
                excesso_solo = perc_solo_float - 100.0
                resumo_comparativo['excesso_solo_perc'] = f"{excesso_solo:.1f}"
        else:
            resumo_comparativo['status_geral'] = "APROVADO"

        # --- Adiciona os valores brutos para a lógica de cores no template ---
        resumo_comparativo['perc_comprimento_ativo_raw'] = perc_comprimento_ativo
        resumo_comparativo['perc_capacidade_solo_raw'] = perc_solo_float

        # --- Montagem do resultado final ---
        resultados_finais = {
            "analises_leff": [],
            "resumo_comparativo": resumo_comparativo,
            "sucesso": True
        }
        
        leffs_calculados = [
            ("Flexão", resultados_m3['leff_flexao']), ("Cisalhamento", resultados_m3['leff_cisalhamento']),
            ("Deformação", resultados_m3['leff_deflexao'])
        ]
        for nome, leff_valor in leffs_calculados:
            pressao_gerada_kgf_cm2, delta_mm = 0, 0
            if leff_valor != float('inf') and B > 0:
                pressao_gerada_pa = (p_newtons + w_newtons) / (leff_valor * B)
                pressao_gerada_kgf_cm2 = pressao_gerada_pa / 98066.5
                lc_valor = (leff_valor - C) / 2.0
                q_para_delta = p_newtons / (leff_valor * B)
                numerador = q_para_delta * B * (lc_valor ** 4)
                denominador = 8 * E_pascals * momento_de_inercia
                if denominador > 0:
                    delta_m = numerador / denominador
                    delta_mm = delta_m * 1000
            is_governing = (leff_valor == leff_minimo_calculado)
            resultados_finais['analises_leff'].append({
                'titulo': f"Limite de {nome}", 'leff': f"{leff_valor:.2f} m",
                'pressao_gerada': f"{pressao_gerada_kgf_cm2:.1f} kgf/cm²",
                'deformacao_mm': f"{delta_mm:.1f} mm", 'is_governing': is_governing
            })

        return resultados_finais
    except (ValueError, KeyError, TypeError) as e:
        return {"erro": f"Erro nos dados de entrada: {e}.", "sucesso": False}
