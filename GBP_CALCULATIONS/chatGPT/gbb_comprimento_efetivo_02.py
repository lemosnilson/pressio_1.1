#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprimento Efetivo Exato (v3.1)
Solução numérica da Eq. 5 para carga pontual no centro,
resolvendo p(x)=k_s·w(x)=p_lim via diferenças finitas,
com cálculo de I = B·t³/12 e detecção correta de x₀.
"""

import math
import numpy as np

def parse_float(prompt):
    """Lê float do usuário, aceitando vírgula ou ponto como decimal."""
    while True:
        s = input(prompt).strip().replace(',', '.')
        try:
            return float(s)
        except ValueError:
            print('Entrada inválida. Digite um número válido.')

def main():
    # 1) Parâmetros geotécnicos e p_lim
    padm    = parse_float('P_adm (kgf/cm²): ')
    padm_pa = padm * 98066.5
    frac    = parse_float('Fração limite p_lim (ex: 0.10): ')
    p_lim   = padm_pa * frac                                    # Eq. 4 :contentReference[oaicite:0]{index=0}

    ks_kn   = parse_float('Coeficiente k_s (kN/m³): ')
    ks      = ks_kn * 1e3                                       # kN/m³ → N/m³

    # 2) Propriedades do mats e carga
    F_t     = parse_float('Carga F (toneladas métricas): ')
    F       = F_t * 1000 * 9.80665                              # t→kg→N

    L       = parse_float('Comprimento do mats L (m): ')
    B       = parse_float('Largura do mats B (m): ')
    t       = parse_float('Espessura do mats t (m): ')
    E_gpa   = parse_float('Módulo de elasticidade E (GPa): ')
    E       = E_gpa * 1e9                                        # GPa→Pa

    # 3) Cálculo de I e EI
    I  = (B * t**3) / 12.0                                       # seção retangular
    EI = E * I

    # 4) Monta malha em x ∈ [–2L, +2L]
    x_min, x_max = -2*L, 2*L
    N            = 801                                           # ímpar para ter x=0 exato
    x            = np.linspace(x_min, x_max, N)
    dx           = x[1] - x[0]

    # 5) Configura sistema A·w = b para d4w/dx4 + (ks/EI)w = F/(EI)·δ
    A = np.zeros((N, N))
    b = np.zeros(N)
    coeff_k = (ks/EI) * dx**4

    # pontos internos
    for i in range(2, N-2):
        A[i, i-2] =  1
        A[i, i-1] = -4
        A[i, i]   =  6 + coeff_k
        A[i, i+1] = -4
        A[i, i+2] =  1

    # carregamento pontual no centro (x=0)
    m      = N//2
    b[m]   = F/EI * dx**3               # δ discretizada como 1/dx → F/(EI)*dx⁴*(1/dx)

    # condições de contorno de viga “infinita”
    A[0, 0]     = 1
    A[N-1, N-1] = 1
    A[1, 0]     = -3; A[1, 1]     =  4; A[1, 2]     = -1; b[1]     = 0
    A[N-2, N-1] = -3; A[N-2, N-2] =  4; A[N-2, N-3] = -1; b[N-2] = 0

    # 6) Resolve o sistema
    w = np.linalg.solve(A, b)
    p = ks * w

    # 7) Determina L_eff corrigindo detecção de x₀
    right = m
    while right < N and p[right] >= p_lim:
        right += 1
    x0    = x[right]               # primeiro x em que p< p_lim
    L_eff = 2 * x0                                          # Etapa 6 :contentReference[oaicite:1]{index=1}

    # 8) RR (Eq. 3) e saída
    RR = (E * I) / (ks * (L * B))                           # Eq. 3 :contentReference[oaicite:2]{index=2}

    # Impressão passo a passo
    print('\n=== Resultados Exatos v3.1 ===')
    print(f'P_adm (Pa)          = {padm_pa:.3f}')
    print(f'p_lim               = {p_lim:.3f}')
    print(f'ks (N/m³)           = {ks:.3e}')
    print(f'Força (N)           = {F:.3f}')
    print(f'I (m⁴)              = {I:.6e}')
    print(f'EI (N·m²)           = {EI:.6e}')
    print(f'Mesh dx             = {dx:.6f} m')
    print(f'Índice central m    = {m}, x=0')
    print(f'Raiz x₀             = {x0:.6f} m')
    print(f'L_eff               = {L_eff:.6f} m')
    print(f'Rigidez Relativa (RR)= {RR:.6e}')

if __name__ == '__main__':
    main()
