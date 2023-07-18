def uniao_afnd(a1, a2):
    novo_estado_inicial = 's0'  # Novo estado inicial
    estados_finais = a1.estados_finais + a2.estados_finais  # Combine os estados finais de a1 e a2

    conjunto_estados = a1.conjunto_estados + a2.conjunto_estados

    transicoes = {}
    transicoes[novo_estado_inicial] = {'ε': [a1.estados_iniciais[0], a2.estados_iniciais[0]]}  # Transições vazias do estado inicial para os iniciais de a1 e a2

    for estado, transicoes_estado in a1.transicoes.items():
        if estado in transicoes:
            transicoes[estado].update(transicoes_estado)
        else:
            transicoes[estado] = transicoes_estado.copy()

    for estado, transicoes_estado in a2.transicoes.items():
        if estado in transicoes:
            transicoes[estado].update(transicoes_estado)
        else:
            transicoes[estado] = transicoes_estado.copy()

    return AFND([novo_estado_inicial], conjunto_estados, estados_finais, transicoes)
