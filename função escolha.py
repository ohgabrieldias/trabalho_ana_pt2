def uniao_afnd(a1, a2):
    estados_iniciais = ['s0']  # Novo estado inicial
    estados_finais = ['f0']  # Novo estado final

    novo_estado = 's1'  # Novo estado para transição entre a1 e a2

    conjunto_estados = a1.conjunto_estados + a2.conjunto_estados
    conjunto_estados.remove(a1.estados_finais[0])
    conjunto_estados.remove(a2.estados_finais[0])
    conjunto_estados += [novo_estado]  # adiciona o novo estado

    transicoes = {}
    transicoes[novo_estado] = {'ε': [a1.estados_iniciais[0], a2.estados_iniciais[0]]}  # ε-transição do novo estado inicial para os estados a1 e a2

    for estado, transicoes_estado in a1.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    for estado, transicoes_estado in a2.transicoes.items():
        if estado in transicoes:
            transicoes[estado].update(transicoes_estado)
        else:
            transicoes[estado] = transicoes_estado.copy()

    transicoes[a1.estados_finais[0]] = {'ε': [estados_finais[0]]}  # ε-tarnsição do estado final de a1 para o novo estado final
    transicoes[a2.estados_finais[0]] = {'ε': [estados_finais[0]]}  # ε-tarnsição do estado final de a2 para o novo estado final

    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)
