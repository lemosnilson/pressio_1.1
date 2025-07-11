# -*- coding: utf-8 -*-
import math

"""
Script para calcular o Comprimento de Apoio Efetivo (Leff) de uma base de grua (Crane Mat)
baseado no paper "Effective Bearing Length of Crane Mats" de David Duerr.

Este script implementa o "Effective Length Calculation Method" para bases de madeira (timber)
e segue as convenções de estilo do código Python (PEP 8).
As unidades de entrada foram personalizadas para o uso prático da engenharia de cargas.
"""


# --- Função para Entrada de Dados ---
def obter_entrada_numerica(prompt):
    """
    Solicita uma entrada numérica ao utilizador, aceitando '.' e ',' como separadores decimais.
    Continua a pedir até que uma entrada válida seja fornecida.

    Args:
        prompt (str): A mensagem a ser exibida ao utilizador.

    Returns:
        float: O número inserido pelo utilizador como um float.
    """
    while True:
        entrada = input(prompt)
        try:
            valor = float(entrada.replace(',', '.'))
            return valor
        except ValueError:
            print("Erro: Por favor, insira um valor numérico válido.")


# --- Função Principal de Cálculo (Versão com ordem de entrada ajustada) ---
def calcular_leff():
    """
    Função principal que coleta os dados e calcula os diferentes valores de Leff,
    usando unidades práticas e convertendo-as internamente para SI.
    """
    print("--- Cálculo do Comprimento de Apoio Efetivo (Leff) de uma Base de Grua ---")
    print("Por favor, insira os valores nas unidades personalizadas indicadas.")
    print("-" * 70)

    # --- Coleta de Dados de Entrada com Ordem Ajustada ---
    print("--- Dados do Solo e Geometria ---")
    qa = obter_entrada_numerica("1. Pressão admissível do solo (qa) [kgf/cm²]: ")

    # Ordem dos dados geométricos ajustada conforme solicitado
    l_real = obter_entrada_numerica("2. Comprimento da base (l_real) [metros - m]: ")
    b = obter_entrada_numerica("3. Largura da base (b) [metros - m]: ")
    d = obter_entrada_numerica("4. Altura da base (d) [metros - m]: ")

    c = obter_entrada_numerica("5. Largura da sapata da grua (c) [metros - m]: ")

    print("\n--- Dados de Carga e Material ---")
    w_tf = obter_entrada_numerica("6. Peso próprio da base (w) [toneladas-força - tf]: ")
    fb = obter_entrada_numerica("7. Tensão admissível à flexão (fb) [Pascals - Pa]: ")
    fv = obter_entrada_numerica("8. Tensão admissível ao cisalhamento (fv) [Pascals - Pa]: ")
    e = obter_entrada_numerica("9. Módulo de elasticidade do material (e) [GPa]: ")

    # --- Conversão de Unidades para o Padrão SI (Pascals, Newtons) ---
    qa_pascals = qa * 98100  # Converte kgf/cm² para Pascals
    w_newtons = w_tf * 9810  # Converte toneladas-força (tf) para Newtons
    e_pascals = e * 1e9  # Converte GPa para Pascals

    print("\n--- A calcular... ---")
    print(f"(Nota: {qa} kgf/cm² convertidos para {qa_pascals:.0f} Pa)")
    print(f"(Nota: {w_tf} tf convertidos para {w_newtons:.0f} N)")
    print(f"(Nota: {e} GPa convertidos para {e_pascals:.0f} Pa)")

    # --- Cálculos Intermédios ---
    modulo_de_seccao = (b * d ** 2) / 6
    momento_de_inercia = (b * d ** 3) / 12

    mn = fb * modulo_de_seccao
    vn = (fv * b * d) / 1.5

    # --- 1. Cálculo do Leff baseado na FLEXÃO ---
    a_flexao = qa_pascals * b
    b_flexao = (-2 * qa_pascals * b * c) - w_newtons
    c_flexao = (qa_pascals * b * c ** 2) + (2 * c * w_newtons) - (8 * mn)

    discriminante_flexao = b_flexao ** 2 - 4 * a_flexao * c_flexao
    leff_flexao = float('inf')
    if discriminante_flexao >= 0:
        leff_flexao = (-b_flexao + math.sqrt(discriminante_flexao)) / (2 * a_flexao)

    # --- 2. Cálculo do Leff baseado no CISALHAMENTO ---
    a_cisalhamento = qa_pascals * b
    b_cisalhamento = (-2 * vn) - (qa_pascals * b * c) - (2 * qa_pascals * b * d) - w_newtons
    c_cisalhamento = (w_newtons * c) + (2 * w_newtons * d)

    discriminante_cisalhamento = b_cisalhamento ** 2 - 4 * a_cisalhamento * c_cisalhamento
    leff_cisalhamento = float('inf')
    if discriminante_cisalhamento >= 0:
        leff_cisalhamento = (-b_cisalhamento + math.sqrt(discriminante_cisalhamento)) / (2 * a_cisalhamento)

    # --- 3. Cálculo do Leff baseado na DEFLEXÃO ---
    termo_interno = (0.06 * e_pascals * momento_de_inercia) / (0.9 * qa_pascals * b)
    lc_deflexao = termo_interno ** (1 / 3.0)
    leff_deflexao = (2 * lc_deflexao) + c

    # --- Determinação do Leff Final ---
    leff_final = min(leff_flexao, leff_cisalhamento, leff_deflexao, l_real)

    # --- Apresentação dos Resultados ---
    print("\n--- Resultados do Cálculo (em metros) ---")
    print(f"Leff baseado na Flexão: {leff_flexao:.4f} m")
    print(f"Leff baseado no Cisalhamento: {leff_cisalhamento:.4f} m")
    print(f"Leff baseado na Deflexão: {leff_deflexao:.4f} m")
    print(f"Comprimento real da base (l_real): {l_real:.4f} m")
    print("-" * 40)
    print(f"O Comprimento de Apoio Efetivo (Leff) final é: {leff_final:.4f} m")
    print("Este é o menor valor entre os calculados e o comprimento real da base.")
    print("-" * 70)


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    calcular_leff()