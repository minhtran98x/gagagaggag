# Copyright (c) 2024, xxx and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _
from frappe.model.document import Document


class xxxFieldsLayout(Document):
	pass
@frappe.whitelist()
def get_fields_layout(doctype: str, type: str):
	print("Test log get_fields_layout doctype :  ", doctype)
	print("Test log get_fields_layout type :  ", type)
	sections = []
	if frappe.db.exists("xxx Fields Layout", {"dt": doctype, "type": type}):
		layout = frappe.get_doc("xxx Fields Layout", {"dt": doctype, "type": type})
	else:
		return []

	if layout.layout:
		sections = json.loads(layout.layout)

	allowed_fields = []
	for section in sections:
		if not section.get("fields"):
			continue
		allowed_fields.extend(section.get("fields"))

	fields = frappe.get_meta(doctype).fields
	fields = [field for field in fields if field.fieldname in allowed_fields]

	for section in sections:
		for field in section.get("fields") if section.get("fields") else []:
			field = next((f for f in fields if f.fieldname == field), None)
			if field:
				if field.fieldtype == "Select" and field.options:
					field.options = field.options.split("\n")
					field.options = [{"label": _(option), "value": option} for option in field.options]
					field.options.insert(0, {"label": "", "value": ""})
				field = {
					"label": _(field.label),
					"name": field.fieldname,
					"type": field.fieldtype,
					"options": field.options,
					"mandatory": field.reqd,
					"placeholder": field.get("placeholder"),
					"filters": field.get("link_filters")
				}
				section["fields"][section.get("fields").index(field["name"])] = field
	print("Test log get_fields_layout sections 2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:  ", sections)
	return sections or []


@frappe.whitelist()
def save_fields_layout(doctype: str, type: str, layout: str):
	if frappe.db.exists("xxx Fields Layout", {"dt": doctype, "type": type}):
		doc = frappe.get_doc("xxx Fields Layout", {"dt": doctype, "type": type})
	else:
		doc = frappe.new_doc("xxx Fields Layout")

	doc.update({
		"dt": doctype,
		"type": type,
		"layout": layout,
	})
	doc.save(ignore_permissions=True)

	return doc.layout