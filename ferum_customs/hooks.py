# ferum_customs/hooks.py

app_name = "ferum_customs"
app_title = "Ferum Customizations"
app_publisher = "ООО ФЕРУМ СБ"
app_description = "Кастомизация ERP для управления проектами и заявками на обслуживание"
app_email = "support@ferumrus.ru"
app_license = "mit"
app_icon = "octicon octicon-briefcase"
app_color = "#2980b9"
app_version = "0.1.0"

# Фикстуры для экспорта кастомизаций (включая кастомные поля для стандартных DocTypes)
# Если вы будете добавлять кастомные поля к стандартному DocType "Project"
# и при создании этих полей в "Customize Form" будете указывать "Module" = "Ferum Customizations",
# то эти строки помогут экспортировать их в ваше приложение.
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Ferum Customizations"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Ferum Customizations"]]},
    # Если вы хотите экспортировать ВСЕ кастомные поля для "Project", независимо от указанного модуля:
    # {"dt": "Custom Field", "filters": [["dt", "=", "Project"]]},
    # {"dt": "Property Setter", "filters": [["doc_type", "=", "Project"]]}
]

# События DocType
doc_events = {
    "PayrollEntryCustom": {
        "on_submit": "ferum_customs.integrations.google_sheets.export_payroll_to_sheet"
    },
    "Project": { # <--- ДОБАВЛЕНО/ИЗМЕНЕНО: Хуки для стандартного DocType "Project"
        "validate": "ferum_customs.custom_project_logic.project_validate",
        "on_update": "ferum_customs.custom_project_logic.project_on_update",
        # "before_save": "ferum_customs.custom_project_logic.project_before_save",
        # "on_submit": "ferum_customs.custom_project_logic.project_on_submit", # Если Project submittable и вы хотите это использовать
        # "on_cancel": "ferum_customs.custom_project_logic.project_on_cancel", # Если Project submittable
    }
    # ... другие ваши doc_events, если есть ...
}

# Задачи планировщика
scheduler_events = {
    "daily": [
        "ferum_customs.integrations.google_sheets.export_service_requests_to_sheet"
    ],
}

# Остальные хуки (commands, website_route_rules и т.д.) остаются как были или добавляются по необходимости.
# export_python_type_annotations = True # Раскомментируйте, если используете
