import numpy as np

def rotate_90(A: np.ndarray) -> np.ndarray:
    """
    Implementa a rotação de 90° no sentido horário para uma matriz quadrada A.
    Não utiliza np.rot90.

    O procedimento segue dois passos:
    1. Transpor A (trocar linhas por colunas), obtendo B = A^T.
    2. Inverter a ordem das colunas de B (cada linha de B deve ser lida de trás para frente)
       para formar A_rot.

    Parâmetros:
    - A: Matriz quadrada de formato (n, n).

    Retorno:
    - Matriz rotacionada A_rot de dimensão (n, n).
    """
    if not isinstance(A, np.ndarray):
        raise TypeError("A entrada 'A' deve ser um np.ndarray.")
    if A.ndim != 2:
        raise ValueError("A entrada 'A' deve ser uma matriz 2-dimensional.")
    if A.shape[0] != A.shape[1]:
        raise ValueError("A entrada 'A' deve ser uma matriz quadrada (n, n).")

    # Passo 1: Transpor A para obter B = A^T
    B = A.T

    # Passo 2: Inverter a ordem das colunas de B
    # Isso pode ser feito usando fatiamento com passo -1 para as colunas: [:, ::-1]
    A_rot = B[:, ::-1]

    return A_rot


def sum_subdiagonals(A: np.ndarray, k: int) -> float:
    """
    Calcula a soma dos elementos na k-ésima subdiagonal abaixo da diagonal principal.

    A soma é definida como: sum_{i=k}^{n-1} A_{i, i-k}.

    Não utiliza np.diag(A, -k); implementa a indexação manual.

    Parâmetros:
    - A: Matriz quadrada de dimensão (n, n).
    - k: Inteiro, 1 <= k < n.

    Retorno:
    - Valor escalar (float) com a soma dos elementos da subdiagonal.
    """
    if not isinstance(A, np.ndarray):
        raise TypeError("A entrada 'A' deve ser um np.ndarray.")
    if A.ndim != 2:
        raise ValueError("A entrada 'A' deve ser uma matriz 2-dimensional.")
    if A.shape[0] != A.shape[1]:
        raise ValueError("A entrada 'A' deve ser uma matriz quadrada (n, n).")

    n = A.shape[0]
    if not isinstance(k, int):
        raise TypeError("O parâmetro 'k' deve ser um inteiro.")
    if not (1 <= k < n):
        raise ValueError(f"O parâmetro 'k' deve satisfazer 1 <= k < n (onde n={n}).")

    subdiagonal_sum = 0.0
    # A fórmula indica sum_{i=k}^{n-1} A_{i, i-k}
    # Onde i representa a linha e i-k representa a coluna.
    # Para a k-ésima subdiagonal, a coluna é sempre k unidades menor que a linha.
    # As linhas válidas para a subdiagonal iniciam em k e vão até n-1.
    for i in range(k, n):
        subdiagonal_sum += A[i, i - k]

    return float(subdiagonal_sum)

def block_matmul(A: np.ndarray, B: np.ndarray, block_size: int) -> np.ndarray:    
    """
    Implementa a multiplicação de duas matrizes A e B, ambas de formato
    compatível para produto, dividindo-as em subblocos de block_size.
    Para cada par de blocos, compute o produto parcimonioso e acumule resultados.

    A ideia é percorrer A e B por blocos, multiplicar blocos correspondentes
    e somar ao bloco de C. Não utilize np.dot ou A @ B diretamente para
    todo o produto, mas apenas para cada subbloco individual.

    Parâmetros:
    - A: Matriz A de dimensão (m, p).
    - B: Matriz B de dimensão (p, n).
    - block_size: Inteiro > 0 indicando o tamanho de cada subbloco quadrado.

    Retorno:
    - Matriz C de dimensão (m, n) resultante do produto em blocos.
    """
    if not isinstance(A, np.ndarray) or not isinstance(B, np.ndarray):
        raise TypeError("As entradas 'A' e 'B' devem ser np.ndarray.")
    if A.ndim != 2 or B.ndim != 2:
        raise ValueError("As entradas 'A' e 'B' devem ser matrizes 2-dimensionais.")
    if A.shape[1] != B.shape[0]:
        raise ValueError("As dimensões das matrizes são incompatíveis para multiplicação: "
                         "A.shape[1] deve ser igual a B.shape[0].")
    if not isinstance(block_size, int) or block_size <= 0:
        raise ValueError("O 'block_size' deve ser um inteiro positivo.")

    m, p = A.shape
    p, n = B.shape[0], B.shape[1] # p já é A.shape[1]

    # Inicializa a matriz C com zeros
    C = np.zeros((m, n))

    # Percorre as linhas de A em blocos (i_0)
    for i_0 in range(0, m, block_size):
        # Percorre as colunas de B em blocos (j_0)
        for j_0 in range(0, n, block_size):
            # Percorre a dimensão interna (p) em blocos (k_0)
            for k_0 in range(0, p, block_size):
                # Define os limites do bloco para A, B e C
                # Bloco de A: A[i_0 : i_0 + block_size, k_0 : k_0 + block_size]
                # Bloco de B: B[k_0 : k_0 + block_size, j_0 : j_0 + block_size]

                # Fatiamento para obter os sub-blocos
                A_block = A[i_0 : min(i_0 + block_size, m), k_0 : min(k_0 + block_size, p)]
                B_block = B[k_0 : min(k_0 + block_size, p), j_0 : min(j_0 + block_size, n)]

                # Multiplica os sub-blocos e acumula em C.
                # Aqui é permitido usar np.dot ou @ para a multiplicação dos sub-blocos.
                C[i_0 : min(i_0 + block_size, m), j_0 : min(j_0 + block_size, n)] += A_block @ B_block

    return C