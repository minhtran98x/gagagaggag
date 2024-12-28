# Copyright (c) 2024, minh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ATS_Company(Document):
	def default_list_data():
		columns = [
			{
				'label': 'Mã công ty',
				'type': 'Data',
				'key': 'company_id',
				'width': '16rem'
			},
   			{
				'label': 'Tên công ty',
				'type': 'Data',
				'key': 'company_name',
				'width': '16rem'
			},
			{
				'label': 'Địa chỉ công ty',
				'type': 'Select',
				'key': 'company_address',
				'width': '16rem'
			},
		]

		rows = [
			"company_id",
   			"company_name",
			"company_address",
			"name"
		]
		return {'columns': columns, 'rows': rows}