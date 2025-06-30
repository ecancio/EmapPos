import numpy as np


def simular_precos(S0: float, sigma: float, days: int) -> np.ndarray:
    """
    Simula uma série temporal de preços de ações de forma simplificada com ruído Gaussiano.

    A função retorna um np.ndarray de tamanho days + 1, onde o primeiro
    elemento é S0 e, a cada passo, soma-se um ruído normal de desvio padrão sigma.

    Parâmetros:
    - S0: preço inicial positivo.
    - sigma: desvio padrão do ruído (volatilidade).
    - days: número de dias a simular.

    Retorno: np.ndarray com preços simulados.
    """
    if S0 <= 0:
        raise ValueError("S0 (preço inicial) deve ser um valor positivo.")
    if sigma < 0:
        raise ValueError("sigma (desvio padrão do ruído) não pode ser negativo.")
    if days < 0:
        raise ValueError("days (número de dias a simular) não pode ser negativo.")

    prices = np.zeros(days + 1)
    prices[0] = S0

    for i in range(1, days + 1):
        # Gerar ruído Gaussiano com média 0 e desvio padrão sigma
        epsilon_t = np.random.normal(0, sigma)
        prices[i] = prices[i-1] + epsilon_t

    return prices

def calc_retornos_simples(prices: np.ndarray) -> np.ndarray:
    """
    Calcula os retornos simples diários dado um vetor de preços.

    Os retornos simples são calculados como (P_t - P_{t-1}) / P_{t-1}.

    Parâmetros:
    - prices: Um np.ndarray contendo os preços (P_0, P_1, ..., P_n).

    Retorno:
    - np.ndarray de dimensão n com os retornos simples.
    """
    if not isinstance(prices, np.ndarray):
        raise TypeError("A entrada 'prices' deve ser um np.ndarray.")
    if prices.ndim != 1:
        raise ValueError("A entrada 'prices' deve ser um vetor (1-dimensional).")
    if len(prices) < 2:
        raise ValueError("São necessários pelo menos 2 preços para calcular retornos.")
    if np.any(prices <= 0):
        raise ValueError("Todos os preços devem ser positivos para calcular retornos simples.")

    # Retornos simples: (P_t - P_{t-1}) / P_{t-1}
    # equivalentemente P_t / P_{t-1} - 1
    # Usamos fatiamento para vetorizar o cálculo.
    returns = (prices[1:] / prices[:-1]) - 1
    return returns

def calc_retornos_log(prices: np.ndarray) -> np.ndarray:
    """
    Calcula os log-retornos diários dado um vetor de preços.

    Os log-retornos são calculados como ln(P_t / P_{t-1}).

    Parâmetros:
    - prices: Um np.ndarray contendo os preços (P_0, P_1, ..., P_n).

    Retorno:
    - np.ndarray de dimensão n com os log-retornos.
    """
    if not isinstance(prices, np.ndarray):
        raise TypeError("A entrada 'prices' deve ser um np.ndarray.")
    if prices.ndim != 1:
        raise ValueError("A entrada 'prices' deve ser um vetor (1-dimensional).")
    if len(prices) < 2:
        raise ValueError("São necessários pelo menos 2 preços para calcular log-retornos.")
    if np.any(prices <= 0):
        raise ValueError("Todos os preços devem ser positivos para calcular log-retornos.")

    # Log-retornos: ln(P_t / P_{t-1})
    # Usamos fatiamento para vetorizar o cálculo.
    returns_log = np.log(prices[1:] / prices[:-1])
    return returns_log
    try:
        calc_retornos_simples([1, 2, 3]) # Lista em vez de numpy array
    except TypeError as e:
        print(f"Erro esperado para entrada não np.ndarray: {e}")

    try:
        calc_retornos_log(np.array([[10, 20], [30, 40]])) # Array 2D
    except ValueError as e:
        print(f"Erro esperado para array não 1-dimensional: {e}")


def sma(returns: np.ndarray, window: int) -> np.ndarray:
    """
    Calcula a Média Móvel Simples (SMA) para um vetor de retornos.

    Para cada índice t a partir de t = window, a SMA é calculada como:
    SMA_t = (1 / window) * sum(r_i) para i de t-window+1 até t.

    Parâmetros:
    - returns: Um np.ndarray contendo o vetor de retornos [r_1, ..., r_n].
    - window: O tamanho da janela da média móvel.

    Retorno:
    - np.ndarray de tamanho n - window + 1 com as médias móveis simples.
    """
    if not isinstance(returns, np.ndarray):
        raise TypeError("A entrada 'returns' deve ser um np.ndarray.")
    if returns.ndim != 1:
        raise ValueError("A entrada 'returns' deve ser um vetor (1-dimensional).")
    if not isinstance(window, int) or window <= 0:
        raise ValueError("A 'window' deve ser um inteiro positivo.")
    if len(returns) < window:
        raise ValueError("O tamanho do vetor de retornos deve ser maior ou igual à 'window'.")

    n = len(returns)
    sma_values = np.zeros(n - window + 1)

    for i in range(window - 1, n):
        sma_values[i - (window - 1)] = np.mean(returns[i - window + 1 : i + 1])
        # Alternativamente, para um cálculo mais eficiente em numpy para grandes arrays:
        # sma_values = np.convolve(returns, np.ones(window)/window, mode='valid')
        # No entanto, a descrição da função SMA_t indica a soma até t, o que o loop faz.
        # np.convolve com 'valid' também faz isso, retornando um array de n - window + 1 elementos.
        # Poderíamos usar:
        # return np.convolve(returns, np.ones(window) / window, 'valid')
        # mas o loop explícito segue a fórmula mais de perto.

    return sma_values

def rolling_std(returns: np.ndarray, window: int, days_size: int = 0) -> np.ndarray:
    """
    Calcula o desvio padrão móvel para um vetor de retornos.

    Para cada t >= window, calcula o desvio padrão da janela.
    A normalização é 1 / (window - days_size).

    Parâmetros:
    - returns: Um np.ndarray contendo o vetor de retornos [r_1, ..., r_n].
    - window: O tamanho da janela para o cálculo do desvio padrão.
    - days_size: Parâmetro opcional para ajustar a normalização.
                 Por padrão é 0, resultando na normalização padrão (ddof=0).
                 Se days_size=1, a normalização é (N-1), que é o comportamento padrão de np.std(ddof=1).

    Retorno:
    - np.ndarray de tamanho n - window + 1 com os desvios padrão móveis.
    """
    if not isinstance(returns, np.ndarray):
        raise TypeError("A entrada 'returns' deve ser um np.ndarray.")
    if returns.ndim != 1:
        raise ValueError("A entrada 'returns' deve ser um vetor (1-dimensional).")
    if not isinstance(window, int) or window <= 0:
        raise ValueError("A 'window' deve ser um inteiro positivo.")
    if not isinstance(days_size, int) or days_size < 0 or days_size >= window:
        raise ValueError("O 'days_size' deve ser um inteiro não negativo e menor que a 'window'.")
    if len(returns) < window:
        raise ValueError("O tamanho do vetor de retornos deve ser maior ou igual à 'window'.")

    n = len(returns)
    rolling_std_values = np.zeros(n - window + 1)

    # O parâmetro ddof (delta degrees of freedom) em numpy.std controla a normalização.
    # ddof = 0 (padrão) normaliza por N (window).
    # ddof = 1 normaliza por N-1.
    # A fórmula indica normalização por (window - days_size).
    # Então, ddof = days_size.
    ddof_param = days_size

    for i in range(window - 1, n):
        rolling_std_values[i - (window - 1)] = np.std(returns[i - window + 1 : i + 1], ddof=ddof_param)

    return rolling_std_values