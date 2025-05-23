import frappe
from frappe.tests.utils import FrappeTestCase

class TestServiceObject(FrappeTestCase):
	def setUp(self):
		# Здесь можно подготовить данные для тестов, если необходимо
		pass

	def tearDown(self):
		# Здесь можно очистить данные после тестов, если необходимо
		# frappe.db.rollback() # Откатить транзакцию, если тесты что-то пишут в БД

	def test_create_service_object(self):

		# Пример теста на создание
		object_name = "Тестовый Объект Сервиса 123"
		if frappe.db.exists("ServiceObject", {"object_name_address": object_name}):
			frappe.delete_doc("ServiceObject", object_name, ignore_permissions=True)

		doc = frappe.new_doc("ServiceObject")
		doc.object_name_address = object_name
		doc.object_type = "Офис"
		# Заполните другие обязательные поля, если они есть
		
		doc.insert(ignore_permissions=True) # ignore_permissions может быть нужен в тестах
		
		self.assertTrue(frappe.db.exists("ServiceObject", doc.name))
		self.assertEqual(doc.object_name_address, object_name)

	# Добавьте другие тесты для валидации, кастомных методов и т.д.
