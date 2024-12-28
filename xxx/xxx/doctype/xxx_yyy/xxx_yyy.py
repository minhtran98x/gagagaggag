# Copyright (c) 2024, xxx and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class xxx_yyy(Document):
	def default_list_data():
		columns = [
			{
				'label': 'Họ và Tên',
				'type': 'Data',
				'key': 'ho_va_ten',
				'width': '16rem'
			},
   			{
				'label': 'Kiểu check',
				'type': 'Check',
				'key': 'kieu_check',
				'width': '16rem'
			},
			{
				'label': 'Kiểu datetime',
				'type': 'Datetime',
				'key': 'kieu_datetime',
				'width': '16rem'
			},
		]

		rows = [
			"ho_va_ten",
   			"kieu_check",
			"kieu_datetime",
			"name"
		]
		return {'columns': columns, 'rows': rows}
