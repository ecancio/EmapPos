from collections import defaultdict, Counter
import math

def pares_e_impares_v1(nums: list[int]) -> tuple[list[int], list[int]]:
    """Recebe uma lista de números e os separa em duas listas: pares e ímpares, um laço for e instruções condicionais. """

    """Parâmetros: nums (list[int]): Uma lista de números inteiros."""
    """Retorno: tuple[list[int], list[int]]: Uma tupla contendo duas listas:a primeira com os números pares e a segunda com os ímpares."""
    pares = []
    impares = []
    for num in nums:
        # Usa o operador de módulo (%) para verificar a paridade [13-15]
        if num % 2 == 0:
            pares.append(num)
        else:
            impares.append(num)
    return pares, impares
def pares_e_impares_v2(nums: list[int]) -> tuple[list[int], list[int]]:
    """
    Recebe uma lista de números e os separa em duas listas: pares e ímpares,
    utilizando list comprehensions para uma solução mais concisa.

    Parâmetros:
        nums (list[int]): Uma lista de números inteiros.

    Retorno:
        tuple[list[int], list[int]]: Uma tupla contendo duas listas:
                                      a primeira com os números pares e a segunda com os ímpares.
    """
    # List comprehensions são uma forma concisa de criar listas [5, 5.1.3, 258]
    pares = [num for num in nums if num % 2 == 0]
    impares = [num for num in nums if num % 2 != 0]
    return pares, impares

def transpose_v1(matrix: list[list[int]]) -> list[list[int]]:
    """
    Calcula a transposta de uma matriz (lista de listas) utilizando laços for aninhados.
    Não utiliza bibliotecas externas, conforme a restrição do problema [21].

    Parâmetros:
        matrix (list[list[int]]): A matriz original.

    Retorno:
        list[list[int]]: A matriz transposta.
    """
    if not matrix or not matrix:
        return [] # Retorna matriz vazia se a entrada for vazia ou inválida.

    rows = len(matrix)
    cols = len(matrix)

    # Inicializa a matriz transposta com as dimensões invertidas (cols x rows)
    transposed = []
    for _ in range(cols):
        transposed.append( * rows) # Preenche com zeros ou pode ser lista vazia e usar append

    # Preenche a matriz transposta [8, 9]
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    return transposed
def transpose_v2(matrix: list[list[int]]) -> list[list[int]]:

    """
    Calcula a transposta de uma matriz (lista de listas) utilizando list comprehensions aninhadas,
    para uma solução mais compacta. Não utiliza bibliotecas externas [21].

    Parâmetros:
        matrix (list[list[int]]): A matriz original.

    Retorno:
        list[list[int]]: A matriz transposta.
    """
    if not matrix or not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix)

    # A compreensão de lista externa itera pelas colunas da matriz original (j)
    # A compreensão de lista interna itera pelas linhas da matriz original (i)
    # e seleciona o elemento matrix[i][j] para a nova posição [j][i]
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

def rotate_tuple_v1(tpl: tuple, n: int) -> tuple:
    """
    Rotaciona os elementos de uma tupla n posições para a direita
    utilizando fatiamento e concatenação de tuplas. Lida com valores
    positivos e negativos de n, e com tuplas vazias.

    Parâmetros:
        tpl (tuple): A tupla original.
        n (int): O número de posições para rotacionar à direita.

    Retorno:
        tuple: A nova tupla com os elementos rotacionados.
    """
    if not tpl:
        return tpl
    
    num_elements = len(tpl)
    # Garante que n esteja dentro dos limites do comprimento da tupla e
    # lida com rotações negativas, transformando-as em equivalentes positivas para rotação à direita.
    # Ex: rotacionar 5 elementos -2 para a direita é o mesmo que +3 para a direita.
    effective_n = n % num_elements

    # Divide a tupla em duas partes e as concatena na ordem invertida para rotação à direita
    # tpl[-effective_n:] pega os últimos 'effective_n' elementos
    # tpl[:-effective_n] pega os primeiros 'num_elements - effective_n' elementos
    # A concatenação de tuplas usa o operador '+' [4, 30]
    return tpl[-effective_n:] + tpl[:-effective_n]
def rotate_tuple_v2(tpl: tuple, n: int) -> tuple:

    """
    Rotaciona os elementos de uma tupla n posições para a direita
    convertendo a tupla para uma lista (listas são mutáveis), manipulando a lista
    e depois convertendo-a de volta para uma tupla.

    Parâmetros:
        tpl (tuple): A tupla original.
        n (int): O número de posições para rotacionar à direita.

    Retorno:
        tuple: A nova tupla com os elementos rotacionados.
    """
    if not tpl:
        return tpl
    
    lst = list(tpl) # Converte a tupla para uma lista para manipulação [4, 5]
    num_elements = len(lst)
    effective_n = n % num_elements

    # Realiza a rotação manual da lista
    # Pega os últimos 'effective_n' elementos e os move para o início
    rotated_part = lst[num_elements - effective_n:]
    remaining_part = lst[:num_elements - effective_n]
    
    return tuple(rotated_part + remaining_part) # Converte a lista rotacionada de volta para tupla

def transpose_v1(matrix: list[list[int]]) -> list[list[int]]:

    """
    Calcula a transposta de uma matriz (lista de listas) utilizando laços for aninhados.
    Não utiliza bibliotecas externas, conforme a restrição do problema [21].

    Parâmetros:
        matrix (list[list[int]]): A matriz original.

    Retorno:
        list[list[int]]: A matriz transposta.
    """
    if not matrix or not matrix:
        return [] # Retorna matriz vazia se a entrada for vazia ou inválida.

    rows = len(matrix)
    cols = len(matrix)

    # Inicializa a matriz transposta com as dimensões invertidas (cols x rows)
    transposed = []
    for _ in range(cols):
        transposed.append( * rows) # Preenche com zeros ou pode ser lista vazia e usar append

    # Preenche a matriz transposta [8, 9]
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    return transposed
def transpose_v2(matrix: list[list[int]]) -> list[list[int]]:
    """
    Calcula a transposta de uma matriz (lista de listas) utilizando list comprehensions aninhadas,
    para uma solução mais compacta. Não utiliza bibliotecas externas [21].

    Parâmetros:
        matrix (list[list[int]]): A matriz original.

    Retorno:
        list[list[int]]: A matriz transposta.
    """
    if not matrix or not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix)

    # A compreensão de lista externa itera pelas colunas da matriz original (j)
    # A compreensão de lista interna itera pelas linhas da matriz original (i)
    # e seleciona o elemento matrix[i][j] para a nova posição [j][i]
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

def flatten_v1(lst: list) -> list:

    """
    Achata uma lista aninhada (listas dentro de listas em qualquer profundidade)
    em uma única lista, utilizando recursão.

    Parâmetros:
        lst (list): A lista potencialmente aninhada.

    Retorno:
        list: Uma nova lista "achatada" contendo todos os elementos.
    """
    result = []
    for item in lst:
        # Verifica se o item é uma lista [34]
        if isinstance(item, list):
            # Se for uma lista, chama a função recursivamente para achatar e
            # estende o resultado atual com os elementos achatados [35, 36]
            result.extend(flatten_v1(item))
        else:
            # Se não for uma lista, adiciona o item diretamente ao resultado
            result.append(item)
    return result
def flatten_v2(lst: list) -> list:
    """
    Achata uma lista aninhada em uma única lista utilizando uma abordagem iterativa
    com uma pilha (stack). Esta versão evita a profundidade máxima de recursão
    para listas muito aninhadas.

    Parâmetros:
        lst (list): A lista potencialmente aninhada.

    Retorno:
        list: Uma nova lista "achatada" contendo todos os elementos.
    """
    result = []
    # Inicializa a pilha com os elementos da lista original em ordem inversa.
    # Isso permite que, ao usar pop() (que remove do final), os elementos sejam processados na ordem original.
    stack = list(lst[::-1]) # Fatiamento [2, 37] para inverter a lista

    while stack: # O laço continua enquanto a pilha não estiver vazia [8, 9]
        current_item = stack.pop() # Remove o último item da pilha (o próximo a ser processado na ordem original)
        
        # Verifica se o item atual é uma lista [34]
        if isinstance(current_item, list):
            # Se for uma lista, seus elementos são adicionados de volta à pilha em ordem inversa
            # para que, quando removidos (pop()), eles mantenham a ordem original.
            stack.extend(current_item[::-1]) # [2, 37]
        else:
            # Se não for uma lista, é um elemento final, então o adiciona ao resultado
            result.append(current_item)
    return result

# 1. Agrupamento por Chave
def group_by_v1(pairs):
    """Agrupa valores de uma lista de tuplas em um dicionário."""
    result = {}
    for key, value in pairs:
        if key not in result:
            result[key] = []
        result[key].append(value)
    return result
def group_by_v2(pairs):
    """Agrupa valores usando collections.defaultdict."""
    result = defaultdict(list)
    for key, value in pairs:
        result[key].append(value)
    return dict(result)

# 2. Inversão de Mapeamento
def invert_map_v1(d):
    """Inverte um dicionário (chaves viram valores e vice-versa)."""
    inverted_dict = {}
    for key, value in d.items():
        inverted_dict[value] = key
    return inverted_dict
def invert_map_v2(d):
    """Inverte um dicionário usando compreensão de dicionário."""
    return {value: key for key, value in d.items()}

# 3. Índices por Valor
def indices_of_v1(lst):
    """Cria um dicionário com os índices de cada elemento de uma lista."""
    indices_map = {}
    for index, value in enumerate(lst):
        if value not in indices_map:
            indices_map[value] = []
        indices_map[value].append(index)
    return indices_map
def indices_of_v2(lst):
    """Cria um mapa de índices usando defaultdict."""
    indices_map = defaultdict(list)
    for index, value in enumerate(lst):
        indices_map[value].append(index)
    return dict(indices_map)

# 4. Fusão com Resolução de Conflitos
def merge_dicts_v1(dict_list):
    """Funde uma lista de dicionários, somando valores de chaves repetidas."""
    merged = {}
    for d in dict_list:
        for key, value in d.items():
            if key in merged:
                merged[key] += value
            else:
                merged[key] = value
    return merged
def merge_dicts_v2(dict_list):
    """Funde dicionários usando collections.Counter para somar valores."""
    merged = Counter()
    for d in dict_list:
        merged.update(d)
    return dict(merged)
# 5. Contador de Dígitos

def conta_digitos_v1(n):
    """Conta a ocorrência de cada dígito em um número inteiro."""
    # Garante que o número seja positivo para a conversão
    s_number = str(abs(n))
    counts = {str(i): 0 for i in range(10)}
    for digit_char in s_number:
        if digit_char in counts:
            counts[digit_char] += 1
    # Converte as chaves de string para inteiro
    return {int(k): v for k, v in counts.items()}
def conta_digitos_v2(n):
    """Conta dígitos usando collections.Counter e compreensão de dicionário."""
    counts = Counter(str(abs(n)))
    # Garante que todos os dígitos de 0 a 9 estejam presentes
    return {i: counts.get(str(i), 0) for i in range(10)}


def count_anagrams_v1(words):
    """Agrupa palavras em listas de anagramas usando um laço for."""
    anagram_map = {}
    for word in words:
        # A chave do anagrama é a palavra com as letras ordenadas
        sorted_key = "".join(sorted(word))
        
        if sorted_key not in anagram_map:
            anagram_map[sorted_key] = []
        
        anagram_map[sorted_key].append(word)
        
    return anagram_map

def count_anagrams_v2(words):
    """Agrupa palavras em listas de anagramas usando defaultdict."""
    anagram_map = defaultdict(list)
    for word in words:
        # A defaultdict cria a lista vazia automaticamente na primeira vez que a chave é acessada
        anagram_map["".join(sorted(word))].append(word)
    return dict(anagram_map) # Converte para um dicionário normal


# Exemplo de uso:
palavras = ["bolo", "bloo", "lobo", "gato", "toga", "mesa"]
print(f"V1: {count_anagrams_v1(palavras)}")
# Resultado esperado: {'bloo': ['bolo', 'bloo', 'lobo'], 'agot': ['gato', 'toga'], 'aems': ['mesa']}
print(f"V1: {count_anagrams_v2(palavras)}")
# Resultado esperado: {'bloo': ['bolo', 'bloo', 'lobo'], 'agot': ['gato', 'toga'], 'aems': ['mesa']}


def parse_csv_v1(text, sep=','):
    """Converte um texto CSV em uma lista de dicionários."""
    lines = text.strip().split('\n')
    
    # Remove e processa o cabeçalho
    header_line = lines.pop(0)
    headers = [h.strip() for h in header_line.split(sep)]
    
    result_list = []
    for line in lines:
        if not line:  # Ignora linhas vazias
            continue
            
        values = [v.strip() for v in line.split(sep)]
        
        row_dict = {}
        for i in range(len(headers)):
            row_dict[headers[i]] = values[i]
            
        result_list.append(row_dict)
        
    return result_list

def parse_csv_v2(text, sep=','):
    """Converte um texto CSV em uma lista de dicionários usando compreensões."""
    lines = text.strip().split('\n')
    headers = [h.strip() for h in lines[0].split(sep)]
    
    # Cria uma lista de dicionários combinando headers com valores de cada linha
    return [
        dict(zip(headers, [v.strip() for v in line.split(sep)]))
        for line in lines[1:] if line # Itera a partir da segunda linha e ignora vazias
    ]

# Exemplo de uso:
csv_text = """
Altura, Nome, Idade
177, Pedro, 21
191, Carlos, 33
169, Alice, 23
"""
print(f"V1: {parse_csv_v1(csv_text)}")

# Exemplo de uso:
csv_text = """
Altura, Nome, Idade
177, Pedro, 21
191, Carlos, 33
169, Alice, 23
"""
print(f"V2: {parse_csv_v2(csv_text)}")


def _sem_duplicatas(grupo):
    """Função auxiliar que verifica se uma lista (linha, coluna ou bloco) tem duplicatas."""
    # Filtra os zeros e verifica se o número de itens únicos é igual ao número total de itens
    numeros = [n for n in grupo if n != 0]
    return len(set(numeros)) == len(numeros)

def validar_sudoku_v1(tabuleiro):
    """Valida um tabuleiro de Sudoku usando laços for explícitos."""
    # 1. Validar Linhas
    for r in range(9):
        if not _sem_duplicatas(tabuleiro[r]):
            return False
            
    # 2. Validar Colunas
    for c in range(9):
        coluna = []
        for r in range(9):
            coluna.append(tabuleiro[r][c])
        if not _sem_duplicatas(coluna):
            return False
            
    # 3. Validar Blocos 3x3
    for i in range(0, 9, 3):  # Itera pelas linhas iniciais dos blocos (0, 3, 6)
        for j in range(0, 9, 3):  # Itera pelas colunas iniciais dos blocos (0, 3, 6)
            bloco = []
            for r in range(i, i + 3):
                for c in range(j, j + 3):
                    bloco.append(tabuleiro[r][c])
            if not _sem_duplicatas(bloco):
                return False
                
    # Se todas as validações passaram
    return True

def validar_sudoku_v2(tabuleiro):
    """Valida um tabuleiro de Sudoku usando uma abordagem funcional com 'all'."""
    # 1. Validar Linhas
    valida_linhas = all(_sem_duplicatas(linha) for linha in tabuleiro)
    if not valida_linhas:
        return False
        
    # 2. Validar Colunas (zip(*matriz) é a forma pythônica de transpor uma matriz)
    valida_colunas = all(_sem_duplicatas(coluna) for coluna in zip(*tabuleiro))
    if not valida_colunas:
        return False
        
    # 3. Validar Blocos 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            # Cria o bloco usando compreensão de lista
            bloco = [tabuleiro[r][c] for r in range(i, i + 3) for c in range(j, j + 3)]
            if not _sem_duplicatas(bloco):
                return False
    
    return True
