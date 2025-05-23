# ferum_customs/integrations/google_sheets.py
import frappe
from frappe import _
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES_SHEETS = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_service():
    """
    Получает аутентифицированный объект сервиса Google Sheets.
    Учетные данные читаются из site_config.json.
    """
    creds_config = frappe.conf.get("ferum_customs_credentials", {})
    google_creds_path = creds_config.get("google_service_account_json_path")

    if not google_creds_path:
        frappe.log_error(
            title=_("Ошибка конфигурации Google Sheets"),
            message=_("Путь к файлу учетных данных Google (google_service_account_json_path) " + \
                    "не настроен в site_config.json внутри 'ferum_customs_credentials'.")
        )
        frappe.throw(
            _("Конфигурация Google Sheets не завершена. Обратитесь к администратору."),
            title=_("Ошибка конфигурации")
        )

    try:
        credentials = service_account.Credentials.from_service_account_file(
            google_creds_path,
            scopes=SCOPES_SHEETS
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except FileNotFoundError:
        frappe.log_error(
            title=_("Ошибка Google Sheets: Файл учетных данных не найден"),
            message=_("Файл учетных данных Google не найден по пути: {0}. " + \
                    "Проверьте путь в site_config.json и права доступа к файлу.").format(google_creds_path)
        )
        frappe.throw(
            _("Файл учетных данных Google не найден. Проверьте конфигурацию."),
            title=_("Ошибка конфигурации")
        )
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Google Sheets Authentication Error")
        frappe.throw(
            _("Ошибка аутентификации Google Sheets: {0}").format(str(e)),
            title=_("Ошибка аутентификации")
        )

@frappe.whitelist()
def export_service_requests_to_sheet(sheet_id=None, sheet_name="Лист1"):
    """
    Экспортирует данные в Google Sheets.
    Реализуйте здесь вашу логику экспорта заявок на обслуживание.
    """
    frappe.logger().info(f"Запуск export_service_requests_to_sheet. Sheet ID: {sheet_id}, Sheet Name: {sheet_name}")

    if not sheet_id:
        # Можно получать sheet_id из настроек по умолчанию, если он не передан
        # settings = frappe.get_doc("Ferum Customs Settings") # Пример, если у вас есть DocType настроек
        # sheet_id = settings.service_requests_sheet_id
        if not sheet_id: # Если все еще нет, то ошибка
            frappe.msgprint(_("Не указан ID Google таблицы (sheet_id) для экспорта заявок."))
            return {"status": "error", "message": "Sheet ID is required for service requests export"}

    try:
        service = get_google_sheets_service()
        frappe.logger().info("Сервис Google Sheets получен успешно для экспорта заявок.")
        
        # ЗАГЛУШКА: Начало вашей логики экспорта
        # service_requests = frappe.get_all("Service Request", filters={"status": "Open"}, fields=["name", "subject", "customer", "creation"])
        # if not service_requests:
        #     frappe.msgprint(_("Нет открытых заявок для экспорта."))
        #     return {"status": "no data"}
        #
        # header_row = ["ID Заявки", "Тема", "Заказчик", "Дата создания"]
        # data_to_export = [header_row]
        # for req in service_requests:
        #     data_to_export.append([req.name, req.subject, req.customer, str(req.creation)])
        #
        # body = {'values': data_to_export}
        # range_name = f"{sheet_name}!A1"
        #
        # result = service.spreadsheets().values().update(
        #     spreadsheetId=sheet_id, range=range_name,
        #     valueInputOption="USER_ENTERED", body=body).execute()
        #
        # msg = _("Данные по заявкам успешно экспортированы. Обновлено строк: {0}").format(result.get("updatedRows"))
        # frappe.msgprint(msg)
        # frappe.logger().info(msg)
        # return {"status": "success", "updated_rows": result.get("updatedRows")}
        # ЗАГЛУШКА: Конец вашей логики экспорта

        frappe.logger().info("✅ export_service_requests_to_sheet (заглушка) выполнен успешно.")
        frappe.msgprint(_("Функция export_service_requests_to_sheet вызвана (реализуйте логику)."))
        return {"status": "placeholder executed"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Export Service Requests to Google Sheets Error")
        return {"status": "error", "message": str(e)}


def export_payroll_to_sheet(doc, method=None):
    """
    Экспортирует данные о PayrollEntry (например, при on_submit).
    Аргумент doc — это экземпляр документа PayrollEntryCustom.
    """
    frappe.logger().info(f"Запуск export_payroll_to_sheet для документа {doc.name}")

    # Пример получения ID таблицы и имени листа из настроек
    # Создайте DocType "Ferum Customs Settings" (Single) с полями:
    # payroll_export_sheet_id (Data)
    # payroll_export_sheet_name (Data)
    settings = frappe.get_cached_doc("Ferum Customs Settings") # Кэшированный вызов для Single DocType
    sheet_id = settings.get("payroll_export_sheet_id")
    sheet_name = settings.get("payroll_export_sheet_name") or "PayrollData" # Имя листа по умолчанию

    if not sheet_id:
        frappe.log_error(
            title=_("Ошибка конфигурации экспорта ЗП"),
            message=_("Не указан ID Google таблицы для экспорта ЗП в настройках 'Ferum Customs Settings'.")
        )
        return # Не прерываем сохранение документа, просто логируем

    try:
        service = get_google_sheets_service()
        frappe.logger().info(f"Сервис Google Sheets получен успешно для экспорта ЗП документа {doc.name}.")

        # ЗАГЛУШКА: Начало вашей логики экспорта данных из 'doc'
        # employee_name = doc.get("employee_name") # Используйте doc.get для безопасного доступа к полям
        # gross_pay = doc.get("gross_pay")
        # posting_date = doc.get("posting_date") or frappe.utils.nowdate()
        #
        # data_to_append = [[str(posting_date), doc.name, employee_name, gross_pay]]
        # body = {'values': data_to_append}
        # range_name = f"{sheet_name}" # Для append можно просто имя листа, данные добавятся в конец
        #
        # result = service.spreadsheets().values().append(
        #     spreadsheetId=sheet_id, range=range_name,
        #     valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body=body).execute()
        # frappe.logger().info(f"Данные по ЗП для {doc.name} добавлены в Google Sheet: {result.get('updates', {}).get('updatedRange')}")
        # ЗАГЛУШКА: Конец вашей логики экспорта
        
        frappe.logger().info(f"✅ export_payroll_to_sheet (заглушка) для {doc.name} выполнен успешно.")
        return {"status": "placeholder executed"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Export Payroll {doc.name} to Google Sheets Error")
        return {"status": "error", "message": str(e)} # Возвращаем статус для возможной обработки
