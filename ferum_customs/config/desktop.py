# ferum_customs/config/desktop.py
from frappe import _

def get_data():
    return [
        {
            "module_name": "Ferum Customizations",  # <--- СОВПАДАЕТ с modules.txt
            "label": _("Ferum Customizations"),
            "color": "#2980b9",
            "icon": "octicon octicon-briefcase",
            "type": "module",
            "description": "Кастомные доработки для учета обслуживания и проектов.",
            "items": [
                {
                    "type": "doctype",
                    "name": "ServiceRequest",
                    "label": _("Заявки на обслуживание"),
                },
                {
                    "type": "doctype",
                    "name": "Contract",
                    "label": _("Контракты"),
                },
                {
                    "type": "doctype",
                    "name": "ServiceReport",
                    "label": _("Акты выполненных работ"),
                },
                {
                    "type": "doctype",
                    "name": "ServiceObject",
                    "label": _("Объекты обслуживания"),
                },
                {
                    "type": "doctype",
                    "name": "Project", # ВНИМАНИЕ: Если это стандартный Project, то ОК. Если кастомный - переименовать.
                    "label": _("Проекты"),
                },
                {
                    "type": "doctype",
                    "name": "PayrollEntryCustom",
                    "label": _("Расчет ЗП (Кастомный)"),
                },
                {
                    "type": "doctype",
                    "name": "PhotoAttachment",
                    "label": _("Фотофиксации"),
                },
                {
                    "type": "doctype",
                    "name": "DocumentAttachment",
                    "label": _("Прикрепленные документы"),
                },
                # Пример для вашего кастомного DocType ferumTest
                # {
                #     "type": "doctype",
                #     "name": "ferumTest",
                #     "label": _("Тестовый древовидный DocType"),
                # },
            ]
        }
    ]
