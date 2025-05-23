# ferum_customs/commands/__init__.py
import frappe
from frappe.utils import cint # Для безопасного преобразования в integer, если нужно

# Важно: Убедитесь, что функции в google_sheets.py принимают аргумент sheet_key/sheet_id
# или что вы здесь передаете все необходимые параметры.

# Если ваши функции в google_sheets.py ожидают sheet_id, а не sheet_key,
# вам нужно либо изменить эти команды, либо функции в google_sheets.py,
# либо иметь механизм для получения sheet_id из sheet_key (например, из настроек).

# Пример, если export_service_requests_to_sheet ожидает sheet_id:
def export_service_requests(sheet_id=None): # Переименовал аргумент для ясности
    """
    Команда для экспорта заявок на обслуживание в Google Sheets.
    Вызывается как: bench --site ваш_сайт execute ferum_customs.commands.export_service_requests --kwargs '{"sheet_id": "ID_ВАШЕЙ_ТАБЛИЦЫ"}'
    """
    # Если sheet_id не передан через --kwargs, можно попытаться взять его из настроек
    if not sheet_id:
        settings = frappe.get_cached_doc("Ferum Customs Settings") # Пример
        sheet_id = settings.get("service_requests_sheet_id")
        if not sheet_id:
            print("Ошибка: ID таблицы Google Sheets (sheet_id) не указан и не найден в настройках.")
            return

    from ferum_customs.integrations import google_sheets # Импортируем модуль
    print(f"Запуск экспорта заявок на обслуживание в таблицу с ID: {sheet_id}")
    result = google_sheets.export_service_requests_to_sheet(sheet_id=sheet_id)
    print(f"Результат экспорта заявок: {result}")


# Для export_payroll функция в google_sheets.py уже принимает 'doc' и 'method',
# что подходит для doc_events, но не для прямой команды bench без конкретного документа.
# Если нужна команда bench для экспорта всех PayrollEntryCustom, логика будет другой.
# Эта команда, как она есть, не очень подходит для вызова через bench execute без контекста документа.

# def export_payroll(some_filter_criteria=None):
#     """
#     Команда для экспорта данных по ЗП (например, всех за определенный период).
#     Требует доработки логики в google_sheets.export_payroll_to_sheet
#     или создания новой функции для пакетного экспорта.
#     """
#     print(f"Запуск экспорта данных по ЗП. Критерии: {some_filter_criteria}")
#     # from ferum_customs.integrations import google_sheets
#     # google_sheets.batch_export_payroll_data(criteria=some_filter_criteria) # Пример вызова
#     print("Функционал экспорта ЗП через команду bench требует дополнительной реализации.")


# Если вы хотите, чтобы эти команды были доступны через `bench ferum_customs <command_name>`,
# их нужно зарегистрировать в `hooks.py` в секции `commands`.
# Например:
# commands = {
#    "export-services": "ferum_customs.commands.export_service_requests"
# }
# И вызывать: bench --site ваш_сайт ferum_customs export-services --sheet_id "ID_ТАБЛИЦЫ"
