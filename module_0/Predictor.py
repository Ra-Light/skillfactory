import numpy as np


def find_sub_range(number_to_predict, range_start, range_end,
                   ranges_count=2):
    """Разбивает интервал на суб интервалы и ищет какому из них принадлежит числою
    Найденый интервал возвращается как результат работы"""

    # вычмсляем длину субинтервалa
    sub_range_len = (range_end - range_start) // ranges_count

    # генерируем суб интервалы
    sub_ranges = [(range_start + i * sub_range_len,
                   range_start + i * sub_range_len + sub_range_len
                       if i < (ranges_count - 1) else range_end)
                  for i in range(0, ranges_count)]

    # ищем интервал, которому принадлежит угадываемое число
    found_sub_range = list(filter(lambda x: x[0] <= number_to_predict <= x[1], sub_ranges))

    return found_sub_range


def game_core_v3(number_to_predict, range_start=1, range_end=100,
                 ranges_count=2):
    """Угадывает число с минимальным количеством ходов"""

    # инициализируем переменную с количеством попыток
    tries_count = 1

    # ищем первый субинтерва, которому принадлежит число
    found_sub_range = find_sub_range(number_to_predict,
                                     range_start, range_end, ranges_count)

    # начало и конец предыдущего интервала в цикле
    prev_range_start = 0
    prev_range_end = 0

    # ищем последующие интервалы
    while (found_sub_range[0][1] - found_sub_range[0][0]) > 1 and \
            (prev_range_start != found_sub_range[0][0] and prev_range_end != found_sub_range[0][1]):
        # найден субинтервал в предыдущем интервале, которому принадлежит угадываемое число
        found_sub_range = find_sub_range(number_to_predict,
                                         found_sub_range[0][0], found_sub_range[0][1], ranges_count)

        # интервале увеличиваем число попыток
        tries_count += 1

        # интервале запоминаем текущий найденный интервал
        prev_range_start = found_sub_range[0][0]
        prev_range_end = found_sub_range[0][1]

    found_number = -1

    # ищем в последнем найденом субинтервале угадываемое число
    for number in range(found_sub_range[0][0], found_sub_range[0][1] + 1):
        tries_count += 1
        if number == number_to_predict: # число найдено - прерываем цикл
            found_number = number
            break

    # возвращаем найденное число и количество попыток
    return found_number, tries_count


def score_game(game_core, range_start=1, range_end=100, ranges_count=2):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число"""
    count_ls = []
    tried_numbers = []

    # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    np.random.seed(1)
    random_array = np.random.randint(range_start, range_end + 1, size=1000)

    for number in random_array:
        # ищем число
        prediction_result = game_core(number, range_start, range_end, ranges_count)
        # запоминаем сгенерированное и угаданное числа
        predicted_numbers = (number, prediction_result[0])
        tried_numbers.append(predicted_numbers)

        # запоминаем количество попыток
        count_ls.append(prediction_result[1])

    # вычисляем среднее значение попыток
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток. Количество подинтервалов: {ranges_count}")
    print("Найдено элементов, где угаданное число не совпадает со случайно сгенерированным (должно быть ноль "
          "элементов): " +
          str(list(filter(lambda x: x[0] != x[1],tried_numbers))))
    return score


# массив с количеством интервалов и попыток
ranges_and_tries = []

# перебираем количество интервалов от одного до ста
# и вычисляем количество попыток
for ranges_count in range(1, 101):
    ranges_and_tries.append((ranges_count, score_game(game_core_v3, range_end=100, ranges_count=ranges_count)))


# ищем запись с минимальным значением попыток
min_tries = list(sorted(ranges_and_tries,key= lambda x: x[1]))[0]

# отображаем минимальное количество попыток и интервалов
print(f"Минимальное число средних попыток ({min_tries[1]}) достигнуто "
      f"при разбиении всего интервала на {min_tries[0]} интервалов")