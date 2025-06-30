import numpy as np

def replace_negatives(v: np.ndarray, new_value: float) -> np.ndarray:
    """
    Substitui todas as entradas negativas em um vetor por um novo valor.
    Não utiliza np.where; faz indexação booleana.

    Parâmetros:
    - v: Vetor de entrada (np.ndarray).
    - new_value: Valor escalar que substituirá cada elemento negativo.

    Retorno:
    - Novo vetor onde todas as entradas negativas de v foram trocadas por new_value.
    """
    if not isinstance(v, np.ndarray):
        raise TypeError("A entrada 'v' deve ser um np.ndarray.")
    if v.ndim != 1:
        raise ValueError("A entrada 'v' deve ser um vetor (1-dimensional).")
    if not isinstance(new_value, (int, float)):
        raise TypeError("O 'new_value' deve ser um escalar (int ou float).")

    # Cria uma cópia do vetor para evitar modificar o original
    v_copy = v.copy()

    # Usa indexação booleana para encontrar e substituir valores negativos
    negative_indices = v_copy < 0
    v_copy[negative_indices] = new_value

    return v_copy

def local_peaks(series: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Identifica todos os máximos locais em uma série temporal unidimensional.
    Um máximo local x_t é um ponto tal que x_{t-1} < x_t > x_{t+1}, para 2 <= t <= N-1.

    Parâmetros:
    - series: Vetor de entrada (np.ndarray) representando a série temporal.

    Retorno:
    - Tupla contendo:
        - indices: np.ndarray de inteiros com as posições t onde há máximos locais.
        - peaks: np.ndarray de floats com os valores x_t correspondentes.
    """
    if not isinstance(series, np.ndarray):
        raise TypeError("A entrada 'series' deve ser um np.ndarray.")
    if series.ndim != 1:
        raise ValueError("A entrada 'series' deve ser um vetor (1-dimensional).")
    if len(series) < 3:
        # Mínimo de 3 pontos (x_{t-1}, x_t, x_{t+1}) para identificar um pico
        return np.array([]), np.array([])

    n = len(series)
    peak_indices = []
    peak_values = []

    # Percorre a série de t=1 a t=n-2 (correspondendo a x_t de índice 1 a n-2)
    # A condição 2 <= t <= N-1 na descrição refere-se ao índice matemático/posição.
    # Em termos de índice Python (0-based), isso é de t=1 a t=n-2.
    # Ou seja, x_{t-1} é series[i-1], x_t é series[i], x_{t+1} é series[i+1]
    for i in range(1, n - 1):
        if series[i] > series[i-1] and series[i] > series[i+1]:
            peak_indices.append(i)
            peak_values.append(series[i])

    return np.array(peak_indices, dtype=int), np.array(peak_values, dtype=float)