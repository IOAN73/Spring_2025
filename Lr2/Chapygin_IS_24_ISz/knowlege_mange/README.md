# Knowlege Manage

## Запуск проекта

### с использованием pip и venv

#### Клонирование проекта

```shell
git clone https://github.com/IOAN73/knowlege_mange.git
```

#### Перейти в папку проекта

```shell
cd knowlege_mange
```

#### Создать виртуальное окружение

```shell
python -m venv .venv
```

#### Активировать виртуальное окружение 

```shell
.\.venv\Scripts\activate
```

#### Поставить требуемые библиотеки

```shell
pip install -r .\requirements.txt
```

#### Установить *PYTHONPATH*

```shell
set PYTHONPATH=<Диск:\путь\до\папки\проекта>
```

#### Запустить

```shell
python knowlege_manage/main.py
```