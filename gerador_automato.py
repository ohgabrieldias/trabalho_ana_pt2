import os
import random
import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import filedialog

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
##############################################################################################################
def concatenacao2(a1, a2):
    estados_iniciais = a1.estados_iniciais  # Estado inicial de a1 como novo estado
    estados_finais = a2.estados_finais  # Estado final de a2 como novo estado
    conjunto_estados = a1.conjunto_estados + a2.conjunto_estados    #adiciona os estados de a1 e a2 no conjunto de estados
    print_afdn(a1)

    transicoes = {} #cria um dicionario para as transicoes
    for estado, transicoes_estado in a1.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()   #Copia as transições de a1 para o novo autômato
    for estado, transicoes_estado in a2.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()   #Copia as transições de a2 para o novo autômato

    if(len(a1.estados_finais) > 1): #se o estado final de a1 for maior que 1 significa que a1 é uma união de estados
        print("len(a1.estados_finais) > 1")
        for estado in a1.estados_finais:   #percorre os estados finais de a1
            transicoes[estado] = {} #cria um dicionario para as transições que antes nao existia
            transicoes[estado]["ε"] = a2.estados_iniciais[0] #adiciona a transição vazia para o estado inicial de a2 à lista de transições

    elif(a2.estados_iniciais[0] == a2.estados_finais[0]): #se o estado inicial de a2 for igual ao estado final de a2 significa que *(Kleene) foi usado
        print("a2.estados_iniciais[0] == a2.estados_finais[0]")
        transicoes[a1.estados_finais[0]] = {}   #sobreescreve o estado final de a1
        transicoes[a1.estados_finais[0]]["ε"] = a2.estados_iniciais[0]

    elif(a1.estados_finais[0] == 's0'): #se o estado final de a1 for = s0 significa que a1 tem fecho de kleene
        print("a1.estados_finais[0] == 's0'")
        transicoes[a1.estados_finais[0]]["ε"] = [transicoes[a1.estados_finais[0]]["ε"]]
        transicoes[a1.estados_finais[0]]["ε"].append(a2.estados_iniciais[0]) #Adiciona nova transição vai para o estado inicial de a2
    else:
        transicoes[a1.estados_finais[0]] = {}   #sobreescreve o estado final de a1
        transicoes[a1.estados_finais[0]]["ε"] = a2.estados_iniciais[0]
    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)
##############################################################################################################
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
##############################################################################################################
def fecho_kleene(a):
    novo_estado = "s0"
    estados_iniciais = [novo_estado]
    conjunto_estados = [novo_estado] + a.conjunto_estados
    
    transicoes = {}
    transicoes[novo_estado] = {}
    transicoes[novo_estado]["ε"] = a.estados_iniciais[0]
    transicoes[a.estados_finais[0]] = {}
    transicoes[a.estados_finais[0]]["ε"] = novo_estado

    estados_finais = [novo_estado]

    # Copia as transições de a para o novo autômato
    for estado, transicoes_estado in a.transicoes.items():
        transicoes[estado] = transicoes_estado.copy()

    return AFND(estados_iniciais, conjunto_estados, estados_finais, transicoes)

##############################################################################################################
conjunto_estados_utilizados = set()

def criar_afnd_simbolo(simbolo):
    global conjunto_estados_utilizados

    while True:
        estado_inicial = "s" + str(random.randint(1, 99))
        estado_final = "f" + str(random.randint(0, 99))
        conjunto_estados = [estado_inicial, estado_final]
        estados_finais = [estado_final]

        if estado_inicial not in conjunto_estados_utilizados and estado_final not in conjunto_estados_utilizados:
            break

    conjunto_estados_utilizados.add(estado_inicial)
    conjunto_estados_utilizados.add(estado_final)

    transicoes = {}
    transicoes[estado_inicial] = {}
    transicoes[estado_inicial][simbolo] = [estado_final]
    return AFND([estado_inicial], conjunto_estados, estados_finais, transicoes)
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
            return concatenacao2(afdn_esquerdo,afdn_direito)
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
def salvar_afdn_para_arquivo(afnd, filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("M = (K, Σ, δ, s, F)\n")
        file.write("M = (K" + str(afnd.conjunto_estados) + ", Σ[0,1], δ, s" + str(afnd.estados_iniciais) + ", F" + str(afnd.estados_finais) + ")\n")
        file.write("Transições (δ):\n")
        for estado, transicoes in afnd.transicoes.items():
            for simbolo, destinos in transicoes.items():
                file.write(f"δ:({estado} --({simbolo})--> {destinos})\n")
        file.write("\n")
        file.write("Conjunto de estados Iniciais(s): " + str(afnd.estados_iniciais) + "\n")
        file.write("Conjunto de estados Finais (F): " + str(afnd.estados_finais) + "\n")
        file.write("Conjunto de estados (K): " + str(afnd.conjunto_estados) + "\n")
##############################################################################################################
def ler_expressao_do_arquivo():
    root = tk.Tk()
    root.withdraw()

    caminho_arquivo = filedialog.askopenfilename(title="Selecionar arquivo", filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")])
    
    if not caminho_arquivo:
        print("Nenhum arquivo selecionado. Saindo...")
        return None, None

    try:
        with open(caminho_arquivo, 'r') as arquivo:
            expressao = arquivo.read()
            nome_arquivo = os.path.basename(caminho_arquivo)  # Extrai o nome do arquivo do caminho completo
            nome_saida_arquivo = "automato_" + nome_arquivo  # Forma o nome do arquivo de saída
            return expressao.strip(), nome_saida_arquivo
    except FileNotFoundError:
        print("Arquivo não encontrado. Certifique-se de que o caminho do arquivo está correto.")
        return None, None
##############################################################################################################
# Função auxiliar para imprimir a árvore sintática
def print_tree(node, level=0):
    if isinstance(node, Node):
        print("  " * level + node.value)
        for child in node.children:
            print_tree(child, level+1)
    else:
        print("  " * level + node)

def main():
    expressao, nome_saida_arquivo = ler_expressao_do_arquivo()
    if expressao:
        lexer.input(expressao)
        resultado = parser.parse(expressao)
        automato = gerar_automato(resultado)
        print_afdn(automato)
        if nome_saida_arquivo:
            # Remove a extensão .txt do nome_saida_arquivo antes de salvar
            nome_saida_arquivo = os.path.splitext(nome_saida_arquivo)[0]
            salvar_afdn_para_arquivo(automato, nome_saida_arquivo)

if __name__ == "__main__":
    main()