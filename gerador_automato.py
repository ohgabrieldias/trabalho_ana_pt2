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
def concatenacao(a1, a2):
    estados_iniciais = a1.estados_iniciais
    estados_finais = a2.estados_finais
    novo_estado = a2.estados_iniciais[0]  # Estado inicial de a2 como novo estado

    conjunto_estados = a1.estados_iniciais + [novo_estado] + a2.estados_finais

    transicoes = {}
    for estado, transicoes_estado in a1.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    for estado, transicoes_estado in a2.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    # Atualiza a primeira transição das transições para ter o estado final de a1 como estado inicial de a2
    for estado in transicoes:
        for simbolo in transicoes[estado]:
            print(transicoes[estado][simbolo], "==" ,a1.estados_finais[0])
            if transicoes[estado][simbolo] == [a1.estados_finais[0]]:  
                transicoes[estado][simbolo] = [a2.estados_iniciais[0]]

    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)
##############################################################################################################
def concatenacao_v2(a1, a2):
    estados_iniciais = a1.estados_iniciais
    estados_finais = a2.estados_finais
    # cria um novo estado contatenando os estados finais do a1 com os estados iniciais do a2
    novo_estado = a1.estados_iniciais[0] + a2.estados_finais[0]
    # adiciona o novo estado ao conjunto de estados
    conjunto_estados = a1.estados_iniciais + [novo_estado] + a2.estados_finais

    transicoes  = a1.transicoes
    for estado in conjunto_estados:
        estado_atual = estado
        if estado in a1.transicoes:
            for simbolo in a1.transicoes[estado]:
                transicoes[estado_atual][simbolo] = novo_estado
    for estado in a2.estados_iniciais:
        transicoes[novo_estado] = a2.transicoes[estado]

    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)

###############################################################################################################
def concatenacao_afnd(a2, a1):
    estados_iniciais = a1.estados_iniciais
    estados_finais = a2.estados_finais

    #print(estados_iniciais)
    #print(estados_finais)
    transicoes = {}
    for estado in a1.estados_finais:
        if estado in a1.transicoes:
            transicoes[estado] = a1.transicoes[estado]

    for estado in a2.estados_iniciais:
        if estado in a2.transicoes:
            if estado in transicoes:
                for simbolo in a2.transicoes[estado]:
                    if simbolo in transicoes[estado]:
                        transicoes[estado][simbolo] += a2.transicoes[estado][simbolo]
                    else:
                        transicoes[estado][simbolo] = a2.transicoes[estado][simbolo]
            else:
                transicoes[estado] = a2.transicoes[estado]

    return AFND(estados_iniciais, estados_finais, transicoes)
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
def fecho_kleene(a):
    estado_inicial = "s"
    estado_final = "f"

    estados_finais = a.estados_finais + [estado_final]

    transicoes = {}
    transicoes[estado_inicial] = {}
    transicoes[estado_inicial].update(a.estados_iniciais)
    transicoes[estado_inicial][None] = [estado_final]
    for estado in a.estados_finais:
        if estado in a.transicoes:
            transicoes[estado][None] = [estado_final]

    return AFND([estado_inicial], estados_finais, transicoes)
##############################################################################################################
def criar_afnd_simbolo(simbolo):
    estado_inicial = "s" + str(random.randint(0, 99))
    estado_final = "f" + str(random.randint(0, 99))
    conjunto_estados = [estado_inicial, estado_final]
    estados_finais = [estado_final]

    transicoes = {}
    transicoes[estado_inicial] = {}
    transicoes[estado_inicial][simbolo] = [estado_final]
    #print(transicoes)
    #print(f"({estado_inicial} --({transicoes[estado_inicial]})--> {estado_final})")
    return AFND([estado_inicial],conjunto_estados, estados_finais, transicoes)
##### printa AFDN ############################################################################################
def print_afdn(afnd):
    print("Estados Iniciais:", afnd.estados_iniciais)
    print("Estados Finais:", afnd.estados_finais)
    print("Conjunto de Estados:", afnd.conjunto_estados)
    print("Transições:")
    for estado, transicoes in afnd.transicoes.items():
        for simbolo, destinos in transicoes.items():
            print(f"({estado} --({simbolo})--> {destinos})")
    print("\n")
##############################################################################################################
def gerar_automato(arvore):
    if isinstance(arvore, Node):
        if arvore.value == "CONCATENACAO":
            afdn_esquerdo = gerar_automato(arvore.children[0])
            # print_afdn(afdn_esquerdo)
            afdn_direito = gerar_automato(arvore.children[1])
            # print_afdn(afdn_direito)
            return concatenacao(afdn_esquerdo,afdn_direito)
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


# Função auxiliar para imprimir a árvore sintática
def print_tree(node, level=0):
    if isinstance(node, Node):
        print("  " * level + node.value)
        for child in node.children:
            print_tree(child, level+1)
    else:
        print("  " * level + node)

# Teste o lexer e parser
expressao = "(0001001)"
lexer.input(expressao)
# for token in lexer:
#     print(token)

resultado = parser.parse(expressao)
# print_tree(resultado)
automato = gerar_automato(resultado)
print_afdn(automato)