# ferum_customs/integrations/google_drive.py
import frappe
from frappe import _
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import mimetypes
import os

SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']
DEFAULT_DRIVE_PHOTO_FOLDER_NAME = "Service Photos" 

def get_google_drive_service():
    """
    Получает аутентифицированный объект сервиса Google Drive.
    Учетные данные читаются из site_config.json.
    """
    creds_config = frappe.conf.get("ferum_customs_credentials", {})
    google_creds_path = creds_config.get("google_service_account_json_path")

    if not google_creds_path:
        frappe.log_error(
            title=_("Ошибка конфигурации Google Drive"),
            message=_("Путь к файлу учетных данных Google (google_service_account_json_path) " + \
                    "не настроен в site_config.json внутри 'ferum_customs_credentials'.")
        )
        frappe.throw(
            _("Конфигурация Google Drive не завершена. Обратитесь к администратору."),
            title=_("Ошибка конфигурации")
        )
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            google_creds_path, 
            scopes=SCOPES_DRIVE
        )
        service = build('drive', 'v3', credentials=credentials)
        return service
    except FileNotFoundError:
        frappe.log_error(
            title=_("Ошибка Google Drive: Файл учетных данных не найден"),
            message=_("Файл учетных данных Google не найден по пути: {0}. " + \
                    "Проверьте путь в site_config.json и права доступа к файлу.").format(google_creds_path)
        )
        frappe.throw(
            _("Файл учетных данных Google не найден. Проверьте конфигурацию."),
            title=_("Ошибка конфигурации")
        )
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Google Drive Authentication Error")
        frappe.throw(
            _("Ошибка аутентификации Google Drive: {0}").format(str(e)),
            title=_("Ошибка аутентификации")
        )

def get_drive_folder_id(folder_name, parent_folder_id=None, create_if_not_exists=False):
    """
    Находит ID папки на Google Drive по имени.
    Если parent_folder_id указан, ищет внутри этой родительской папки.
    Если create_if_not_exists=True, создает папку, если она не найдена.
    Возвращает ID папки или None.
    """
    service = get_google_drive_service()
    
    # Экранируем одинарные кавычки в имени папки для безопасности запроса
    safe_folder_name = folder_name.replace("'", "\\'")
    query = f"name = '{safe_folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"
    # else: # Поиск в корне диска сервисного аккаунта (если parent_folder_id не указан)
          # Если нужно искать в общем "My Drive" пользователя, а не сервисного аккаунта,
          # потребуется другой подход или указание ID корневой папки "My Drive"
          # query += f" and 'root' in parents" # Для сервисного аккаунта это обычно его собственный корень

    try:
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            corpora='user' # Искать в файлах пользователя (сервисного аккаунта)
        ).execute()
        files = response.get('files', [])
        
        if files:
            return files[0].get('id')
        elif create_if_not_exists:
            frappe.logger().info(f"Папка '{folder_name}' не найдена на Google Drive, создаем новую.")
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
            
            folder = service.files().create(body=file_metadata, fields='id').execute()
            frappe.logger().info(f"Папка '{folder_name}' создана с ID: {folder.get('id')}")
            return folder.get('id')
        else:
            frappe.logger().info(f"Папка '{folder_name}' не найдена на Google Drive.")
            return None
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Error finding/creating folder '{folder_name}' on Google Drive")
        return None


@frappe.whitelist()
def upload_photo_to_drive(file_doc_name, target_folder_name=None, drive_parent_folder_id=None):
    """
    Загружает файл из Frappe DocType "File" в указанную папку на Google Drive.
    Args:
        file_doc_name (str): Имя документа "File" в Frappe.
        target_folder_name (str, optional): Имя целевой папки на Google Drive.
                                            Если не указано, используется DEFAULT_DRIVE_PHOTO_FOLDER_NAME.
        drive_parent_folder_id (str, optional): ID родительской папки на Google Drive, внутри которой
                                                искать/создавать target_folder_name. Если None,
                                                поиск/создание будет в корне диска сервисного аккаунта.
    """
    service = get_google_drive_service()

    if not frappe.db.exists("File", file_doc_name):
        msg = _("Файл с именем {0} не найден в системе.").format(file_doc_name)
        frappe.msgprint(msg)
        return {"status": "error", "message": msg}

    file_doc = frappe.get_doc("File", file_doc_name)
    
    # Получаем локальный путь к файлу. Важно, чтобы файл был доступен на сервере.
    # Если файл приватный, get_local_path() может не сработать без дополнительных настроек.
    # Для публичных файлов это обычно frappe-bench/sites/имя_сайта/public/files/имя_файла
    # Для приватных файлов путь будет другим.
    if file_doc.is_private:
        file_path = file_doc.get_full_path() # Попытка получить полный путь для приватных файлов
    else:
        file_path = os.path.join(frappe.get_site_path("public", "files"), file_doc.file_name)

    if not os.path.exists(file_path):
        # Дополнительная проверка, если get_local_path или get_full_path не вернули ожидаемый результат
        # или если файл был удален с диска, но запись в DocType File осталась.
        alt_file_path = os.path.abspath(os.path.join(frappe.get_site_path(), file_doc.file_url.lstrip('/')))
        if os.path.exists(alt_file_path):
            file_path = alt_file_path
        else:
            msg = _("Локальный файл для документа File {0} не найден по пути: {1} или {2}").format(file_doc_name, file_path, alt_file_path)
            frappe.log_error(msg, "Google Drive Upload Error")
            return {"status": "error", "message": msg}


    filename = file_doc.file_name # Имя файла для Google Drive

    if not target_folder_name:
        target_folder_name = DEFAULT_DRIVE_PHOTO_FOLDER_NAME
    
    # Получаем ID целевой папки
    app_target_folder_id = get_drive_folder_id(target_folder_name, 
                                               parent_folder_id=drive_parent_folder_id, 
                                               create_if_not_exists=True)

    if not app_target_folder_id:
        msg = _("Не удалось найти или создать папку '{0}' на Google Drive.").format(target_folder_name)
        frappe.log_error(msg, "Google Drive Upload Error")
        return {"status": "error", "message": msg}

    mime_type, _ = mimetypes.guess_type(filename) # Определяем MIME по имени файла (более надежно)
    if not mime_type:
        mime_type = 'application/octet-stream'

    file_metadata = {
        'name': filename,
        'parents': [app_target_folder_id]
    }
    
    try:
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        
        gdrive_file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id, name, webViewLink, webContentLink'
        ).execute()
        
        success_msg = _("Файл '{0}' успешно загружен в папку '{1}' на Google Drive. Ссылка: {2}").format(
            filename, target_folder_name, gdrive_file.get('webViewLink')
        )
        frappe.logger().info(success_msg, "Google Drive Upload")
        frappe.msgprint(success_msg)
        
        return {
            "status": "success",
            "gdrive_id": gdrive_file.get('id'),
            "gdrive_name": gdrive_file.get('name'),
            "webViewLink": gdrive_file.get('webViewLink'),
            "webContentLink": gdrive_file.get('webContentLink')
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Google Drive Upload Error")
        return {"status": "error", "message": str(e)}
