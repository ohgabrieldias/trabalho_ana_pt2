def uniao_afnd(a1, a2):
    estados_iniciais = ['s0']  # New initial state
    estados_finais = ['f0']  # New final state

    novo_estado = 's1'  # New state for transition between a1 and a2

    conjunto_estados = a1.conjunto_estados + a2.conjunto_estados
    conjunto_estados.remove(a1.estados_finais[0])
    conjunto_estados.remove(a2.estados_finais[0])
    conjunto_estados += [novo_estado]  # Add new state

    transicoes = {}
    transicoes[novo_estado] = {'ε': [a1.estados_iniciais[0], a2.estados_iniciais[0]]}  # ε-transition from new state to initial states of a1 and a2

    for estado, transicoes_estado in a1.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    for estado, transicoes_estado in a2.transicoes.items():
        if estado in transicoes:
            transicoes[estado].update(transicoes_estado)
        else:
            transicoes[estado] = transicoes_estado.copy()

    transicoes[a1.estados_finais[0]] = {'ε': [estados_finais[0]]}  # ε-transition from final state of a1 to new final state
    transicoes[a2.estados_finais[0]] = {'ε': [estados_finais[0]]}  # ε-transition from final state of a2 to new final state

    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)
