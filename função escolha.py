def escolha_afnd(a1, a2):
    estado_inicial = "s"
    estado_final = "f"

    estados_finais = [estado_final]

    transicoes = {}
    transicoes[estado_inicial] = {}
    transicoes[estado_inicial][None] = [a1.estados_iniciais[0], a2.estados_iniciais[0]]

    for estado in a1.estados_finais:
        if estado in a1.transicoes:
            transicoes[estado][None] = [estado_final]

    for estado in a2.estados_finais:
        if estado in a2.transicoes:
            transicoes[estado][None] = [estado_final]

    return AFND([estado_inicial], estados_finais, transicoes)
