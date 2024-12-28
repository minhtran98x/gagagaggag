import json

from bs4 import BeautifulSoup
import frappe
from frappe import _
from frappe.utils.caching import redis_cache
from frappe.desk.form.load import get_docinfo

@frappe.whitelist()
def get_activities(name):
		if frappe.db.exists("xxx_yyy", name):
			return get_xxx_yyy_activities(name,"xxx_yyy")
		if frappe.db.exists("ATS-Institution", name):
			return get_ats_institution_activities(name,"ATS-Institution")
		else:
			frappe.throw(_("Document not found"), frappe.DoesNotExistError)
  
def get_xxx_yyy_activities(name,doctype_param):
	get_docinfo('',doctype_param, name)
	docinfo = frappe.response["docinfo"]
	lead_meta = frappe.get_meta(doctype_param)
	lead_fields = {field.fieldname: {"label": field.label, "options": field.options} for field in lead_meta.fields}
	avoid_fields = [
		# "converted",
		# "response_by",
		# "sla_creation",
		# "sla",
		"name",
		"first_response_time",
		"first_responded_on",
	]

	doc = frappe.db.get_values(doctype_param, name, ["creation", "owner"])[0]
	activities = [{
		"activity_type": "creation",
		"creation": doc[0],
		"owner": doc[1],
		"data": "created this yyy",
		"is_lead": True,
	}]

	docinfo.versions.reverse()

	for version in docinfo.versions:
		data = json.loads(version.data)
		if not data.get("changed"):
			continue

		if change := data.get("changed")[0]:
			field = lead_fields.get(change[0], None)

			if not field or change[0] in avoid_fields or (not change[1] and not change[2]):
				continue

			field_label = field.get("label") or change[0]
			field_option = field.get("options") or None

			activity_type = "changed"
			data = {
				"field": change[0],
				"field_label": field_label,
				"old_value": change[1],
				"value": change[2],
			}

			if not change[1] and change[2]:
				activity_type = "added"
				data = {
					"field": change[0],
					"field_label": field_label,
					"value": change[2],
				}
			elif change[1] and not change[2]:
				activity_type = "removed"
				data = {
					"field": change[0],
					"field_label": field_label,
					"value": change[1],
				}

		activity = {
			"activity_type": activity_type,
			"creation": version.creation,
			"owner": version.owner,
			"data": data,
			"is_lead": True,
			"options": field_option,
		}
		activities.append(activity)

	for comment in docinfo.comments:
		activity = {
			"name": comment.name,
			"activity_type": "comment",
			"creation": comment.creation,
			"owner": comment.owner,
			"content": comment.content,
			"attachments": get_attachments('Comment', comment.name),
			"is_lead": True,
		}
		activities.append(activity)

	# for communication in docinfo.communications + docinfo.automated_messages:
	# 	activity = {
	# 		"activity_type": "communication",
	# 		"communication_type": communication.communication_type,
	# 		"creation": communication.creation,
	# 		"data": {
	# 			"subject": communication.subject,
	# 			"content": communication.content,
	# 			"sender_full_name": communication.sender_full_name,
	# 			"sender": communication.sender,
	# 			"recipients": communication.recipients,
	# 			"cc": communication.cc,
	# 			"bcc": communication.bcc,
	# 			"attachments": get_attachments('Communication', communication.name),
	# 			"read_by_recipient": communication.read_by_recipient,
	# 			"delivery_status": communication.delivery_status,
	# 		},
	# 		"is_lead": True,
	# 	}
	# 	activities.append(activity)

	for attachment_log in docinfo.attachment_logs:
		activity = {
			"name": attachment_log.name,
			"activity_type": "attachment_log",
			"creation": attachment_log.creation,
			"owner": attachment_log.owner,
			"data": parse_attachment_log(attachment_log.content, attachment_log.comment_type),
			"is_lead": True,
		}
		activities.append(activity)

	# calls = get_linked_calls(name)
	# notes = get_linked_notes(name)
	# tasks = get_linked_tasks(name)
	calls = []
	notes = []
	tasks = []
	attachments = get_attachments(doctype_param, name)

	activities.sort(key=lambda x: x["creation"], reverse=True)
	activities = handle_multiple_versions(activities)

	return activities, calls, notes, tasks, attachments

def get_ats_institution_activities(name,doctype_param):
	get_docinfo('',doctype_param, name)
	docinfo = frappe.response["docinfo"]
	lead_meta = frappe.get_meta(doctype_param)
	lead_fields = {field.fieldname: {"label": field.label, "options": field.options} for field in lead_meta.fields}
	avoid_fields = [
		# "converted",
		# "response_by",
		# "sla_creation",
		# "sla",
		"name",
		"first_response_time",
		"first_responded_on",
	]

	doc = frappe.db.get_values(doctype_param, name, ["creation", "owner"])[0]
	activities = [{
		"activity_type": "creation",
		"creation": doc[0],
		"owner": doc[1],
		"data": "created this yyy",
		"is_lead": True,
	}]

	docinfo.versions.reverse()

	for version in docinfo.versions:
		data = json.loads(version.data)
		if not data.get("changed"):
			continue

		if change := data.get("changed")[0]:
			field = lead_fields.get(change[0], None)

			if not field or change[0] in avoid_fields or (not change[1] and not change[2]):
				continue

			field_label = field.get("label") or change[0]
			field_option = field.get("options") or None

			activity_type = "changed"
			data = {
				"field": change[0],
				"field_label": field_label,
				"old_value": change[1],
				"value": change[2],
			}

			if not change[1] and change[2]:
				activity_type = "added"
				data = {
					"field": change[0],
					"field_label": field_label,
					"value": change[2],
				}
			elif change[1] and not change[2]:
				activity_type = "removed"
				data = {
					"field": change[0],
					"field_label": field_label,
					"value": change[1],
				}

		activity = {
			"activity_type": activity_type,
			"creation": version.creation,
			"owner": version.owner,
			"data": data,
			"is_lead": True,
			"options": field_option,
		}
		activities.append(activity)

	for comment in docinfo.comments:
		activity = {
			"name": comment.name,
			"activity_type": "comment",
			"creation": comment.creation,
			"owner": comment.owner,
			"content": comment.content,
			"attachments": get_attachments('Comment', comment.name),
			"is_lead": True,
		}
		activities.append(activity)

	# for communication in docinfo.communications + docinfo.automated_messages:
	# 	activity = {
	# 		"activity_type": "communication",
	# 		"communication_type": communication.communication_type,
	# 		"creation": communication.creation,
	# 		"data": {
	# 			"subject": communication.subject,
	# 			"content": communication.content,
	# 			"sender_full_name": communication.sender_full_name,
	# 			"sender": communication.sender,
	# 			"recipients": communication.recipients,
	# 			"cc": communication.cc,
	# 			"bcc": communication.bcc,
	# 			"attachments": get_attachments('Communication', communication.name),
	# 			"read_by_recipient": communication.read_by_recipient,
	# 			"delivery_status": communication.delivery_status,
	# 		},
	# 		"is_lead": True,
	# 	}
	# 	activities.append(activity)

	for attachment_log in docinfo.attachment_logs:
		activity = {
			"name": attachment_log.name,
			"activity_type": "attachment_log",
			"creation": attachment_log.creation,
			"owner": attachment_log.owner,
			"data": parse_attachment_log(attachment_log.content, attachment_log.comment_type),
			"is_lead": True,
		}
		activities.append(activity)

	# calls = get_linked_calls(name)
	# notes = get_linked_notes(name)
	# tasks = get_linked_tasks(name)
	calls = []
	notes = []
	tasks = []
	attachments = get_attachments(doctype_param, name)

	activities.sort(key=lambda x: x["creation"], reverse=True)
	activities = handle_multiple_versions(activities)

	return activities, calls, notes, tasks, attachments

def get_attachments(doctype, name):
	return frappe.db.get_all(
		"File",
		filters={"attached_to_doctype": doctype, "attached_to_name": name},
		fields=["name", "file_name", "file_type", "file_url", "file_size", "is_private", "creation", "owner"],
	) or []

def handle_multiple_versions(versions):
	activities = []
	grouped_versions = []
	old_version = None
	for version in versions:
		is_version = version["activity_type"] in ["changed", "added", "removed"]
		if not is_version:
			activities.append(version)
		if not old_version:
			old_version = version
			if is_version: grouped_versions.append(version)
			continue
		if is_version and old_version.get("owner") and version["owner"] == old_version["owner"]:
			grouped_versions.append(version)
		else:
			if grouped_versions:
				activities.append(parse_grouped_versions(grouped_versions))
			grouped_versions = []
			if is_version: grouped_versions.append(version)
		old_version = version
		if version == versions[-1] and grouped_versions:
			activities.append(parse_grouped_versions(grouped_versions))

	return activities

def parse_grouped_versions(versions):
	version = versions[0]
	if len(versions) == 1:
		return version
	other_versions = versions[1:]
	version["other_versions"] = other_versions
	return version

# def get_linked_calls(name):
# 	calls = frappe.db.get_all(
# 		"CRM Call Log",
# 		filters={"reference_docname": name},
# 		fields=[
# 			"name",
# 			"caller",
# 			"receiver",
# 			"from",
# 			"to",
# 			"duration",
# 			"start_time",
# 			"end_time",
# 			"status",
# 			"type",
# 			"recording_url",
# 			"creation",
# 			"note",
# 		],
# 	)
# 	return calls or []

# def get_linked_notes(name):
# 	notes = frappe.db.get_all(
# 		"FCRM Note",
# 		filters={"reference_docname": name},
# 		fields=['name', 'title', 'content', 'owner', 'modified'],
# 	)
# 	return notes or []

# def get_linked_tasks(name):
# 	tasks = frappe.db.get_all(
# 		"CRM Task",
# 		filters={"reference_docname": name},
# 		fields=[
# 			"name",
# 			"title",
# 			"description",
# 			"assigned_to",
# 			"assigned_to",
# 			"due_date",
# 			"priority",
# 			"status",
# 			"modified",
# 		],
# 	)
# 	return tasks or []

def parse_attachment_log(html, type):
	soup = BeautifulSoup(html, "html.parser")
	a_tag = soup.find("a")
	type = "added" if type == "Attachment" else "removed"
	if not a_tag:
		return {
			"type": type,
			"file_name": html.replace("Removed ", ""),
			"file_url": "",
			"is_private": False,
		}

	is_private = False
	if "private/files" in a_tag["href"]:
		is_private = True

	return {
		"type": type,
		"file_name": a_tag.text,
		"file_url": a_tag["href"],
		"is_private": is_private,
	}