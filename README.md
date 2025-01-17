# DriverApp

### Приложение «драйвер» для работы с промышленным 4-х канальным источником питания со следующими возможностями:
1. Постоянный опрос телеметрии источника питания (текущее напряжение, ток, мощность по каждому каналу);
2. Логгирование телеметрии - в файл. Каждое измерение - с меткой времени;
3. Имеет команду на включение канала питания (параметры: номер канала питания, заданное напряжение, заданный ток);
4. Имеет команду на отключение канала питания(параметры: номер канала питания);
5. Имеет команду на запрос текущего состояния всех каналов питания (время измерения, значение напряжений, токов по всем каналам питания). Выходной формат - json.
6. Внешний API для программы - REST
7. Использовать asyncio
8. ПО обменивается с источником питания по tcp/ip по протоколу scpi (текстовый формат с разделителем \n). 

### Алгоритм включения канала питания. Выдать команды:
1. Задать ток для канала питания (подсистема SOURCE)
2. Задать напряжение для канала питания (подсистема SOURCE)
3. Включить выход канала питания (подсистема OUTPUT)

### Алгоритм отключения канала питания:
1. Отключить выход канала питания (подсистема OUTPUT)


### Общий конфигурационный файл
Все специфичные переменные для проекта задаются в [settings.py](app/config/settings.py)


<details>
<summary>Локальное разворачивание</summary>

### Настройка локального окружения
```sh
python3 -m venv env

source env/bin/activate

pip install -r requirements.txt
```

### Прогон через линтеры и запуск тестов
```sh
flake8 .
pytest tests/
```

### Запуск
```sh
python run.py
```

### API
```
http://0.0.0.0:8000/docs
```

#### Запустить команду из корневой директории, если появляются ошибки с отсутствием модуля
```sh
export PYTHONPATH=$(pwd)
```
</details>