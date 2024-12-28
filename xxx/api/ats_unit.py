import frappe

@frappe.whitelist()
def get_tree_data(doctype):
    data = frappe.get_all(doctype, fields=['name', 'parent_ats_unit', 'is_group'])
    return data