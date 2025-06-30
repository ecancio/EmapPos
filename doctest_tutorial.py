"""
doctest_tutorial.py
-------------------

Este módulo contém exemplos de funções simples com testes embutidos nas docstrings (DocTest).

Para executar todos os testes, use:
    doctest -v doctest_tutorial.py

ou execute:
    python doctest_tutorial.py
"""


def soma(x: int | float, y: int | float) -> int | float:
    """
    Soma x e y.

    Args:
        x (int | float): Primeiro operando.
        y (int | float): Segundo operando.

    Returns:
        int | float: Resultado da adição de x e y.

    Examples:
        >>> soma(1, 2)
        3
        >>> soma(-5, 5)
        0
        >>> soma(2.5, 3.1)
        5.6
    """
    return x + y


def divide(x: int | float, y: int | float) -> float:
    """
    Divide x por y.

    Args:
        x (int | float): Dividendo.
        y (int | float): Divisor (não pode ser zero).

    Returns:
        float: Resultado da divisão x / y.

    Raises:
        ValueError: Se y for igual a zero.

    Examples:
        >>> divide(8, 2)
        4.0
        >>> divide(5, 2)
        2.5
        >>> divide(5, 0)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: Divisor não pode ser zero.
    """
    if y == 0:
        raise ValueError("Divisor não pode ser zero.")
    return x / y


def fatorial(n: int) -> int:
    """
    Calcula o fatorial de n (n!).

    Args:
        n (int): Número inteiro não-negativo.

    Returns:
        int: Fatorial de n.

    Raises:
        ValueError: Se n for negativo ou não for inteiro.

    Examples:
        >>> fatorial(5)
        120
        >>> fatorial(0)
        1
        >>> fatorial(-1)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: n não pode ser negativo.
    """
    if not isinstance(n, int):
        raise ValueError("n deve ser um inteiro.")
    if n < 0:
        raise ValueError("n não pode ser negativo.")
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def conte_palavras(texto: str) -> int:
    """
    Conta palavras em uma string (separadas por espaços).

    Args:
        texto (str): Texto de entrada.

    Returns:
        int: Número de palavras encontradas.

    Examples:
        >>> conte_palavras("Olá mundo")
        2
        >>> conte_palavras("   python  é   legal  ")
        3
    """
    return len(texto.strip().split())


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
