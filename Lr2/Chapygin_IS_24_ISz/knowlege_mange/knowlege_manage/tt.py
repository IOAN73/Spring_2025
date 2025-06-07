def calculate_cost(N, M, K, A, B):
    # Шаг 1: Рассчитать общее количество кубиков, необходимых для сборки сервера
    total_needed = (N * A) + (M * B)

    # Шаг 2: Вычесть количество уже имеющихся кубиков
    remaining_needed = total_needed - K

    # Шаг 3: Если кубиков хватает, покупка не требуется
    if remaining_needed <= 0:
        return 0

    # Шаг 4: Определить, сколько комплектов по 650 кубиков нужно докупить
    sets_needed = (remaining_needed + 649) // 650

    # Шаг 5: Рассчитать общую стоимость покупки
    cost = sets_needed * 30

    return cost


# Чтение входных данных
N, M = map(int, input().split())
K, A, B = map(int, input().split())

# Вычисление стоимости
result = calculate_cost(N, M, K, A, B)

# Вывод результата
print(result)

#___________________________________________________________________________________________________________ second

def format_brackets(s):
    depth = 0
    result = []

    for char in s:
        if char == '(':
            result.append(' ' * (depth * 2) + char)
            depth += 1
        elif char == ')':
            depth -= 1
            result.append(' ' * (depth * 2) + char)

    return '\n'.join(result)

# Чтение входных данных
input_string = input().strip()

# Форматирование и вывод результата
formatted_string = format_brackets(input_string)
print(formatted_string)

#______________________________________________________________________________________________________________ third

def count_divisors(n):
    """Функция для подсчета количества делителей числа n"""
    count = 0
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            count += 1
            if i != n // i:
                count += 1
    return count


def find_best_reward_index(n, rewards):
    """Функция для нахождения индекса лучшей награды"""
    max_divisors = 0
    best_index = -1
    max_elements = 0

    for i in range(n):
        reward = rewards[i]
        divisors_count = count_divisors(reward)

        if (divisors_count > max_divisors) or (divisors_count == max_divisors and reward > max_elements):
            max_divisors = divisors_count
            max_elements = reward
            best_index = i + 1

    return best_index


# Чтение входных данных
import sys

input = sys.stdin.read
data = input().split()
n = int(data[0])
rewards = list(map(int, data[1:]))

# Нахождение лучшей награды
best_index = find_best_reward_index(n, rewards)

# Вывод результата
print(best_index)