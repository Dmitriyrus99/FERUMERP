# ferum_customs/config/docs.py

# Если ваша система документации ожидает эту функцию и структуру:
def get_docs_info(): # Переименовал для ясности, если это специфичная функция
    return [
        {
            # Если 'latest_module' используется как технический идентификатор модуля,
            # то он должен совпадать с именем модуля из modules.txt
            "module_name_for_docs": "Ferum Customizations", # Или 'ferum_customs' если система ожидает имя приложения
            "module_label_for_docs": "Ferum Customizations", # Для отображения
            "lists": [
                {
                    "type": "DocType",
                    "name": "ServiceRequest" # Убедитесь, что этот DocType будет документирован
                },
                {
                    "type": "DocType",
                    "name": "PhotoAttachment" # Убедитесь, что этот DocType будет документирован
                }
                # Добавьте другие DocType для документации
            ]
        }
    ]

# Стандартный способ влияния на контекст документации:
# def get_context(context):
# 	context.brand_html = "Документация по Ferum Customizations"
# 	context.docs_base_url = "/docs/user/manual/ru/ferum_customizations" # Пример
#   # context.source_link = "https://github.com/ваш_логин/ferum_customs" # Пример
