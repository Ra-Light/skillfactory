from os import system, name
import re


# матрица состояний игры
game_matrix = None
# флаг завершения игры
end_game = False


# функция инициализации игровой матрицы
def init_matrix():
    return [[' ' for x in range(1, 4)] for i in range(1, 4)]


# функция для очистки экрана
def clear():
    # for mac and linux
    if name == 'posix':
        _ = system('clear')

    else:
        # for windows
        _ = system('cls')


# функция отображения доски с ходами
def show_board(players):
    row_num = 1
    # отображаются игроки
    print(f"Игроки: {players[0]} (X), {players[1]} (0)")

    # отображаются допустимые координаты
    print(
        "Формат координат: <Строка><Разделитель><Столбец>. Допустимые разделители: ' ',';',':',',','.'. Допустимые значения координат: 1-3<Разделитель>1-3")
    print("Для прерывания игры вместо координат наберите exit.")
    print()
    for row in game_matrix:
        figures_row = f"║ {row[0]} ║ {row[1]} ║ {row[2]} ║"
        if row_num == 1:
            print("╔═══╦═══╦═══╗")  # first row
            print(figures_row)
            print("╠═══╬═══╬═══╣")
        elif row_num == 2:
            print(figures_row)
            print("╠═══╬═══╬═══╣")
        else:
            print(figures_row)
            print("╚═══╩═══╩═══╝")
        row_num += 1


# присваиваем указанной ячейке фигуру
def set_figure(entered_coords, game_matrix, current_figure):
    coords_values = re.split(r"[,| |:|;|.]+", entered_coords.strip())
    result = "OK"

    # check elements count
    if len(coords_values) != 2:
        result = f"Непонятны координаты '{entered_coords}'."
    elif len(coords_values) == 2:
        try:
            #пробуем конвертировать координаты в число
            x_coord = int(coords_values[0])
            y_coord = int(coords_values[1])
        except:
            # конвертировать не удалось
            result = f"Непонятны координаты '{entered_coords}'."

    if result == "OK":
        # проверка координат на принадлежность правильному интервалу
        if not 0 < x_coord < 4 or not 0 < y_coord < 4:
            result = f"Координаты '{entered_coords}' выходят за пределы допустимых (1-3<Разделитель>1-3)."

    if result == "OK":
        if game_matrix[x_coord - 1][y_coord - 1].strip() == '':
            # присваиваем символ ячейке
            game_matrix[x_coord - 1][y_coord - 1] = current_figure
        else:
            # ячейка уже заполнена - пишем сообщение об ошибке
            result = f"Ячейка '{entered_coords}' уже заполнена!"

    return result


# функция проверки есть ли победитель
def is_win(game_matrix, current_player_figure):

    figure_won_rows, figure_won_cols, figure_won_diagonals = False, False, False

    # проверка строк на выигрошную комбинацию
    figure_won_rows = len(list(filter(lambda x: (len(list(filter(lambda y: y == current_player_figure, x))) == 3), game_matrix))) > 0

    # проверка столбцов на выигрошную комбинацию
    for i in range(0, 3):
        if not figure_won_cols:
            figure_won_cols = len(list(filter(lambda x: x[i] == current_player_figure ,game_matrix))) == 3
        else:
            break

    # проверка диагоналей на выигрошную комбинацию
    figure_won_diagonals = (game_matrix[0][0] == current_player_figure and game_matrix[1][1] == current_player_figure and
                  game_matrix[2][2] == current_player_figure) or \
                 (game_matrix[0][2] == current_player_figure and game_matrix[1][1] == current_player_figure and
                  game_matrix[2][0] == current_player_figure)

    return figure_won_diagonals or figure_won_rows or figure_won_cols


# функция инициализации игры: создаётся новая матица, устанавливается текущий игрок как играющий еркстиками, сбрасывается флаг окончания игры
def init_game(first_player, second_player):
    global game_matrix, end_game, current_player_figure
    # инициализация матрицы состояний игры
    game_matrix = init_matrix()

    # инициализируем первую фигуру
    current_player_figure = 'X'

    # отображаем игровую доску
    show_board((first_player, second_player))

    # сбрасываем флаг завершения игры
    end_game = False



# Справка для игры
help_text = """
Приветствую игроки!
Введите свои имена перед игрой. Первым играть начинают крестики. Бросьте монетку кто будет играть крестиками ;)
Каждый игрок во время его хода вводит координаты клетки в формате "<Строка><Разделитель><Столбец>" куда он хочет ходить. 
Допустимые разделители: ' ',';',':',',','.'. Возможные оординаты: (1-3<Разделитель>1-3).
Для прерывания игры вместо координат наберите exit.
Жмите Ввод для продолжения.
"""


# отображаем справку для игры и ожидаем нажатия клавиши Ввод
input_text = input(help_text)

# Ждем имени первого игрока
first_player = input("Введите имя первого игрока (играет Х):")

while not first_player:
    first_player = input("Введите имя первого игрока (играет Х):")

# Ждём имени второго игрока
second_player = input("Введите имя второго игрока (играет 0):")

while not second_player:
    second_player = input("Введите имя второго игрока (играет 0):")

# инициализируем игру
init_game(first_player, second_player)

# флаг прерывания игры
break_game = False

while True:
    # ждём хода текущего игрока
    current_player_name = f"Ходите {first_player if current_player_figure == 'X' else second_player} ({current_player_figure})"
    coords = ''
    win = False

    while not coords:
        # считываем введённые координаты
        coords = input(current_player_name)

    # прерываем игру и выходим из программы
    if coords.lower().strip() == "exit":
        break_game = True

    if not break_game:
        # присаваиваем фигуру ячейке матрицы и возвращаем результат присвоения
        set_result = set_figure(coords, game_matrix, current_player_figure)

        while set_result != "OK":
            # введены неверные или непонятные координаты ячейки - ждём правильных координат ячейки
            coords = input(set_result + " Введите веpные координаты ячейки (формат: 1-3<Разделитель>1-3):")
            if coords.lower().strip() == "exit":
                break_game = True
                break #прерываем ввод координат
            set_result = set_figure(coords, game_matrix, current_player_figure)

    # прерываем игру и выходим из программы
    if break_game:
        print("Игра прервана!!!!")
        break

    if set_result == "OK":
        # проверяем есть ли победитель
        win = is_win(game_matrix, current_player_figure)

    # очистка экрана
    clear()
    # отображаем игровую доску с фигурами
    show_board((first_player, second_player))

    if win:
        # есть победитель - показываем его на экране и предлагаем сыграть ещё
        print(
            f"Победил игрок {first_player if current_player_figure == 'X' else second_player} ({current_player_figure})")
        end_game = True
        # сбрасфваем флаг победителя
        win = False
    else:
        # проверяем есть ли свободные ячейки
        free_cells = list(filter(lambda x: len(list(filter(lambda y: y.strip() == '', x))) > 0, game_matrix))

        if len(free_cells) == 0:
            print("Победителя нет.")
            end_game = True
        else:
            # меняем текущую фигуру игрока
            current_player_figure = '0' if current_player_figure == 'X' else 'X'

    if end_game:
        end_game = False  # сбпасываем флаг окончания игры
        new_game = input(f"Сыграете в новую партию? (Да - y/Нет - n):")

        if new_game.lower() == 'y':
            clear()
            # реинициализируем игру
            init_game(first_player, second_player)
        else:
            # выходим из игры
            print("Пока, пока!!!! До встречи на игровом поле!!!!")
            break