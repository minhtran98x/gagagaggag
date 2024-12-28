import frappe
from frappe import _

COLORS_STATE = {
    "": {
        "color": '#525252',
        "background": "#f3f3f3"
    },
    "Primary": {
        "color": '#0070cc',
        "background": "#edf6fd"
    },
    "Info": {
        "color": '#007be0',
        "background": "#f7fbfd"
    },
    "Success": {
        "color": '#16794c',
        "background": "#e4f5e9"
    },
    "Warning": {
        "color": '#bd3e0c',
        "background": "#fff1e7"
    },
    "Danger": {
        "color": '#b52a2a',
        "background": "#fff0f0"
    },
    "Inverse": {
        "color": 'inherit',
        "background": "inherit"
    }
}


@frappe.whitelist()
def get_doc_info(doctype, docname=''):
    from frappe.model.workflow import is_transition_condition_satisfied
    transitions_access = []
    workflow = None
    allow_sate_cancel = True
    allow_state_edit = False
    is_submittable = frappe.db.get_value(
        'DocType', doctype, ['is_submittable'])
    workflow_state = ''
    override_status = 0
    lst_status = {
        0: {
            "label": _("Draft"),
            "color": '#b52a2a',
            "background": "#fff0f0"
        },
        1: {
            "label": _("Submitted"),
            "color": '#0070cc',
            "background": "#edf6fd"
        },
        2: {
            "label": _("Cancelled"),
            "color": '#b52a2a',
            "background": "#fff0f0"
        },
        3: {
            "label": _("Not Saved"),
            "color": '#bd3e0c',
            "background": "#fff1e7"
        }
    }

    # tim kiem workflow cho doc
    if docname:
        # lay workflow
        workflow = frappe.db.get_value(
            "Workflow", {"document_type": doctype, "is_active": 1}, ["name", "workflow_state_field", "override_status"], as_dict=1)

        # neu ton tai workflow thi xu ly
        if workflow:
            override_status = workflow.override_status
            # lay user hien tai
            current_user = frappe.session.user
            # lay cac quyen cua user
            user_roles = frappe.get_roles(current_user)

            doc = frappe.get_doc(doctype, docname)
            workflow_state = doc.get(workflow.workflow_state_field)
            # lay style cua trang thai workflow
            workflow_state_style = frappe.db.get_value(
                'Workflow State', workflow_state, ["style"])
            color_state = COLORS_STATE.get(workflow_state_style)
            lst_status[workflow_state] = {
                "label": _(workflow_state),
                "color": color_state['color'] if color_state else "inherit",
                "background": color_state['background'] if color_state else "inherit",
            }
            # lay cac transition cho hanh dong tiep theo cua user
            transitions = frappe.get_all('Workflow Transition', filters={
                'parent': workflow.name, 'state': workflow_state
            }, fields=['action', 'allowed', 'allow_self_approval', 'condition'], order_by='idx asc')
            # kiem tra xem co duoc phep cancel doc khi co workflow khong
            next_state = frappe.db.get_value(
                'Workflow Document State', {'parent': workflow.name, 'doc_status': 2}, ["state"])
            if next_state:
                allow_sate_cancel = False if frappe.db.exists('Workflow Transition', {
                    'parent': workflow.name, 'next_state': next_state
                }) else True
            # kiem tra xem co duoc phep edit doc khi co workflow khong
            workflow_states = frappe.get_all('Workflow Document State', filters={
                'parent': workflow.name, 'state': workflow_state
            }, fields=['allow_edit', 'avoid_status_override'], order_by='idx asc', limit=1)
            for role in workflow_states:
                if role.allow_edit in user_roles:
                    allow_state_edit = True
                if role.avoid_status_override and override_status == 0:
                    override_status == role.avoid_status_override

            # loc cac transition duoc phep doi voi user
            for trans in transitions:
                # neu khong thoa man condition doc thi bo qua
                if not is_transition_condition_satisfied(trans, doc):
                    continue
                # neu bo qua hanh dong cho user tao doc thi bo qua
                if doc.owner == current_user and trans.allow_self_approval == 0:
                    continue
                # neu user khong co quyen voi doc thi bo qua
                if trans.allowed not in user_roles:
                    continue
                # them cac transition hop le
                transitions_access.append({
                    'action': trans.action
                })

    permissions = {
        'read': 1 if frappe.has_permission(doctype, 'read') else 0,
        'create': 1 if frappe.has_permission(doctype, 'create') else 0,
        'write': 1 if frappe.has_permission(doctype, 'write') else 0,
        'submit': 1 if is_submittable and frappe.has_permission(doctype, 'submit') else 0,
        'cancel': 1 if is_submittable and frappe.has_permission(doctype, 'cancel') else 0,
        'delete': 1 if frappe.has_permission(doctype, 'delete') else 0,
        'amend': 1 if is_submittable and frappe.has_permission(doctype, 'amend') else 0,
    }

    return {
        "permissions": permissions,
        "transitions": transitions_access,
        "has_workflow": True if workflow else False,
        "allow_sate_cancel": allow_sate_cancel,
        "allow_state_edit": allow_state_edit,
        "is_amended": True if frappe.db.exists(doctype, {"amended_from": docname}) else False,
        "is_submittable": is_submittable,
        "override_status": override_status,
        "lst_status": lst_status,
        "workflow_state": workflow_state
    }
