# Copyright (c) 2024, minh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ATSInstitution(Document):
	def default_list_data():
		columns = [
			{
				'label': 'Tên tổ chức',
				'type': 'Data',
				'key': 'institution_name',
				'width': '16rem'
			},
   			{
				'label': 'Địa chỉ',
				'type': 'Data',
				'key': 'location',
				'width': '16rem'
			},
			{
				'label': 'Hình thức đào tạo',
				'type': 'Select',
				'key': 'training_type',
				'width': '16rem'
			},
		]

		rows = [
			"institution_name",
   			"location",
			"training_type",
			"name"
		]
		return {'columns': columns, 'rows': rows}
