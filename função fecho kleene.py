def fecho_kleene_afnd(afnd):
    # Adicionando um novo estado inicial e uma transição vazia para o antigo estado inicial
    afnd['estados'].insert(0, 'q0')
    afnd['transicoes'].insert(0, {'origem': 'q0', 'simbolo': '', 'destino': afnd['estado_inicial']})

    # Adicionando uma nova transição vazia dos estados finais para o estado inicial
    for estado_final in afnd['estados_finais']:
        afnd['transicoes'].append({'origem': estado_final, 'simbolo': '', 'destino': afnd['estado_inicial']})

    # Adicionando uma nova transição vazia dos estados finais para os outros estados
    for estado_final in afnd['estados_finais']:
        for estado in afnd['estados']:
            afnd['transicoes'].append({'origem': estado_final, 'simbolo': '', 'destino': estado})

    # Atualizando os estados finais para incluir o novo estado inicial
    afnd['estados_finais'].append('q0')

    return afnd

# Exemplo de uso
afnd = {
    'estados': ['q1', 'q2'],
    'simbolos': ['0', '1'],
    'estado_inicial': 'q1',
    'estados_finais': ['q2'],
    'transicoes': [
        {'origem': 'q1', 'simbolo': '0', 'destino': 'q2'},
        {'origem': 'q2', 'simbolo': '1', 'destino': 'q1'}
    ]
}

resultado = fecho_kleene_afnd(afnd)
print(resultado)
