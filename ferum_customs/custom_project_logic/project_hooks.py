    # ferum_customs/custom_project_logic/project_hooks.py
    import frappe
    from frappe import _

    def project_validate(doc, method):
        """
        Вызывается при валидации стандартного документа Project.
        doc: экземпляр документа Project
        method: строка, указывающая на событие (например, "validate", "on_submit")
        """
        frappe.logger("ferum_customs").info(f"Запущена валидация для Project: {doc.name}, событие: {method}")
        
        # Пример валидации:
        # if doc.custom_some_critical_field and not doc.custom_another_related_field:
        #     frappe.throw(_("Если заполнено 'Критическое поле', то 'Связанное поле' также должно быть заполнено."))
        
        # if doc.project_type == "Коммерческий" and doc.get("custom_contract_value", 0) < 1000:
        #     frappe.msgprint(_("Для коммерческих проектов сумма контракта обычно больше 1000."), indicator="orange", title=_("Предупреждение"))
        pass

    def project_on_update(doc, method):
        """
        Вызывается после сохранения (создания или обновления) стандартного документа Project.
        """
        frappe.logger("ferum_customs").info(f"Документ Project обновлен: {doc.name}, событие: {method}")

        # Пример действия при обновлении:
        # if doc.status == "Completed" and not doc.custom_completion_notified:
        #     # Отправить уведомление о завершении проекта
        #     frappe.sendmail(
        #         recipients=["manager@example.com"],
        #         subject=_("Проект {0} завершен").format(doc.name),
        #         message=_("Проект {0} ({1}) был отмечен как завершенный.").format(doc.name, doc.project_name)
        #     )
        #     frappe.db.set_value("Project", doc.name, "custom_completion_notified", 1) # Чтобы не отправлять повторно
        pass

    # Вы можете добавить здесь другие функции, на которые ссылаетесь в hooks.py для Project:
    # def project_before_save(doc, method):
    #     pass
    