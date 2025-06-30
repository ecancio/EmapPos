import threading
import time
import random
from typing import Dict, List, Any, Tuple, Optional
import numpy as np

# O dicionário para armazenar os resultados das médias móveis de cada ação.
# Ele será inicializado dentro da função principal 'calcular_medias_moveis'
# e as threads irão preenchê-lo.
# Como cada thread escreve em uma chave única, um lock explícito para a escrita
# no dicionário não é estritamente necessário para garantir correção em Python,
# pois as operações de atribuição de dicionário para uma única chave são atômicas.
# No entanto, em cenários mais complexos ou para clareza em concorrência, um lock
# ou outro mecanismo de sincronização seria considerado.
# Para este problema, a simplicidade de atribuição direta é suficiente.
_results_container: Dict[str, np.ndarray] = {}

def _calculate_single_ma_task(stock_name: str, prices_array: np.ndarray, janela: int) -> None:
    """
    Função alvo para cada thread: calcula a média móvel simples (SMA) para uma
    única série de preços e armazena o resultado no container global.

    Utiliza `np.convolve` para uma implementação eficiente da média móvel.

    :param stock_name: O nome da ação (chave para o resultado).
    :type stock_name: str
    :param prices_array: O array NumPy de preços para a ação.
    :type prices_array: np.ndarray
    :param janela: O tamanho da janela para o cálculo da média móvel.
    :type janela: int
    """
    if len(prices_array) < janela:
        print(f"Aviso: Preços de '{stock_name}' ({len(prices_array)} pontos) são menores que a janela ({janela}). Definindo média móvel como vazia.")
        _results_container[stock_name] = np.array([])
        return

    # A média móvel simples é equivalente a uma convolução com um kernel de 1/janela
    # e np.ones(janela)
    # 'valid' mode significa que apenas os pontos onde a janela se sobrepõe completamente
    # aos dados de entrada são calculados, resultando em um array de tamanho N - janela + 1.
    moving_averages = np.convolve(prices_array, np.ones(janela)/janela, mode='valid')
    
    _results_container[stock_name] = moving_averages
    print(f"Thread para '{stock_name}' completou o cálculo da média móvel. Tamanho do resultado: {len(moving_averages)}")


def calcular_medias_moveis(acoes: Dict[str, np.ndarray], janela: int) -> Dict[str, np.ndarray]:
    """
    Calcula as médias móveis de preços de múltiplas ações em paralelo.

    Para cada ação no dicionário `acoes`, uma thread separada é criada para
    calcular sua média móvel de `janela` dias. Os resultados são coletados
    em um dicionário e retornados.

    :param acoes: Dicionário onde as chaves são nomes de ações (str) e os valores
                  são arrays NumPy de preços (np.ndarray).
                  Deve conter pelo menos uma ação e arrays válidos.
    :type acoes: Dict[str, np.ndarray]
    :param janela: Tamanho da janela para a média móvel. Deve ser um inteiro positivo.
    :type janela: int
    :raises TypeError: Se `acoes` não for um dicionário, ou `janela` não for um inteiro.
    :raises ValueError: Se `acoes` estiver vazio, `janela` não for positivo,
                        ou qualquer array de preços não for 1-dimensional ou contiver
                        dados insuficientes para a janela.
    :return: Um dicionário com as médias móveis calculadas para cada ação.
    :rtype: Dict[str, np.ndarray]

    :Example:
    >>> # Exemplo de uso:
    >>> # prices_data = {
    >>> #    "AAPL": np.array([100, 101, 102, 103, 104, 105, 106]),
    >>> #    "GOOG": np.array([200, 202, 201, 205, 203, 207, 206])
    >>> # }
    >>> # window_size = 3
    >>> # mas = calcular_medias_moveis(prices_data, window_size)
    >>> # print("\\nMédias Móveis Calculadas:")
    >>> # for stock, ma_array in mas.items():
    >>> #    print(f"{stock}: {ma_array}")
    """
    global _results_container # Referencia a variável global para que as threads possam atualizá-la

    # --- Validações de Parâmetros ---
    if not isinstance(acoes, dict):
        raise TypeError("O parâmetro 'acoes' deve ser um dicionário.")
    if not acoes:
        raise ValueError("O dicionário 'acoes' não pode estar vazio.")
    for stock_name, prices_array in acoes.items():
        if not isinstance(stock_name, str):
            raise TypeError("As chaves do dicionário 'acoes' devem ser strings (nomes das ações).")
        if not isinstance(prices_array, np.ndarray):
            raise TypeError(f"O valor para a ação '{stock_name}' deve ser um np.ndarray.")
        if prices_array.ndim != 1:
            raise ValueError(f"O array de preços para '{stock_name}' deve ser 1-dimensional.")
        if np.any(prices_array < 0):
             raise ValueError(f"O array de preços para '{stock_name}' contém valores negativos, o que não é esperado para preços.")
            
    if not isinstance(janela, int) or janela <= 0:
        raise ValueError("O parâmetro 'janela' deve ser um inteiro positivo.")

    # Limpa o container de resultados de execuções anteriores
    _results_container = {} 

    threads: List[threading.Thread] = []

    # Cria e inicia uma thread para cada ação
    for stock_name, prices_array in acoes.items():
        thread = threading.Thread(target=_calculate_single_ma_task, args=(stock_name, prices_array, janela))
        threads.append(thread)
        thread.start()

    print(f"\nIniciando cálculo paralelo de médias móveis para {len(acoes)} ações...")

    # Espera que todas as threads terminem sua execução
    for thread in threads:
        thread.join()

    print("\nCálculo de médias móveis concluído para todas as ações.")

    return _results_container

def _calculate_volatility_segment(
    retornos: np.ndarray,
    janela: int,
    start_output_idx: int,
    end_output_idx: int,
    result_array: np.ndarray,
    thread_id: int
) -> None:
    """
    Função alvo para cada thread: calcula o desvio padrão móvel para um
    segmento específico do array de saída `result_array`.

    Cada thread é responsável por calcular a volatilidade para um intervalo
    disjunto de índices na matriz de resultado final.

    :param retornos: O array NumPy completo de retornos diários.
    :type retornos: np.ndarray
    :param janela: O tamanho da janela para o cálculo da volatilidade.
    :type janela: int
    :param start_output_idx: O índice inicial no `result_array` que esta thread deve preencher.
    :type start_output_idx: int
    :param end_output_idx: O índice final (exclusivo) no `result_array` que esta thread deve preencher.
    :type end_output_idx: int
    :param result_array: O array NumPy pré-alocado onde os resultados calculados serão armazenados.
                         Este array é compartilhado entre as threads, mas cada thread escreve em
                         sua própria parte, evitando condições de corrida de escrita.
    :type result_array: np.ndarray
    :param thread_id: Um ID para identificar a thread nos logs.
    :type thread_id: int
    """
    # print(f"Thread {thread_id}: Processando índices de {start_output_idx} a {end_output_idx-1} do resultado.")
    for i in range(start_output_idx, end_output_idx):
        # O slice de dados para o cálculo do desvio padrão
        # Para o resultado no índice 'i', a janela de dados vai de 'i' até 'i + janela - 1'
        data_window = retornos[i : i + janela]
        
        # Calcula o desvio padrão da janela. ddof=1 para desvio padrão amostral.
        volatility = np.std(data_window, ddof=1) 
        
        result_array[i] = volatility
        # Pequeno atraso para simular o trabalho real e observar a concorrência
        # time.sleep(random.uniform(0.001, 0.005)) 
    # print(f"Thread {thread_id}: Concluída.")


def calcular_volatilidade(retornos: np.ndarray, janela: int, num_threads: int) -> np.ndarray:
    """
    Calcula a volatilidade (desvio padrão) sobre janelas móveis de `janela` dias
    para um array de retornos, utilizando processamento paralelo com `num_threads` threads.

    O array de `retornos` é dividido em `num_threads` partes, e uma thread é
    usada para calcular a volatilidade para cada parte dos resultados.
    Os resultados parciais são combinados em um único array NumPy.

    :param retornos: Array NumPy de retornos diários.
                     Deve ser 1-dimensional e ter pelo menos `janela` elementos.
    :type retornos: np.ndarray
    :param janela: Tamanho da janela para o cálculo da volatilidade.
                   Deve ser um inteiro positivo e menor ou igual ao comprimento de `retornos`.
    :type janela: int
    :param num_threads: Número de threads a serem usadas.
                        Deve ser um inteiro positivo.
    :type num_threads: int
    :raises TypeError: Se `retornos` não for um np.ndarray, ou `janela`/`num_threads` não forem inteiros.
    :raises ValueError: Se `retornos` não for 1-dimensional, `janela` ou `num_threads` não forem positivos,
                        ou o comprimento de `retornos` for insuficiente para a `janela`.
    :return: Um array NumPy com as volatilidades calculadas para cada janela.
    :rtype: np.ndarray
    
    :Example:
    >>> # Exemplo de uso:
    >>> # daily_returns = np.array([0.01, 0.02, -0.01, 0.03, 0.005, -0.02, 0.015, 0.00, 0.008, -0.005])
    >>> # window_size = 3
    >>> # num_processors = 2
    >>> # volatilities = calcular_volatilidade(daily_returns, window_size, num_processors)
    >>> # print("\\nVolatilidades Calculadas:", volatilities)
    """
    # --- Validações de Parâmetros ---
    if not isinstance(retornos, np.ndarray):
        raise TypeError("O parâmetro 'retornos' deve ser um np.ndarray.")
    if retornos.ndim != 1:
        raise ValueError("O array 'retornos' deve ser 1-dimensional.")
    if not isinstance(janela, int) or janela <= 0:
        raise ValueError("O parâmetro 'janela' deve ser um inteiro positivo.")
    if not isinstance(num_threads, int) or num_threads <= 0:
        raise ValueError("O parâmetro 'num_threads' deve ser um inteiro positivo.")    

    # Calcula o número total de elementos no array de saída
    num_output_elements = len(retornos) - janela + 1
    
    # Se não houver elementos de saída válidos, retorna um array vazio
    if num_output_elements <= 0:
        return np.array([])

    # Array pré-alocado para armazenar os resultados
    final_volatilities = np.zeros(num_output_elements, dtype=float)
    
    threads: List[threading.Thread] = []

    # Divide o trabalho (os índices do array de saída) entre as threads
    # Calcula o tamanho de cada "chunk" de saída que uma thread será responsável
    chunk_size = (num_output_elements + num_threads - 1) // num_threads

    print(f"\nIniciando cálculo de volatilidade paralelo para {num_output_elements} elementos com {num_threads} threads.")

    for i in range(num_threads):
        start_output_idx = i * chunk_size
        end_output_idx = min((i + 1) * chunk_size, num_output_elements) # Garante que não exceda o limite

        # Se o segmento estiver vazio, a thread não precisa ser criada
        if start_output_idx >= end_output_idx:
            continue

        thread = threading.Thread(
            target=_calculate_volatility_segment,
            args=(retornos, janela, start_output_idx, end_output_idx, final_volatilities, i + 1)
        )
        threads.append(thread)
        thread.start()

    # Espera que todas as threads terminem
    for thread in threads:
        thread.join()

    print("\nCálculo de volatilidade concluído por todas as threads.")

    return final_volatilities