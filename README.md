# TPC

Практическое задание по курсу "Основы обработки текстов"

### Постановка задачи

Требуется реализовать алгоритм, принимающий на вход текстовый файл с НПА и возвращающий
JSON объект, содержащий извлеченные метаданные.

Алгоритм должен поддерживать следующие типы метаданных:
1. тип документа;
2. номер документа;
3. дата принятия;
4. название документа;
5. орган, принявший акт.

### Структура репозитория

- **train** - тексты для обучения;
- **Description.pdf** - подробное описание задачи;
- **eval_module.py** - скрипт для оценки качества классификации;
- **solution.py** - мое решение задачи.
