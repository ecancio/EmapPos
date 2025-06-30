from collections import defaultdict, Counter
import math

def future_value_m1(pv, r, n, t):
    """
    Maneira 1: Calcula o valor futuro usando o operador de potência **.
    Args:
        pv (float): Valor presente (principal).
        r (float): Taxa de juros anual (ex: 0.05 para 5%).
        n (int): Número de períodos de capitalização por ano.
        t (float): Tempo em anos.    
    Returns:
        float: O valor futuro do investimento.
    """
    # A fórmula é aplicada diretamente.
    fv = pv * (1 + r / n) ** (n * t)
    return fv

def future_value_m2(pv, r, n, t):
    """
    Maneira 2: Calcula o valor futuro usando a função math.pow().
    Args:
        pv (float): Valor presente (principal).
        r (float): Taxa de juros anual (ex: 0.05 para 5%).
        n (int): Número de períodos de capitalização por ano.
        t (float): Tempo em anos.    
    Returns:
        float: O valor futuro do investimento.
    """
    # math.pow(base, expoente) realiza a mesma operação que base ** expoente.
    base = 1 + r / n
    expoente = n * t
    fv = pv * math.pow(base, expoente)
    return fv

def standard_deviation_m1(returns):
    """
    Maneira 1: Calcula o desvio padrão com um laço for explícito.    
    Args:
        returns (list[float]): Uma lista de valores numéricos (retornos).

    Returns:
        float: O desvio padrão dos valores.
    """
    n = len(returns)
    if n == 0:
        return 0
    
    # Passo 1: Calcular a média (x̄)
    mean = sum(returns) / n
    
    # Passo 2: Calcular a soma dos quadrados das diferenças (Σ(xi - x̄)²)
    sum_squared_diff = 0
    for x in returns:
        sum_squared_diff += (x - mean) ** 2
        
    # Passo 3: Calcular a variância e, em seguida, o desvio padrão (raiz da variância)
    variance = sum_squared_diff / n
    std_dev = math.sqrt(variance)
    
    return std_dev

# Exemplo:
print(f"Maneira 2: R$ {future_value_m2(1000, 0.05, 12, 10):.2f}")
print(f"Maneira 1: R$ {future_value_m1(1000, 0.05, 12, 10):.2f}")

# Exemplo:
retornos = [0.1, 0.05, -0.02, 0.08, 0.03]

def standard_deviation_m2(returns):
    """
    Maneira 2: Calcula o desvio padrão de forma compacta e funcional.
    
    Args:
        returns (list[float]): Uma lista de valores numéricos (retornos).

    Returns:
        float: O desvio padrão dos valores.
    """
    n = len(returns)
    if n == 0:
        return 0
    
    # Calcula a média
    mean = sum(returns) / n
    
    # Usa uma expressão geradora para calcular a soma dos quadrados das diferenças
    # e divide por n para obter a variância, tudo em uma linha.
    variance = sum((x - mean) ** 2 for x in returns) / n
    
    # Retorna a raiz quadrada da variância.
    return math.sqrt(variance)

print(f"Maneira 1: {standard_deviation_m1(retornos):.4f}")
print(f"Maneira 2: {standard_deviation_m2(retornos):.4f}")

def time_to_double_m1(r):
    """
    Maneira 1: Calcula o tempo para dobrar usando logaritmo natural (ln).

    Args:
        r (float): A taxa de crescimento contínuo (ex: 0.07 para 7%).

    Returns:
        float: O número de anos para o investimento dobrar.
    """
    # math.log(x) calcula o logaritmo natural de x.
    return math.log(2) / math.log(1 + r)

def time_to_double_m2(r):
    """
    Maneira 2: Calcula o tempo para dobrar usando logaritmo na base 10.
    O resultado é idêntico devido à propriedade de mudança de base dos logaritmos.

    Args:
        r (float): A taxa de crescimento contínuo (ex: 0.07 para 7%).

    Returns:
        float: O número de anos para o investimento dobrar.
    """
    # A razão entre logs da mesma base é constante.
    # log_b(x) / log_b(y) == ln(x) / ln(y)
    return math.log10(2) / math.log10(1 + r)

# Exemplo (Regra dos 72 aproximada -> 72/7 ~ 10.2)
print(f"Maneira 1: {time_to_double_m1(0.07):.2f} anos")

print(f"Maneira 1: {time_to_double_m2(0.07):.2f} anos")