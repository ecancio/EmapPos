import random
from ThreadingBasics import simular_traders, simular_feeds_de_dados, gerenciar_risco, monitorar_acoes
from AdvancedConcurrency import calcular_medias_moveis, calcular_volatilidade
import numpy as np  

if __name__ == '__main__':
    # Exemplo de uso da função:
    print("Iniciando simulação com 5 traders e 100 ordens por trader...")
    final_order_book = simular_traders(num_traders=5, num_orders=100)

    # Verificando algumas ordens (opcional)
    if final_order_book['buy']:
        print("\nPrimeiras 5 ordens de compra:")
        for order in final_order_book['buy'][:5]:
            print(order)
    if final_order_book['sell']:
        print("\nPrimeiras 5 ordens de venda:")
        for order in final_order_book['sell'][:5]:
            print(order)

    # Verificações de integridade (opcional)
    total_orders_placed = sum(len(final_order_book[key]) for key in final_order_book)
    expected_total_orders = 5 * 100
    print(f"\nVerificação: Ordens totais esperadas: {expected_total_orders}, Ordens colocadas: {total_orders_placed}")
    assert total_orders_placed == expected_total_orders, "O número total de ordens não corresponde ao esperado!"
    print("Verificação do número total de ordens: OK")

    # Verificar se os IDs são únicos
    all_order_ids = [order['id'] for order_list in final_order_book.values() for order in order_list]
    assert len(all_order_ids) == len(set(all_order_ids)), "Foram gerados IDs de ordem duplicados!"
    print("Verificação de IDs únicos: OK")

    # Testando com valores extremos ou inválidos
    print("\n--- Testes de Validação ---")
    try:
        simular_traders(num_traders=0, num_orders=10)
    except ValueError as e:
        print(f"Erro esperado para num_traders=0: {e}")

    try:
        simular_traders(num_traders=5, num_orders=-1)
    except ValueError as e:
        print(f"Erro esperado para num_orders negativo: {e}")

    try:
        simular_traders(num_traders=2, num_orders=10)
    except ValueError as e: # Catch ValueError because type check is part of validation
        print(f"Erro esperado para num_traders não inteiro: {e}")

    try:
        simular_traders(num_traders=1, num_orders="abc")
    except ValueError as e: # Catch ValueError because type check is part of validation
        print(f"Erro esperado para num_orders não inteiro: {e}")

    print("\nSimulação com 2 traders e 5 ordens cada para verificar saída pequena...")
    small_order_book = simular_traders(num_traders=2, num_orders=5)
    print("\nEstado final do order_book (pequeno):")
    print(small_order_book)
    assert len(small_order_book['buy']) + len(small_order_book['sell']) == 10
    print("Verificação do número total de ordens para caso pequeno: OK")

    # Exemplo de uso
    acoes_para_simular = ["AAPL", "GOOG", "TSLA", "MSFT"]
    tempo_sim = 15 # segundos

    print(f"Iniciando simulação de feeds de dados para {acoes_para_simular} por {tempo_sim} segundos.")
    final_prices_result = simular_feeds_de_dados(acoes=acoes_para_simular, tempo_total=tempo_sim)

    print("\n--- Dicionário Final de Preços ---")
    for stock, price in sorted(final_prices_result.items()):
        print(f"{stock}: {price:.2f}")
    print("---------------------------------\n")

    
    print("--- Teste de Gerenciamento de Risco Concorrente ---")

    # Exemplo 1: Limite que permite que todas as estratégias aloquem risco
    print("\n--- Exemplo 1: Todas as estratégias conseguem alocar ---")
    total_risk_limit_1 = 100.0
    strategies_1 = [
        ("Estratégia A", 20.0),
        ("Estratégia B", 30.0),
        ("Estratégia C", 40.0)
    ]
    sim_time_1 = 3 # segundos
    final_allocation_1 = gerenciar_risco(total_risk_limit_1, strategies_1, sim_time_1)
    print("\nAlocação Final de Risco (Exemplo 1):", final_allocation_1)
    print(f"Risco Total Alocado Final (Exemplo 1): {sum(final_allocation_1.values()):.2f}")
    assert sum(final_allocation_1.values()) <= total_risk_limit_1
    assert all(strat[1] <= final_allocation_1.get(strat[0], 0.0) for strat in strategies_1)


    # Exemplo 2: Limite apertado, algumas estratégias podem não conseguir alocar tudo
    print("\n--- Exemplo 2: Limite apertado ---")
    total_risk_limit_2 = 50.0
    strategies_2 = [
        ("Estratégia X", 30.0),
        ("Estratégia Y", 25.0),
        ("Estratégia Z", 10.0)
    ]
    sim_time_2 = 5 # segundos (dá mais tempo para as threads tentarem)
    final_allocation_2 = gerenciar_risco(total_risk_limit_2, strategies_2, sim_time_2)
    print("\nAlocação Final de Risco (Exemplo 2):", final_allocation_2)
    print(f"Risco Total Alocado Final (Exemplo 2): {sum(final_allocation_2.values()):.2f}")
    assert sum(final_allocation_2.values()) <= total_risk_limit_2


    # Exemplo 3: Apenas uma estratégia, para verificar o comportamento básico
    print("\n--- Exemplo 3: Uma única estratégia ---")
    total_risk_limit_3 = 10.0
    strategies_3 = [("Unica", 7.5)]
    sim_time_3 = 2
    final_allocation_3 = gerenciar_risco(total_risk_limit_3, strategies_3, sim_time_3)
    print("\nAlocação Final de Risco (Exemplo 3):", final_allocation_3)
    print(f"Risco Total Alocado Final (Exemplo 3): {sum(final_allocation_3.values()):.2f}")
    assert sum(final_allocation_3.values()) == 7.5

    print("--- Teste de Gerenciamento de Risco Concorrente ---")

    # Exemplo 1: Limite que permite que todas as estratégias aloquem risco
    print("\n--- Exemplo 1: Todas as estratégias conseguem alocar ---")
    total_risk_limit_1 = 100.0
    strategies_1 = [
        ("Estratégia A", 20.0),
        ("Estratégia B", 30.0),
        ("Estratégia C", 40.0)
    ]
    sim_time_1 = 3 # segundos
    final_allocation_1 = gerenciar_risco(total_risk_limit_1, strategies_1, sim_time_1)
    print("\nAlocação Final de Risco (Exemplo 1):", final_allocation_1)
    print(f"Risco Total Alocado Final (Exemplo 1): {sum(final_allocation_1.values()):.2f}")
    assert sum(final_allocation_1.values()) <= total_risk_limit_1
    assert all(strat[1] <= final_allocation_1.get(strat[0], 0.0) for strat in strategies_1)


    # Exemplo 2: Limite apertado, algumas estratégias podem não conseguir alocar tudo
    print("\n--- Exemplo 2: Limite apertado ---")
    total_risk_limit_2 = 50.0
    strategies_2 = [
        ("Estratégia X", 30.0),
        ("Estratégia Y", 25.0),
        ("Estratégia Z", 10.0)
    ]
    sim_time_2 = 5 # segundos (dá mais tempo para as threads tentarem)
    final_allocation_2 = gerenciar_risco(total_risk_limit_2, strategies_2, sim_time_2)
    print("\nAlocação Final de Risco (Exemplo 2):", final_allocation_2)
    print(f"Risco Total Alocado Final (Exemplo 2): {sum(final_allocation_2.values()):.2f}")
    assert sum(final_allocation_2.values()) <= total_risk_limit_2


    # Exemplo 3: Apenas uma estratégia, para verificar o comportamento básico
    print("\n--- Exemplo 3: Uma única estratégia ---")
    total_risk_limit_3 = 10.0
    strategies_3 = [("Unica", 7.5)]
    sim_time_3 = 2
    final_allocation_3 = gerenciar_risco(total_risk_limit_3, strategies_3, sim_time_3)
    print("\nAlocação Final de Risco (Exemplo 3):", final_allocation_3)
    print(f"Risco Total Alocado Final (Exemplo 3): {sum(final_allocation_3.values()):.2f}")
    assert sum(final_allocation_3.values()) == 7.5


    # --- Exemplos de Uso ---
    print("--- Exemplo 1: Alvo alcançável ---")
    stocks1 = ["AAPL", "GOOG", "MSFT"]
    target1 = 175.0
    random.seed(42) # Para reprodutibilidade do exemplo
    hit_stocks1 = monitorar_acoes(stocks1, target1)
    print(f"\nAções que atingiram o valor alvo ({target1:.2f}): {hit_stocks1}")
    # Nota: A saída exata pode variar ligeiramente devido aos `time.sleep` e à concorrência,
    # mas o resultado final da lista deve ser consistente com a semente random.

    print("\n--- Exemplo 2: Alvo mais difícil de alcançar ---")
    stocks2 = ["TSLA", "AMZN", "NVDA"]
    target2 = 1000.0
    random.seed(10) # Outra semente para diferentes resultados
    hit_stocks2 = monitorar_acoes(stocks2, target2)
    print(f"\nAções que atingiram o valor alvo ({target2:.2f}): {hit_stocks2}")

    print("\n--- Exemplo 3: Apenas uma ação ---")
    stocks3 = ["KO"]
    target3 = 60.0
    random.seed(20)
    hit_stocks3 = monitorar_acoes(stocks3, target3)
    print(f"\nAções que atingiram o valor alvo ({target3:.2f}): {hit_stocks3}")


     # --- Exemplos de Uso ---
    print("--- Exemplo 1: Duas ações, janela pequena ---")
    prices_data_1 = {
        "AAPL": np.array([100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0]),
        "GOOG": np.array([200.0, 202.0, 201.0, 205.0, 203.0, 207.0, 206.0])
    }
    window_size_1 = 3
    mas_1 = calcular_medias_moveis(prices_data_1, window_size_1)
    print("\nMédias Móveis Calculadas (Exemplo 1):")
    for stock, ma_array in mas_1.items():
        print(f"  {stock}: {ma_array}")
    # Verificar alguns valores:
    # AAPL [101. 102. 103. 104. 105.] (100+101+102)/3 = 101
    # GOOG [201.  202.66666667  203.  205.  205.33333333]

    print("\n--- Exemplo 2: Mais ações, janela maior ---")
    prices_data_2 = {
        "MSFT": np.array([150.0, 151.5, 152.0, 150.5, 153.0, 154.0, 151.0, 155.0, 156.0, 157.5]),
        "AMZN": np.array([3000.0, 3010.0, 3005.0, 3020.0, 3015.0, 3030.0, 3025.0, 3040.0, 3035.0, 3050.0]),
        "TSLA": np.array([900.0, 910.0, 905.0, 920.0, 915.0, 930.0, 925.0, 940.0, 935.0, 950.0])
    }
    window_size_2 = 5
    mas_2 = calcular_medias_moveis(prices_data_2, window_size_2)
    print("\nMédias Móveis Calculadas (Exemplo 2):")
    for stock, ma_array in mas_2.items():
        print(f"  {stock}: {ma_array}")

    print("\n--- Exemplo 3: Ação com dados insuficientes para a janela ---")
    prices_data_3 = {
        "SHORT": np.array([10.0, 11.0]),
        "LONG": np.array([100.0, 101.0, 102.0, 103.0])
    }
    window_size_3 = 3
    mas_3 = calcular_medias_moveis(prices_data_3, window_size_3)
    print("\nMédias Móveis Calculadas (Exemplo 3):")
    for stock, ma_array in mas_3.items():
        print(f"  {stock}: {ma_array}")
    # 'SHORT' deve ter um array vazio. 'LONG' deve ter resultados.


 # --- Exemplos de Uso ---
    print("--- Exemplo 1: Retornos simples, janela pequena, 2 threads ---")
    daily_returns_1 = np.array([0.01, 0.02, -0.01, 0.03, 0.005, -0.02, 0.015, 0.00, 0.008, -0.005, 0.012, 0.003])
    window_1 = 3
    num_threads_1 = 2
    volatilities_1 = calcular_volatilidade(daily_returns_1, window_1, num_threads_1)
    print(f"\nVolatilidades Calculadas (Janela {window_1}, Threads {num_threads_1}): {volatilities_1}")

    # Para comparação, cálculo serial
    serial_volatilities_1 = []
    for i in range(len(daily_returns_1) - window_1 + 1):
        serial_volatilities_1.append(np.std(daily_returns_1[i : i + window_1], ddof=1))
    serial_volatilities_1 = np.array(serial_volatilities_1)
    print(f"Volatilidades Seriais (para comparação): {serial_volatilities_1}")
    assert np.allclose(volatilities_1, serial_volatilities_1), "O resultado paralelo não corresponde ao serial!"
    print("Verificação de correspondência com cálculo serial: OK.")


    print("\n--- Exemplo 2: Retornos maiores, janela média, 4 threads ---")
    # Gerar retornos aleatórios mais longos
    np.random.seed(42)
    daily_returns_2 = np.random.normal(loc=0.0005, scale=0.01, size=200) # 200 dias de retornos
    window_2 = 20 # Janela de 20 dias (um mês útil)
    num_threads_2 = 4
    volatilities_2 = calcular_volatilidade(daily_returns_2, window_2, num_threads_2)
    print(f"\nVolatilidades Calculadas (Janela {window_2}, Threads {num_threads_2}). Primeiros 5: {volatilities_2[:5]}")
    print(f"Tamanho do array de volatilidades: {len(volatilities_2)}")

    # Comparação serial para o segundo exemplo
    serial_volatilities_2 = []
    for i in range(len(daily_returns_2) - window_2 + 1):
        serial_volatilities_2.append(np.std(daily_returns_2[i : i + window_2], ddof=1))
    serial_volatilities_2 = np.array(serial_volatilities_2)
    assert np.allclose(volatilities_2, serial_volatilities_2), "O resultado paralelo não corresponde ao serial para Exemplo 2!"
    print("Verificação de correspondência com cálculo serial (Exemplo 2): OK.")


    print("\n--- Exemplo 3: Janela maior que os retornos ---")
    returns_short = np.array([0.01, 0.02])
    window_short = 5
    num_threads_short = 1
    volatilities_short = calcular_volatilidade(returns_short, window_short, num_threads_short)
    print(f"\nVolatilidades Calculadas (Janela {window_short}, retornos curtos): {volatilities_short}")
    assert len(volatilities_short) == 0
    print("Verificação de array vazio para dados insuficientes: OK.")

