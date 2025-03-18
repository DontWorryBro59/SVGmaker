import os
import time
import logging

log = logging.getLogger(name='svg_maker')


# Декоратор для красивого вывода функции
def make_look_cute(func):
    def wrapper(*args, **kwargs):
        log.info('*' * 100)
        result = func(*args, **kwargs)
        log.info('*' * 100)
        return result

    return wrapper


@make_look_cute
def read_cfg():
    max_len_org = 35
    max_len_fio = 20
    directory_to_save = 'svg_files/'
    log.info('Читаем файл config.cfg')
    try:
        with open('config.cfg', 'r') as file:
            data_cfg = file.read().split('\n')
    except FileNotFoundError:
        log.error('Файл config.cfg не найден')
        return max_len_org, max_len_fio, directory_to_save

    try:
        max_len_org = int(data_cfg[0].split('=')[1])
        max_len_fio = int(data_cfg[1].split('=')[1])
        directory_to_save = data_cfg[2].split('=')[1]
        if directory_to_save[-1] != '/':
            directory_to_save += '/'
    except ValueError:
        log.error('Неверный формат данных в файле config.cfg')
        return max_len_org, max_len_fio, directory_to_save
    log.info('Файл прочитан конфигурация взята из файла config.cfg')
    return max_len_org, max_len_fio, directory_to_save


def read_def_svg():
    """
    Reads the default SVG pattern from a file named 'default_pattern.svg'.
    """
    with open('default_ pattern.svg', 'r', encoding='utf-8') as file:
        data = file.read()
        return data


@make_look_cute
def read_input_data() -> list:
    """
    Reads input data from a file named 'input_data.txt'.
    """
    log.info('Читаем файл input_data.txt')
    lines = []
    with open('input_data.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if line == '\n':
                continue
            line = line.replace('\n', '')
            line = line.strip()
            line = line.split('/')
            if len(line) < 3:
                print(f'Неверный формат данных в строке {line}')
                continue
            lines.append(line)
    log.info('Файл прочитан')
    return lines


def split_string(s, max_length) -> list:
    """
    Split string for 3 lines
    """
    words = s.split()
    lines = []
    current_line = ''
    for word in words:
        if len(current_line + ' ' + word) <= max_length:
            current_line += ' ' + word
        else:
            lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
    return lines


@make_look_cute
def create_svg_data(list_of_data: list) -> list[dict]:
    log.info('Создаем данные для SVG-файлов')
    data_list = []
    for line in list_of_data:
        # Создаем переменные для хранения данных сотрудника и имя для SVG-файла
        organization = line[0].strip()
        family, name, patronymic = line[1].split()
        # Проверяем, что фамилия, имя и отчество не слишком длинные
        for el in line[1].split():
            if len(el) > MAX_LEN_FIO:
                log.error(f'Слишком длинное имя для {file_name[:-4]}')
                continue
        file_name = f'{family}_{name}_{patronymic}.svg'
        post = line[2]
        data_to_svg = []
        log.info(f'Обрабатываем данные для {file_name[:-4]}')
        # Разбиваем название организации на 1-3 строки, если оно слишком длинное
        organization = split_string(organization, MAX_LEN_ORG)
        if len(organization) > 3:
            log.error(f'Слишком длинная организация для {file_name[:-4]}')
            continue
        # Добавляем данные организации в список data_to_svg
        if len(organization) == 1:
            data_to_svg.append(
                f'<text x="900" y="160"  class="fil0 fnt0" text-anchor="middle">{organization[0]}</text>')
        if len(organization) == 2:
            data_to_svg.append(
                f'<text x="900" y="120"  class="fil0 fnt0" text-anchor="middle">{organization[0]}</text>')
            data_to_svg.append(
                f'<text x="900" y="180"  class="fil0 fnt0" text-anchor="middle">{organization[1]}</text>')
        if len(organization) == 3:
            data_to_svg.append(f'<text x="900" y="90"  class="fil0 fnt0" text-anchor="middle">{organization[0]}</text>')
            data_to_svg.append(
                f'<text x="900" y="145"  class="fil0 fnt0" text-anchor="middle">{organization[1]}</text>')
            data_to_svg.append(
                f'<text x="900" y="202"  class="fil0 fnt0" text-anchor="middle">{organization[2]}</text>')
        # Добавляем данные ФИО в список data_to_svg
        data_to_svg.append(f'<text x="900" y="300"  class="fil0 fnt1" text-anchor="middle">{family}</text>')
        data_to_svg.append(f'<text x="900" y="376"  class="fil0 fnt1" text-anchor="middle">{name}</text>')
        data_to_svg.append(f'<text x="900" y="452"  class="fil0 fnt1" text-anchor="middle">{patronymic}</text>')
        # Разбиваем должность на 1-2 строки, если она слишком длинная
        post = split_string(post, MAX_LEN_FIO)
        if len(post) > 2:
            log.error(f'Слишком длинная должность для {file_name[:-4]}')
            continue
        # Добавляем данные должности в список data_to_svg
        if len(post) == 1:
            data_to_svg.append(f'<text x="900" y="560"  class="fil0 fnt0" text-anchor="middle">{post[0]}</text>')
        if len(post) == 2:
            data_to_svg.append(f'<text x="900" y="530"  class="fil0 fnt0" text-anchor="middle">{post[0]}</text>')
            data_to_svg.append(f'<text x="900" y="590"  class="fil0 fnt0" text-anchor="middle">{post[1]}</text>')

        # Записываем данные в словарь data_list для дальнейшей обработки
        data_list.append({'file_name': file_name, 'data_to_svg': data_to_svg})
    log.info('Данные для SVG-файлов созданы')
    return data_list


@make_look_cute
def create_svg(data_list: list[dict]) -> None:
    """
    Creates SVG files for each employee in the data_list.
    """
    log.info('Создаем SVG-файлы для каждого сотрудника из списка')
    log.info('Создаем директорию для сохранения файлов, если она не существует')
    if not os.path.exists(directory_to_save):
        os.mkdir(directory_to_save)

    default_svg = read_def_svg()
    for data in data_list:
        data_to_replace = '\n'.join(data['data_to_svg'])
        new_svg = default_svg.replace('information_to_add', data_to_replace)
        with open(f'{directory_to_save}{data["file_name"]}', 'w', encoding='utf-8') as file:
            file.write(new_svg)
    log.info('SVG-файлы созданы')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # Читаем файл config.cfg и получаем параметры для работы приложения
    MAX_LEN_ORG, MAX_LEN_FIO, directory_to_save = read_cfg()
    # Читаем файл input_data.txt и получаем список с данными
    list_with_input = read_input_data()
    # Создаем файлы svg для каждого сотрудника из списка
    data_list = create_svg_data(list_with_input)
    # Создаем SVG-файлы для каждого сотрудника из списка
    create_svg(data_list)
    log.info('Приложение завершило работу')
    log.info('TIMESLEEP = 100 seconds')
    log.info('*'*100)
    time.sleep(100)
