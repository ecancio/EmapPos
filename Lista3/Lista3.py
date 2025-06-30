from Simulations import simular_precos, calc_retornos_simples, calc_retornos_log, sma, rolling_std  
from Operations import rotate_90, sum_subdiagonals, block_matmul
from Filters import replace_negatives, local_peaks  
import numpy as np

if __name__ == '__main__':
    # Exemplo de uso:
    S0_initial = 100.0
    sigma_volatility = 1.0
    num_days = 252  # Um ano de dias úteis

    simulated_prices = simular_precos(S0_initial, sigma_volatility, num_days)
    
    print(simulated_prices)

    # Calcular retornos simples
    simple_returns = calc_retornos_simples(simulated_prices)
    print(f"Retornos simples: {simple_returns}")
    print(f"Número de retornos simples: {len(simple_returns)}")

    # Calcular log-retornos
    log_returns = calc_retornos_log(simulated_prices)
    print(f"Log-retornos: {log_returns}")
    print(f"Número de log-retornos: {len(log_returns)}")

     # Gerar preços e retornos de exemplo
    print(f"Retornos de exemplo (primeiros 5): {log_returns[:5]}")
    print(f"Número total de retornos: {len(log_returns)}")

    # Teste da função SMA
    window_sma = 10
    sma_results = sma(log_returns, window_sma)
    print(f"\nSMA com janela {window_sma} (primeiros 5): {sma_results[:5]}")
    print(f"Número de SMAs calculadas: {len(sma_results)}")
    print(f"Esperado: {len(log_returns) - window_sma + 1}")

    # Teste da função rolling_std
    window_std = 10
    # Caso 1: days_size = 0 (normalização por N)
    rolling_std_results_0 = rolling_std(log_returns, window_std, days_size=0)
    print(f"\nRolling Std com janela {window_std}, days_size=0 (primeiros 5): {rolling_std_results_0[:5]}")
    print(f"Número de Rolling Stds calculadas: {len(rolling_std_results_0)}")

    # Caso 2: days_size = 1 (normalização por N-1, equivalente a desvio padrão amostral)
    rolling_std_results_1 = rolling_std(log_returns, window_std, days_size=1)
    print(f"\nRolling Std com janela {window_std}, days_size=1 (primeiros 5): {rolling_std_results_1[:5]}")
    print(f"Número de Rolling Stds calculadas: {len(rolling_std_results_1)}")

    # --- Testes da função rotate_90 ---
    print("--- Testes de rotate_90 ---")
    matrix1 = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    print("Matriz original 1:\n", matrix1)
    rotated_matrix1 = rotate_90(matrix1)
    print("Matriz rotacionada 1 (90 graus horário):\n", rotated_matrix1)
    # Comparação com np.rot90 para validação (opcional, já que não é para usar a função)
    # expected_rotated1 = np.rot90(matrix1, k=-1) # k=-1 for 90 degrees clockwise
    # print("Esperado (np.rot90 k=-1):\n", expected_rotated1)
    # print("Rotação customizada igual à esperada:", np.array_equal(rotated_matrix1, expected_rotated1))

     # --- Testes da função sum_subdiagonals ---
    print("\n--- Testes de sum_subdiagonals ---")
    matrix_sum = np.array([
        [1,  2,  3,  4],
        [5,  6,  7,  8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ])
    print("Matriz para soma de subdiagonais:\n", matrix_sum)

    # k = 1: Soma da 1ª subdiagonal (abaixo da principal)
    # Elementos: A[1,0]=5, A[2,1]=10, A[3,2]=15
    # Soma esperada: 5 + 10 + 15 = 30
    k1 = 1
    sum_k1 = sum_subdiagonals(matrix_sum, k1)
    print(f"Soma da subdiagonal k={k1}: {sum_k1} (Esperado: 30.0)")

       # --- Testes da função block_matmul ---
    print("--- Testes de block_matmul ---")

    # Exemplo 1: Matrizes de tamanho exato para os blocos
    A1 = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]) # 4x4
    B1 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]) # 4x4 (matriz identidade)
    block_size1 = 2

    print(f"\nMatriz A1 ({A1.shape}):\n", A1)
    print(f"Matriz B1 ({B1.shape}):\n", B1)
    print(f"Block Size: {block_size1}")

    C1_block = block_matmul(A1, B1, block_size1)  
    C1_expected = A1 @ B1 # Produto direto para comparação
    print(f"Resultado com block_matmul C1 ({C1_block.shape}):\n", C1_block)
    print(f"Resultado esperado (A1 @ B1):\n", C1_expected)
    print(f"Resultado é aproximadamente igual ao esperado: {np.allclose(C1_block, C1_expected)}")

        # --- Testes da função replace_negatives ---
    print("--- Testes de replace_negatives ---")
    vec1 = np.array([1.0, -2.5, 3.0, -0.1, 5.0, -10.0])
    new_val1 = 0.0
    result1 = replace_negatives(vec1, new_val1)
    print(f"Vetor original: {vec1}")
    print(f"Novo valor: {new_val1}")
    print(f"Vetor resultante: {result1}")
    print(f"Original não modificado (cópia feita): {vec1 is not result1}") # Deve ser True

    series2 = np.array([5, 4, 3, 2, 1]) # Série decrescente (sem picos)
    indices2, peaks2 = local_peaks(series2)
    print(f"\nSérie original: {series2}")
    print(f"Índices dos picos locais: {indices2}")
    print(f"Valores dos picos locais: {peaks2}") # Deve ser arrays vazios

    series3 = np.array([1, 2, 3, 4, 5]) # Série crescente (sem picos)
    indices3, peaks3 = local_peaks(series3)
    print(f"\nSérie original: {series3}")
    print(f"Índices dos picos locais: {indices3}")
    print(f"Valores dos picos locais: {peaks3}") # Deve ser arrays vazios
