import os
import random
import ply.lex as lex
import ply.yacc as yacc

# Variáveis globais
afdn1 = None
afdn2 = None
afdnResul = None
# Defina t lista de nomes dos tokens
tokens = (
    'SIMBOLO',
    'OU',
    'ESTRELA_KLEENE',
    'PARENTESE_ESQ',
    'PARENTESE_DIR',
)

# Defina os padrões de expressões regulares para os tokens
t_SIMBOLO = r'[01]'
t_OU = r'\|'
t_ESTRELA_KLEENE = r'\*'
t_PARENTESE_ESQ = r'\('
t_PARENTESE_DIR = r'\)'

# Ignore caracteres de espaço em branco
t_ignore = ' \t\n'

# Tratamento de erro para caracteres não reconhecidos
def t_error(t):
    print(f"Caractere não reconhecido: {t.value[0]}")
    t.lexer.skip(1)

# Construa o lexer
lexer = lex.lex()

# Definição da classe Node para representar os nós da árvore sintática
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)

# Regras da gramática
def p_expression(p):
    '''
    expression : termo
               | expression OU termo
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = Node("OU", [p[1], p[3]])


def p_termo(p):
    '''
    termo : fator
          | termo fator
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Node("CONCATENACAO", [p[1], p[2]])

def p_fator(p):
    '''
    fator : atom
          | fator ESTRELA_KLEENE
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Node("ESTRELA_KLEENE", [p[1]])

def p_atom(p):
    '''
    atom : SIMBOLO
         | PARENTESE_ESQ expression PARENTESE_DIR
    '''
    if len(p) == 2:
        p[0] = Node("sym",[p[1]])
    elif len(p) == 4:
        p[0] = p[2]

# Tratamento de erro para erros de sintaxe
def p_error(p):
    print("Erro de sintaxe")

# Construa o parser
parser = yacc.yacc()

class AFND:
    def __init__(self, estados_iniciais, conjunto_estados, estados_finais, δ):
        self.estados_iniciais = estados_iniciais
        self.estados_finais = estados_finais
        self.conjunto_estados = conjunto_estados
        self.transicoes = δ
##############################################################################################################
def concatenacaov2(a1, a2):
    estados_iniciais = a1.estados_iniciais
    estados_finais = a2.estados_finais
    novo_estado = a1.estados_finais[0] + a2.estados_iniciais[0]  # Estado inicial de a2 como novo estado

    conjunto_estados =  a1.conjunto_estados + [novo_estado] + a2.conjunto_estados
    conjunto_estados.remove(a1.estados_finais[0])  # Remove o estado final de a1 do conjunto de estados
    conjunto_estados.remove(a2.estados_iniciais[0]) # Remove o estado inicial de a2 do conjunto de estados

    transicoes = {}
    transicoes_tmp = {}
    transicoes_tmp[novo_estado] = {}

    # Atualiza o nome dos estados finais de a1 para o novo nome
    for estado in a1.transicoes:
        for simbolo in a1.transicoes[estado]:
            if a1.transicoes[estado][simbolo] == [a1.estados_finais[0]]: 
                a1.transicoes[estado][simbolo] = [novo_estado]

    a1.estados_finais[0] = novo_estado

    for estado in a2.transicoes:
        for simbolo in a2.transicoes[estado]:
            if estado == a2.estados_iniciais[0]:
                transicoes_tmp[novo_estado][simbolo] = [a2.estados_finais[0]]
                del a2.transicoes[estado][simbolo]
                break

    a2.transicoes[novo_estado] = transicoes_tmp[novo_estado]
    a2.estados_iniciais[0] = novo_estado

    # Copia as transições de a1 e a2 para o novo autômato
    for estado, transicoes_estado in a1.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()
   
    for estado, transicoes_estado in a2.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    # Atualiza a primeira transição das transições para ter o estado final de a1 como estado inicial de a2
    for estado in transicoes:
        for simbolo in transicoes[estado]:
            if transicoes[estado][simbolo] == [a1.estados_finais[0]]:  # Testa se o proximo estado é o estado final de a1
                transicoes[estado][simbolo] = [a2.estados_iniciais[0]]  # Atualiza o estado final de a1 para o estado inicial de a2

    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)
##############################################################################################################
def concatenacao(a1, a2):
    estados_iniciais = a1.estados_iniciais
    estados_finais = a2.estados_finais
    novo_estado = a2.estados_iniciais[0]  # Estado inicial de a2 como novo estado

    conjunto_estados =  a1.conjunto_estados + a2.conjunto_estados
    conjunto_estados.remove(a1.estados_finais[0])  # Remove o estado final de a1 do conjunto de estados

    transicoes = {}
    for estado, transicoes_estado in a1.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    for estado, transicoes_estado in a2.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    # Atualiza a primeira transição das transições para ter o estado final de a1 como estado inicial de a2
    for estado in transicoes:
        for simbolo in transicoes[estado]:
            # print(transicoes[estado][simbolo], "==" ,a1.estados_finais[0])
            if transicoes[estado][simbolo] == [a1.estados_finais[0]]:  
                transicoes[estado][simbolo] = [a2.estados_iniciais[0]]

    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)
##############################################################################################################
def uniao_afnd(a1, a2):
    estado_inicial = "s0"
    estados_finais = a1.estados_finais + a2.estados_finais

    transicoes = {}
    transicoes[estado_inicial] = {}
    for estado in a1.estados_iniciais:
        if estado in a1.transicoes:
            transicoes[estado_inicial].update(a1.transicoes[estado])

    transicoes[estado_inicial].update(a2.estados_iniciais)

    return AFND([estado_inicial], estados_finais, transicoes)


##############################################################################################################

def fecho_kleene(afnd):
    estado_inicial = "s0"
    conjunto_estados = afnd.conjunto_estados.copy()
    transicoes = {}

    for estado, transicoes_estado in afnd.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    estado_final_str = "f" + str(len(conjunto_estados))
    conjunto_estados.append(estado_final_str)

    # Adiciona transição vazia do estado inicial para o estado final
    if "ε" not in transicoes[estado_inicial]:
        transicoes[estado_inicial]["ε"] = [estado_final_str]
    else:
        transicoes[estado_inicial]["ε"].append(estado_final_str)

    # Adiciona transições do estado final para o estado inicial
    estado_final_str = "f" + str(len(conjunto_estados))
    conjunto_estados.append(estado_final_str)

    if "3" not in transicoes[estado_inicial]:
        transicoes[estado_inicial]["3"] = [estado_final_str]
    else:
        transicoes[estado_inicial]["3"].append(estado_final_str)

    # Adiciona transição do estado final f2 para o estado f33
    estado_f33_str = "f" + str(len(conjunto_estados))
    conjunto_estados.append(estado_f33_str)

    if "1" not in transicoes["f2"]:
        transicoes["f2"]["1"] = [estado_f33_str]
    else:
        transicoes["f2"]["1"].append(estado_f33_str)

    # Adiciona transição do estado f33 para o estado inicial s0
    if "3" not in transicoes[estado_f33_str]:
        transicoes[estado_f33_str]["3"] = [estado_inicial]
    else:
        transicoes[estado_f33_str]["3"].append(estado_inicial)

    estados_finais = [estado_final_str]

    # Adiciona transições vazias dos estados finais originais para o estado final
    for estado_final in afnd.estados_finais:
        estado_final_str = str(estado_final)
        if estado_final_str not in transicoes:
            transicoes[estado_final_str] = {}
        if "ε" not in transicoes[estado_final_str]:
            transicoes[estado_final_str]["ε"] = [estado_final_str]

    # Adiciona transições para cada símbolo do autômato original
    for estado in conjunto_estados:
        for simbolo in afnd.transicoes.get(estado, {}):
            if simbolo not in transicoes[estado]:
                transicoes[estado][simbolo] = afnd.transicoes[estado][simbolo]

    return AFND([estado_inicial], conjunto_estados, estados_finais, transicoes)


##############################################################################################################
def criar_afnd_simbolo(simbolo):
    estado_inicial = "s" + str(random.randint(0, 99))
    estado_final = "f" + str(random.randint(0, 99))
    conjunto_estados = [estado_inicial, estado_final]
    estados_finais = [estado_final]

    transicoes = {}
    transicoes[estado_inicial] = {}
    transicoes[estado_inicial][simbolo] = [estado_final]
    return AFND([estado_inicial],conjunto_estados, estados_finais, transicoes)
##### printa AFDN ############################################################################################
def print_afdn(afnd):
    print("Estados Iniciais(s):", afnd.estados_iniciais)
    print("Estados Finais (F):", afnd.estados_finais)
    print("Conjunto de Estados (K):", afnd.conjunto_estados)
    print("Transições (δ):")
    for estado, transicoes in afnd.transicoes.items():
        for simbolo, destinos in transicoes.items():
            print(f"δ:({estado} --({simbolo})--> {destinos})")
    print("\n")
##############################################################################################################
def gerar_automato(arvore):
    if isinstance(arvore, Node):
        if arvore.value == "CONCATENACAO":
            afdn_esquerdo = gerar_automato(arvore.children[0])
            # print_afdn(afdn_esquerdo)
            afdn_direito = gerar_automato(arvore.children[1])
            # print_afdn(afdn_direito)
            return concatenacaov2(afdn_esquerdo,afdn_direito)
        elif arvore.value == "OU":
            afdn_esquerdo = gerar_automato(arvore.children[0])
            afdn_direito = gerar_automato(arvore.children[1])
            return uniao_afnd(afdn_esquerdo, afdn_direito)
        elif arvore.value == "ESTRELA_KLEENE":
            afdn = gerar_automato(arvore.children[0])
            return fecho_kleene(afdn)
        elif arvore.value == "sym":
            simbolo = arvore.children[0]
            return criar_afnd_simbolo(simbolo)
    return None

##############################################################################################################
def save_afdn_to_file(afnd, filename):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, filename)
    with open(file_path, 'w') as file:
        file.write("M = (K, Σ, δ, s, F)\n")
        file.write("M = (K"+ str(afnd.conjunto_estados)+", Σ[0,1], δ, s"+ str(afnd.estados_iniciais)+", F"+ str(afnd.estados_finais)+")\n")
        file.write("Transições (δ):\n")
        for estado, transicoes in afnd.transicoes.items():
            for simbolo, destinos in transicoes.items():
                file.write(f"δ:({estado} --({simbolo})--> {destinos})\n")
        file.write("\n")
        file.write("Conjunto de estados Iniciais(s): " + str(afnd.estados_iniciais) + "\n")
        file.write("Conjunto de estados Finais (F): " + str(afnd.estados_finais) + "\n")
        file.write("Conjunto de estados (K): " + str(afnd.conjunto_estados) + "\n")
       
     

##############################################################################################################
# Função auxiliar para imprimir a árvore sintática
def print_tree(node, level=0):
    if isinstance(node, Node):
        print("  " * level + node.value)
        for child in node.children:
            print_tree(child, level+1)
    else:
        print("  " * level + node)

# Teste o lexer e parser
expressao = "(01001)"
lexer.input(expressao)
# for token in lexer:
#     print(token)

resultado = parser.parse(expressao)
# print_tree(resultado)
automato = gerar_automato(resultado)
print_afdn(automato)
save_afdn_to_file(automato, "automato.txt")
