# %%
# -*- coding: utf-8 -*-
"""
Δ-Σ Реконструкция Арифметики Пеано: НАТУРАЛЬНЫЕ ЧИСЛА как результат применения
операторов различия (Δ) и связи (Σ). Демонстрация теорем о Δ-Σ структуре.
"""

from dataclasses import dataclass
from typing import Callable, TypeVar, Generic, Union, Any
from functools import wraps
import random

# ==================== ОСНОВНЫЕ ТИПЫ И ОПЕРАТОРЫ ====================

T = TypeVar('T')

class Void:
    """Тип, не имеющий значений (начальный объект)."""
    def __repr__(self):
        return "Void"

@dataclass(frozen=True)
class Left(Generic[T]):
    """Левая сумма (A ⊕ B) -> A."""
    value: T

@dataclass(frozen=True)
class Right(Generic[T]):
    """Правая сумма (A ⊕ B) -> B."""
    value: T

Sum = Union[Left[T], Right[T]]  # Тип суммы A ⊕ B

# ---------- ОПЕРАТОР РАЗЛИЧИЯ (Δ) ----------
def delta(x: Any, force_right: bool = False) -> Sum:
    """
    Минимальный оператор различия Δ: A → A ⊕ A.
    ВОТ ИСПРАВЛЕНИЕ: теперь delta реально различает!
    По умолчанию для Z возвращает Left, для S — Right.
    force_right можно использовать для принудительного ветвления.
    """
    if force_right:
        return Right(x)
    # Для типа Nat: Z → Left, S → Right
    if isinstance(x, Z):
        return Left(x)  # Базовый случай
    else:
        return Right(x)  # Индуктивный случай

# ---------- ОПЕРАТОР СВЯЗИ (Σ) ----------
def sigma(pair: tuple[T, T], op: Callable[[T, T], T]) -> T:
    """
    Минимальный оператор связи Σ: A × A → A.
    Для натуральных чисел — это операция следования (succ).
    """
    a, b = pair
    return op(a, b)

# ==================== ПОСТРОЕНИЕ НАТУРАЛЬНЫХ ЧИСЕЛ ====================

@dataclass(frozen=True)
class Z:
    """Ноль (Zero) — базовый конструктор."""
    def __repr__(self):
        return "Z"
    def __int__(self):
        return 0

@dataclass(frozen=True)
class S:
    """Следование (Successor) — индуктивный конструктор."""
    pred: 'Nat'
    def __repr__(self):
        return f"S({self.pred})"
    def __int__(self):
        return 1 + int(self.pred)

Nat = Union[Z, S]  # Тип натуральных чисел

# ---------- ПОМОЩНИКИ ДЛЯ СОЗДАНИЯ ЧИСЕЛ ----------
def zero() -> Nat:
    return Z()

def succ(n: Nat) -> Nat:
    return S(n)

def from_int(n: int) -> Nat:
    """Создать Nat из обычного целого."""
    if n <= 0:
        return Z()
    return S(from_int(n-1))

# ==================== Δ-Σ ДЕКОМПОЗИЦИЯ ОПЕРАЦИЙ ====================

# ---------- СЛОЖЕНИЕ ----------
def add(a: Nat, b: Nat) -> Nat:
    """
    Сложение a + b через Δ и Σ.
    Δ: ветвление на базовый случай (b = Z) и индуктивный (b = S(b_pred)).
    Σ: операция следования (succ) в индуктивном случае.
    """
    # Δ-акт: различение структуры b
    choice = delta(b)
    
    if isinstance(choice, Left):
        # Базовый случай: b = Z -> a + 0 = a
        return a
    else:
        # Индуктивный случай: b = S(b_pred) -> a + S(b) = S(a + b_pred)
        # ВОТ ИСПРАВЛЕНИЕ: нужно правильно получить b_pred
        b_pred = b.pred if isinstance(b, S) else Z()
        # Σ-акт: применение succ к результату рекурсивного вызова
        return succ(add(a, b_pred))

# ---------- УМНОЖЕНИЕ ----------
def multiply(a: Nat, b: Nat) -> Nat:
    """
    Умножение a * b как итерация сложения.
    """
    choice = delta(b)
    
    if isinstance(choice, Left):
        # a * 0 = 0
        return Z()
    else:
        # a * S(b) = a + (a * b)
        b_pred = b.pred if isinstance(b, S) else Z()
        return add(a, multiply(a, b_pred))

# ---------- ПРЕДИКАТЫ ----------
def is_zero(n: Nat) -> bool:
    """
    Предикат 'n = 0' — чистый Δ-акт.
    """
    choice = delta(n)
    return isinstance(choice, Left)

def is_even(n: Nat) -> bool:
    """
    Чётность через рекурсию.
    """
    if isinstance(n, Z):
        return True
    elif isinstance(n, S):
        if isinstance(n.pred, Z):
            return False  # 1
        else:
            # Чётность(S(S(x))) = Чётность(x)
            return is_even(n.pred.pred if isinstance(n.pred, S) else Z())
    return False

# ==================== ДЕМОНСТРАЦИЯ ====================

def demo_basic():
    """Основная демонстрация."""
    print("="*60)
    print("Δ-Σ РЕКОНСТРУКЦИЯ АРИФМЕТИКИ ПЕАНО (ИСПРАВЛЕННАЯ)")
    print("="*60)
    
    # 1. Создание чисел
    print("\n1. СОЗДАНИЕ ЧИСЕЛ:")
    numbers = [from_int(i) for i in range(5)]
    for i, n in enumerate(numbers):
        print(f"  from_int({i}) = {n}")
    
    # 2. Сложение
    print("\n2. СЛОЖЕНИЕ (Δ-Σ ДЕКОМПОЗИЦИЯ):")
    a, b = from_int(2), from_int(3)
    result = add(a, b)
    print(f"  {a} + {b} = {result}")
    print(f"  Проверка: 2 + 3 = {int(result)}")
    
    # 3. Умножение
    print("\n3. УМНОЖЕНИЕ (Δ-Σ ДЕКОМПОЗИЦИЯ):")
    result = multiply(a, b)
    print(f"  {a} * {b} = {result}")
    print(f"  Проверка: 2 * 3 = {int(result)}")
    
    # 4. Предикаты
    print("\n4. ПРЕДИКАТЫ (ЧИСТЫЕ Δ-АКТЫ):")
    for i in range(4):
        n = from_int(i)
        print(f"  is_zero({i}) = {is_zero(n)} | is_even({i}) = {is_even(n)}")

def demo_recursion_depth():
    """Демонстрация рекурсивной природы."""
    print("\n" + "="*60)
    print("РЕКУРСИВНАЯ СТРУКТУРА ОПЕРАЦИЙ")
    print("="*60)
    
    def trace_add(a: Nat, b: Nat, depth: int = 0) -> Nat:
        """Версия add с трассировкой."""
        indent = "  " * depth
        print(f"{indent}add({a}, {b}) [глубина: {depth}]")
        
        choice = delta(b)
        if isinstance(choice, Left):
            print(f"{indent}Δ: базовый случай -> возвращаем {a}")
            return a
        else:
            b_pred = b.pred if isinstance(b, S) else Z()
            print(f"{indent}Δ: индуктивный случай -> рекурсия")
            print(f"{indent}Σ: применяем succ к результату")
            intermediate = trace_add(a, b_pred, depth + 1)
            result = succ(intermediate)
            print(f"{indent}Результат уровня {depth}: {result}")
            return result
    
    print("\nТрассировка 2 + 3:")
    a, b = from_int(2), from_int(3)
    result = trace_add(a, b)
    print(f"\nИтог: {a} + {b} = {result} = {int(result)}")

def demo_structural_analysis():
    """Анализ структуры через Δ."""
    print("\n" + "="*60)
    print("СТРУКТУРНЫЙ АНАЛИЗ ЧЕРЕЗ Δ")
    print("="*60)
    
    for i in range(4):
        n = from_int(i)
        choice = delta(n)
        
        if isinstance(choice, Left):
            print(f"Δ({i} = {n}) → Left (это Z или базовый случай)")
        else:
            print(f"Δ({i} = {n}) → Right (это S или индуктивный случай)")
            
            # Можно анализировать дальше
            if isinstance(n, S):
                sub_choice = delta(n.pred)
                if isinstance(sub_choice, Left):
                    print(f"  Δ({n.pred}) → Left (предшественник — Z)")
                else:
                    print(f"  Δ({n.pred}) → Right (предшественник — S)")

def main():
    """Основная функция."""
    demo_basic()
    demo_recursion_depth()
    demo_structural_analysis()
    
    # Теоретический вывод
    print("\n" + "="*60)
    print("ТЕОРЕТИЧЕСКИЕ ВЫВОДЫ")
    print("="*60)
    print("""
    1. КОРРЕКТНАЯ РАБОТА Δ:
       - Δ(Z) → Left  (базовый случай)
       - Δ(S(n)) → Right (индуктивный случай)
       
    2. РЕКУРСИВНАЯ СТРУКТУРА:
       - Сложение: Δ-ветвление + Σ(succ)-композиция
       - Умножение: итерация сложения (второй уровень)
       
    3. МИНИМАЛЬНОСТЬ:
       - Все операции сводятся к композициям Δ и Σ
       - Удаление Δ уничтожает ветвление
       - Удаление Σ уничтожает композицию/рекурсию
       
    4. ВЕРИФИКАЦИЯ:
       - 2 + 3 = 5 ✓
       - 2 * 3 = 6 ✓
       - is_zero корректен ✓
    """)

if __name__ == "__main__":
    main()


