# SVGmaker - это скрипт позволяющий создавать растровые изображения для печати

### Проблема: 
Есть небольшой бизнес по созданию бейджиков с помощью лазерного станка.
Заявки поступают из маркетплейса Озон. 
Человеку приходилось вручную переносить данные в SVG-шаблоны.
Требуется автоматизация данного процесса

### Задача
- Требуется отредактировать исходный SVG макет для дальнейшего использования
- Необходимо читать данные из файла и вносить их в SVG макет
- Для каждого человека создавать отдельный SVG файл.
  
Данные людей записываются в текстовый документ в формате компания/ФИО/должность
Реализован скрипт для чтения данных, проверки данных и создания SVG файлов.
Написана функция для разбития данных на 1, 2 или 3 строки (организация) и
1 или 2 строки (должность)

стек: скрипт написан на базовых библиотеках Python

# Инструкция по использованию скрипта

Для работы скрипта необходимо 4 файла
*** default_pattern.svg 
  Отвечает за базовый шаблон SVG файла. Обратите внимание, в нем есть строчка "information_to_add". 
  Именно по этой строчки скрипт ориентируется куда добавлять файл

*** input_data.txt 
  Отвечает за входящие данные. Отсюда скрипт берет организацию/ФИО/должность
  Обратите внимание на пример входящих данных, данные должны быть строго разделены знаком '/'
  Благодаря этому скрипт делит строку на входные данные

*** config.cfg
  Первые три строчки отвечают за настройки скрипта
# Кофигурация подтягивается из файла пример входных данных
    MAX_LEN_ORG - рекомендуемая длина от 20 до 35
    MAX_LEN_FIO - рекомендуемая длина от 15 до 25
    directory_to_save - папка куда будут сохранены файлы в текущей директории
  Если данные указаны некорректно, будут использоваться стандартные настройки файла

*** svgmaker-script.exe
  Исполняющий файл. После его выполнения будет создана папка с SVG файлами

для компиляции исполняющего файла для других систем (MACOS, linux)
скачайте исходный код с репозитория:

## запустите две команды из директории файла scgmaker-script.py
    pip install pyinstaller
    pyinstaller --onefile your_script.py
