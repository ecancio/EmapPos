import threading
import time
import random
from typing import Dict, List, Any, Tuple

# Dicionário compartilhado para armazenar os preços das ações
prices: Dict[str, float] = {}
# Lock para sincronizar o acesso ao dicionário 'prices'
prices_lock = threading.Lock()
# Evento para sinalizar às threads quando devem parar
stop_simulation_event = threading.Event()

# Define a estrutura do order_book global e o Lock
order_book: Dict[str, List[Dict[str, Any]]] = {
    'buy': [],  # Lista de ordens de compra
    'sell': []   # Lista de ordens de venda
}
order_book_lock = threading.Lock()
order_id_counter = 0  # Contador global para IDs de ordem únicos
order_id_counter_lock = threading.Lock() # Lock para o contador de IDs

# Variáveis globais para o gerenciamento de risco
current_total_risk: float = 0.0
allocated_risk_per_strategy: Dict[str, float] = {}
risk_lock = threading.Lock()
stop_simulation_event = threading.Event() # Evento para sinalizar o fim da simulação

# Lista compartilhada para armazenar as ações que atingiram o valor_alvo
reached_target_stocks: List[str] = []
# Lock para sincronizar o acesso à lista compartilhada
reached_lock = threading.Lock()

def _generate_unique_order_id() -> int:
    """
    Gera um ID de ordem único e thread-safe.
    """
    global order_id_counter
    with order_id_counter_lock:
        order_id_counter += 1
        return order_id_counter

def _trader_task(trader_id: int, num_orders_per_trader: int) -> None:
    """
    Função que simula o comportamento de um trader colocando ordens.

    Cada trader_task coloca 'num_orders_per_trader' ordens no order_book.
    Usa um threading.Lock para garantir acesso seguro ao order_book.

    :param trader_id: ID único do trader (para identificação nos logs).
    :type trader_id: int
    :param num_orders_per_trader: Número de ordens que este trader deve colocar.
    :type num_orders_per_trader: int
    """
    for _ in range(num_orders_per_trader):
        order_type = random.choice(['buy', 'sell'])
        price = round(random.uniform(90.0, 110.0), 2)  # Preço aleatório
        quantity = random.randint(1, 100)  # Quantidade aleatória
        order_id = _generate_unique_order_id()

        order = {
            'id': order_id,
            'price': price,
            'quantity': quantity,
            'trader_id': trader_id, # Adiciona trader_id para melhor rastreamento
            'type': order_type # Adiciona tipo para consistência
        }

        # Adquire o lock antes de modificar o order_book
        with order_book_lock:
            order_book[order_type].append(order)
            # print(f"Trader {trader_id}: Colocou ordem {order_type} com ID {order_id}")
        
        # Simula algum tempo de processamento/atividade antes de colocar a próxima ordem
        # time.sleep(0.001) # Pequeno sleep para simular trabalho, pode ser removido para performance

def simular_traders(num_traders: int, num_orders: int) -> Dict[str, List[Dict[str, Any]]]:
    """
    Implementa uma simulação onde múltiplas threads (traders) inserem
    ordens de compra ou venda em uma estrutura compartilhada chamada `order_book`.

    Utiliza `threading.Lock` para garantir que o acesso ao `order_book` seja seguro e atômico.
    Após todas as threads finalizarem, retorna o estado final da estrutura `order_book`.

    :param num_traders: Número de threads (traders) a serem criadas.
                        Deve ser um inteiro positivo.
    :type num_traders: int
    :param num_orders: Número de ordens que cada trader deve colocar.
                       Deve ser um inteiro positivo.
    :type num_orders: int
    :raises TypeError: Se `num_traders` ou `num_orders` não forem inteiros.
    :raises ValueError: Se `num_traders` ou `num_orders` não forem positivos.
    :return: O estado final da estrutura `order_book`, que é um dicionário com chaves
             'buy' e 'sell', cada uma contendo uma lista de ordens (cada ordem é um
             dicionário com 'id', 'price' e 'quantity').
    :rtype: Dict[str, List[Dict[str, Any]]]
    """
    global order_book, order_id_counter # Resetar para cada nova simulação
    
    # Validações dos parâmetros
    if not isinstance(num_traders, int) or num_traders <= 0:
        raise ValueError("num_traders deve ser um inteiro positivo.")
    if not isinstance(num_orders, int) or num_orders <= 0:
        raise ValueError("num_orders deve ser um inteiro positivo.")

    # Reinicia o order_book e o contador de IDs para garantir uma simulação limpa
    # Isso é importante se a função for chamada múltiplas vezes.
    order_book = {'buy': [], 'sell': []}
    order_id_counter = 0

    threads: List[threading.Thread] = []

    # Cria e inicia as threads dos traders
    for i in range(num_traders):
        thread = threading.Thread(target=_trader_task, args=(i + 1, num_orders))
        threads.append(thread)
        thread.start()

    # Espera que todas as threads terminem
    for thread in threads:
        thread.join()

    print(f"\nSimulação concluída!")
    print(f"Total de ordens de compra: {len(order_book['buy'])}")
    print(f"Total de ordens de venda: {len(order_book['sell'])}")
    print(f"Total geral de ordens: {len(order_book['buy']) + len(order_book['sell'])}")
    print(f"Número total de IDs únicos gerados: {order_id_counter}")

    return order_book

def _stock_feed_task(stock_name: str) -> None:
    """
    Simula um feed de dados para uma ação específica, atualizando seu preço
    periodicamente no dicionário global 'prices'.

    :param stock_name: O nome da ação (ticker).
    :type stock_name: str
    """
    # Inicializa o preço da ação no dicionário compartilhado
    with prices_lock:
        prices[stock_name] = 100.0  # Preço inicial arbitrário

    print(f"Feed para {stock_name} iniciado com preço inicial {prices[stock_name]:.2f}")

    while not stop_simulation_event.is_set():
        # Gera uma variação de preço aleatória (e.g., -1% a +1%)
        price_change_factor = 1 + random.uniform(-0.01, 0.01)

        with prices_lock:
            current_price = prices[stock_name]
            new_price = current_price * price_change_factor
            # Garante que o preço não caia para zero ou negativo
            if new_price < 0.01:
                new_price = 0.01
            prices[stock_name] = new_price
            # print(f"[{time.time():.2f}] {stock_name}: Preço atualizado para {new_price:.2f}")

        # Tempo de espera aleatório (1 a 3 segundos) antes da próxima atualização
        wait_time = random.uniform(1, 3)
        # Usa wait() do evento para poder parar a thread antes do timeout
        if stop_simulation_event.wait(wait_time):
            break # Se o evento foi setado, sai do loop

    print(f"Feed para {stock_name} finalizado.")

def _printer_task() -> None:
    """
    Imprime os preços atuais de todas as ações no dicionário 'prices' a cada 5 segundos.
    """
    print("Thread de impressão iniciada.")
    while not stop_simulation_event.is_set():
        with prices_lock:
            # Cria uma cópia para imprimir e evitar manter o lock por muito tempo
            current_prices = prices.copy()
        
        print("\n--- Preços Atuais ---")
        for stock, price in sorted(current_prices.items()):
            print(f"{stock}: {price:.2f}")
        print("---------------------\n")
        
        # Espera por 5 segundos, verificando se a simulação deve parar
        if stop_simulation_event.wait(5):
            break # Se o evento foi setado, sai do loop
    print("Thread de impressão finalizada.")

def simular_feeds_de_dados(acoes: List[str], tempo_total: int) -> Dict[str, float]:
    """
    Simula a atualização de feeds de dados de preços de ações concorrentemente.

    Cria um dicionário compartilhado `prices` que armazena os preços atuais
    de várias ações. Uma thread é criada para cada ação em `acoes`,
    representando um feed de dados que atualiza periodicamente (a cada 1-3 segundos)
    o preço da sua ação no dicionário. Um `threading.Lock` é usado para
    sincronizar o acesso ao dicionário. Uma thread adicional imprime os preços
    atuais a cada 5 segundos. A simulação roda por `tempo_total` segundos.

    :param acoes: Lista de nomes de ações (e.g., ["AAPL", "GOOG", "TSLA"]).
                  Deve conter pelo menos um nome de ação.
    :type acoes: List[str]
    :param tempo_total: Tempo total de simulação em segundos.
                        Deve ser um inteiro positivo.
    :type tempo_total: int
    :raises TypeError: Se `acoes` não for uma lista de strings, ou `tempo_total` não for um inteiro.
    :raises ValueError: Se `acoes` estiver vazia, ou `tempo_total` não for positivo.
    :return: O dicionário final de preços após a simulação.
    :rtype: Dict[str, float]

    :Example:
    >>> # Para rodar o exemplo, este bloco precisa ser executado.
    >>> # É recomendado rodá-lo separadamente para ver o output em tempo real.
    >>> # final_prices = simular_feeds_de_dados(acoes=["MSFT", "AMZN"], tempo_total=10)
    >>> # print("\\nFinal Prices:", final_prices)
    """
    global prices, stop_simulation_event # Acessa e reseta as variáveis globais

    # Validações dos parâmetros
    if not isinstance(acoes, list) or not all(isinstance(a, str) for a in acoes):
        raise TypeError("acoes deve ser uma lista de strings (nomes de ações).")
    if not acoes:
        raise ValueError("A lista de ações não pode estar vazia.")
    if not isinstance(tempo_total, int) or tempo_total <= 0:
        raise ValueError("tempo_total deve ser um inteiro positivo.")

    # Reinicia o dicionário de preços e o evento para uma nova simulação limpa
    prices = {}
    stop_simulation_event.clear() # Garante que o evento não esteja setado de uma execução anterior

    threads: List[threading.Thread] = []

    # Cria e inicia as threads para cada feed de dados de ações
    for stock in acoes:
        thread = threading.Thread(target=_stock_feed_task, args=(stock,))
        threads.append(thread)
        thread.start()

    # Cria e inicia a thread de impressão
    printer_thread = threading.Thread(target=_printer_task)
    threads.append(printer_thread)
    printer_thread.start()

    print(f"\nSimulação iniciada por {tempo_total} segundos...")
    # Aguarda o tempo total da simulação
    time.sleep(tempo_total)

    print("\nTempo de simulação esgotado. Sinalizando threads para pararem...")
    # Sinaliza para todas as threads que elas devem parar
    stop_simulation_event.set()

    # Espera que todas as threads terminem a execução
    for thread in threads:
        thread.join()

    print("\nTodas as threads foram finalizadas.")
    # Retorna o estado final do dicionário de preços
    with prices_lock:
        final_prices = prices.copy()
    return final_prices    

def _strategy_task(strategy_name: str, requested_risk: float, total_risk_limit: float) -> None:
    """
    Função que simula uma estratégia tentando alocar risco em um portfólio.
    Esta função é executada por cada thread de estratégia.

    A estratégia verifica o risco total atual e, se houver espaço (ou seja,
    não excederá o limite `total_risk_limit` ao alocar `requested_risk`),
    ela aloca seu risco. Se o risco total exceder o limite, a thread espera.

    :param strategy_name: O nome da estratégia.
    :type strategy_name: str
    :param requested_risk: A quantidade de risco que esta estratégia deseja alocar.
    :type requested_risk: float
    :param total_risk_limit: O limite máximo de risco disponível para o portfólio.
    :type total_risk_limit: float
    """
    global current_total_risk, allocated_risk_per_strategy

    print(f"Estratégia {strategy_name}: Iniciada, solicitando {requested_risk:.2f} de risco.")

    # Loop para tentar alocar risco enquanto a simulação não for parada
    while not stop_simulation_event.is_set():
        with risk_lock:
            if current_total_risk + requested_risk <= total_risk_limit:
                # Há espaço: aloca o risco
                current_total_risk += requested_risk
                allocated_risk_per_strategy[strategy_name] = (
                    allocated_risk_per_strategy.get(strategy_name, 0.0) + requested_risk
                )
                print(f"Estratégia {strategy_name}: ALOCADO {requested_risk:.2f}. Risco total atual: {current_total_risk:.2f}")
                break  # Risco alocado, a thread pode terminar sua tarefa de alocação
            else:
                # Não há espaço: espera e tenta novamente
                print(f"Estratégia {strategy_name}: Risco insuficiente ({current_total_risk:.2f}/{total_risk_limit:.2f}). Esperando...")

        # Espera por um tempo antes de tentar novamente se não conseguiu alocar
        # random.uniform para simular variabilidade no tempo de espera
        wait_time = random.uniform(0.1, 0.5) # Espera entre 100ms e 500ms
        if stop_simulation_event.wait(wait_time):
            break # Se o evento de parada for setado durante a espera, sai do loop

    print(f"Estratégia {strategy_name}: Finalizada. Risco alocado final: {allocated_risk_per_strategy.get(strategy_name, 0.0):.2f}")


def gerenciar_risco(total_risco: float, estrategias: List[Tuple[str, float]], tempo_total: int) -> Dict[str, float]:
    """
    Gerencia a alocação de risco em um portfólio por múltiplas estratégias concorrentemente.

    Cada estratégia tenta alocar uma quantidade de risco em um limite total.
    Usa `threading.Lock` para proteger a variável de risco total compartilhada.
    Se o risco exceder o limite, a thread de estratégia espera.

    :param total_risco: Limite total de risco disponível para o portfólio.
                        Deve ser um float positivo.
    :type total_risco: float
    :param estrategias: Lista de tuplas, onde cada tupla contém o nome da estratégia (str)
                         e o risco que ela deseja alocar (float).
                         Ex: [("EstrategiaA", 10.5), ("EstrategiaB", 5.0)].
    :type estrategias: List[Tuple[str, float]]
    :param tempo_total: Tempo total de simulação em segundos.
                        Deve ser um inteiro positivo.
    :type tempo_total: int
    :raises TypeError: Se os tipos dos parâmetros não corresponderem ao esperado.
    :raises ValueError: Se os valores dos parâmetros forem inválidos (e.g., limites não positivos,
                        lista de estratégias vazia, risco solicitado não positivo).
    :return: Um dicionário com o risco alocado por cada estratégia ao final da simulação.
    :rtype: Dict[str, float]

    :Example:
    >>> # Para rodar o exemplo, este bloco precisa ser executado.
    >>> # É recomendado rodá-lo separadamente para ver o output em tempo real.
    >>> #
    >>> # limit = 100.0
    >>> # strategies_list = [("Alpha", 30.0), ("Beta", 40.0), ("Gamma", 25.0), ("Delta", 20.0)]
    >>> # final_allocation = gerenciar_risco(limit, strategies_list, 5)
    >>> # print("\\nAlocação Final de Risco:", final_allocation)
    """
    global current_total_risk, allocated_risk_per_strategy, stop_simulation_event

    # --- Validação de Parâmetros ---
    if not isinstance(total_risco, (int, float)) or total_risco <= 0:
        raise ValueError("total_risco deve ser um float positivo.")
    if not isinstance(estrategias, list) or not all(isinstance(e, tuple) and len(e) == 2 and isinstance(e[0], str) and isinstance(e[1], (int, float)) and e[1] > 0 for e in estrategias):
        raise TypeError("estrategias deve ser uma lista de tuplas (nome_estrategia: str, risco_solicitado: float positivo).")
    if not estrategias:
        raise ValueError("A lista de estratégias não pode estar vazia.")
    if not isinstance(tempo_total, int) or tempo_total <= 0:
        raise ValueError("tempo_total deve ser um inteiro positivo.")

    # --- Inicialização Global para a Simulação ---
    current_total_risk = 0.0
    allocated_risk_per_strategy = {strat[0]: 0.0 for strat in estrategias} # Inicializa com 0 para todas as estratégias
    stop_simulation_event.clear() # Garante que o evento não esteja setado de uma execução anterior

    threads: List[threading.Thread] = []

    # Cria e inicia as threads para cada estratégia
    for name, risk_value in estrategias:
        thread = threading.Thread(target=_strategy_task, args=(name, risk_value, total_risco))
        threads.append(thread)
        thread.start()

    print(f"\nSimulação de gerenciamento de risco iniciada por {tempo_total} segundos.")
    print(f"Limite total de risco: {total_risco:.2f}")

    # Aguarda o tempo total da simulação
    time.sleep(tempo_total)

    print("\nTempo de simulação esgotado. Sinalizando threads para pararem...")
    # Sinaliza para todas as threads que elas devem parar
    stop_simulation_event.set()

    # Espera que todas as threads terminem a execução
    for thread in threads:
        thread.join()

    print("\nTodas as threads de estratégia foram finalizadas.")
    print(f"Risco total final alocado: {current_total_risk:.2f}")

    # Retorna o estado final da alocação de risco
    return allocated_risk_per_strategy

def _monitor_stock_task(stock_name: str, valor_alvo: float) -> None:

    """
    Função que simula o monitoramento de uma única ação.

    Gera um valor anterior e um valor atual para o preço da ação com pequenos
    atrasos aleatórios. Verifica se o `valor_alvo` foi atingido ou ultrapassado
    entre esses dois valores. Se sim, adiciona o nome da ação à lista compartilhada.

    :param stock_name: O nome da ação (ticker).
    :type stock_name: str
    :param valor_alvo: O valor a ser monitorado nas oscilações do preço da ação.
    :type valor_alvo: float
    """
    global reached_target_stocks # Indica que estamos modificando a variável global

    # Simula a obtenção do valor anterior com um pequeno atraso
    time.sleep(random.uniform(0.05, 0.2)) # Atraso de 50ms a 200ms
    # Gerar um valor anterior aleatório, centrado ao redor do valor_alvo, mas com variação
    # Para garantir que o valor_alvo possa estar entre eles, geramos um intervalo que inclui o alvo.
    # Ex: se alvo é 100, anterior pode ser 95 ou 105.
    variation_range = valor_alvo * 0.1 # +/- 10% do valor_alvo como range de variação
    valor_anterior = random.uniform(valor_alvo - variation_range, valor_alvo + variation_range)

    # Simula a obtenção do valor atual com outro pequeno atraso
    time.sleep(random.uniform(0.05, 0.2)) # Atraso de 50ms a 200ms
    valor_atual = random.uniform(valor_alvo - variation_range, valor_alvo + variation_range)


    # Garante que os valores não sejam negativos (preços)
    valor_anterior = max(0.01, valor_anterior)
    valor_atual = max(0.01, valor_atual)

    # Ordena os valores para facilitar a verificação do intervalo
    min_price = min(valor_anterior, valor_atual)
    max_price = max(valor_anterior, valor_atual)

    print(f"[{time.time():.2f}] {stock_name}: Anterior={valor_anterior:.2f}, Atual={valor_atual:.2f}, Alvo={valor_alvo:.2f}")

    # Verifica se o valor_alvo está entre o valor anterior e o valor atual (inclusive extremidades)
    if min_price <= valor_alvo <= max_price:
        # Se o valor_alvo foi atingido/ultrapassado, adiciona à lista compartilhada
        with reached_lock:
            reached_target_stocks.append(stock_name)
            print(f"!!! {stock_name}: ALVO {valor_alvo:.2f} ATINGIDO/ULTRAPASSADO !!!")
    else:
        print(f"    {stock_name}: Alvo {valor_alvo:.2f} NÃO atingido.")

def monitorar_acoes(acoes: List[str], valor_alvo: float) -> List[str]:
    """
    Simula o monitoramento concorrente de ações utilizando múltiplas threads.

    Cada thread é responsável por monitorar uma ação específica. Para simular
    a variação do preço, gera um valor anterior e um valor atual para cada ação,
    ambos obtidos com um pequeno atraso aleatório. A thread verifica se o
    `valor_alvo` está entre o valor anterior e o valor atual da ação (inclusive
    as extremidades). Todas as ações que atingirem o `valor_alvo` devem ser
    adicionadas a uma lista compartilhada. `threading.Lock` é utilizado para
    garantir que a lista compartilhada seja acessada de forma segura.

    :param acoes: Lista de nomes de ações (e.g., ["AAPL", "GOOG", "TSLA"]).
                  Deve conter pelo menos um nome de ação.
    :type acoes: List[str]
    :param valor_alvo: Valor a ser monitorado nas oscilações do preço das ações.
                       Deve ser um float positivo.
    :type valor_alvo: float
    :raises TypeError: Se `acoes` não for uma lista de strings, ou `valor_alvo` não for numérico.
    :raises ValueError: Se `acoes` estiver vazia, ou `valor_alvo` não for positivo.
    :return: Lista com os nomes das ações cujo preço atingiu ou ultrapassou o `valor_alvo`
             entre o valor anterior e o valor atual.
    :rtype: List[str]

    :Example:
    >>> # Exemplo de uso:
    >>> # stocks_to_monitor = ["BRK.A", "JPM", "GS"]
    >>> # target_value = 200.0
    >>> # hit_stocks = monitorar_acoes(stocks_to_monitor, target_value)
    >>> # print("\\nAções que atingiram o valor alvo:", hit_stocks)
    """
    global reached_target_stocks # Garante que estamos usando a variável global

    # --- Validação de Parâmetros ---
    if not isinstance(acoes, list) or not all(isinstance(a, str) for a in acoes):
        raise TypeError("acoes deve ser uma lista de strings (nomes de ações).")
    if not acoes:
        raise ValueError("A lista de ações não pode estar vazia.")
    if not isinstance(valor_alvo, (int, float)) or valor_alvo <= 0:
        raise ValueError("valor_alvo deve ser um float positivo.")

    # Reinicia a lista de ações atingidas para cada nova execução
    reached_target_stocks.clear()

    threads: List[threading.Thread] = []

    # Cria e inicia uma thread para cada ação
    for stock_name in acoes:
        thread = threading.Thread(target=_monitor_stock_task, args=(stock_name, valor_alvo))
        threads.append(thread)
        thread.start()

    print("\nIniciando monitoramento concorrente de ações...")

    # Espera que todas as threads terminem sua execução
    for thread in threads:
        thread.join()

    print("\nMonitoramento concluído para todas as ações.")

    # Retorna a lista final de ações que atingiram o valor alvo
    return reached_target_stocks