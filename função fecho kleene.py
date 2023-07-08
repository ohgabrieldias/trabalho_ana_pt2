def fecho_kleene(afnd):
    estados_iniciais = afnd.estados_iniciais
    estados_finais = afnd.estados_finais

    novo_estado = 'q0'  # Novo estado inicial

    conjunto_estados = afnd.conjunto_estados + [novo_estado]

    transicoes = {}
    for estado, transicoes_estado in afnd.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    # Adiciona transições vazias do novo estado inicial para o estado inicial anterior e para os estados finais anteriores
    transicoes[novo_estado] = {}
    for estado_final in estados_finais:
        if estado_final not in transicoes[novo_estado]:
            transicoes[novo_estado][estado_final] = []
        transicoes[novo_estado][estado_final].append(novo_estado)
    if afnd.estados_iniciais not in transicoes[novo_estado]:
        transicoes[novo_estado][afnd.estados_iniciais] = []
    transicoes[novo_estado][afnd.estados_iniciais].append(novo_estado)
    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)
