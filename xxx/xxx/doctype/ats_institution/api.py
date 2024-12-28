import frappe
from frappe import _
import json
from xxx.api.doc import get_fields_meta


@frappe.whitelist()
def create_yyy(institution_name=None, location=None, type=None):
    try:
        # Tên Doctype
        doctype_name = "ATS-Institution"

        # Kiểm tra các trường bắt buộc
        validate_required_fields(doctype_name, {
            "institution_name": institution_name,
            "location": location,
            "type": type
        })

        # Tạo và lưu bản ghi
        yyy_record = frappe.get_doc({
            "doctype": doctype_name,
            "institution_name": institution_name,
            "location": location,
            "type": type
        })
        yyy_record.insert()
        frappe.db.commit()

        # Trả về kết quả thành công
        return {
            "message": "Tạo thành công.",
            "data": yyy_record.name  # Trả về tên (ID) của bản ghi mới
        }

    except frappe.exceptions.ValidationError as e:
        # Rollback để tránh lưu dữ liệu không hợp lệ
        frappe.db.rollback()
        frappe.local.response["http_status_code"] = 400
        return {
            "message": "Tạo không thành công.",
            "error": "Validation Error",
            "details": str(e)
        }

    except Exception as e:
        # Rollback để tránh lưu dữ liệu khi gặp lỗi
        frappe.db.rollback()
        frappe.local.response["http_status_code"] = 500
        return {
            "message": "Tạo không thành công.",
            "error": "Unknown Error",
            "details": str(e)
        }

@frappe.whitelist()
def get_yyy(name):
    lst = frappe.qb.DocType("ATS-Institution")

    query = frappe.qb.from_(lst).select("*").where(lst.name == name).limit(1)

    lst_data = query.run(as_dict=True)
    if not len(lst_data):
        frappe.throw(_("yyy not found"), frappe.DoesNotExistError)
    lst_data = lst_data.pop()

    lst_data["doctype"] = "ATS-Institution"
    lst_data["fields_meta"] = get_fields_meta("ATS-Institution")
    print("Test log lst_data : ",lst_data)
    return lst_data


@frappe.whitelist()
def update_yyy(yyyId, institution_name=None, location=None, type=None):
    try:
        # Lấy bản ghi cần cập nhật
        doc = frappe.get_doc('ATS-Institution', yyyId)
        
        # Kiểm tra các trường bắt buộc (chỉ kiểm tra các trường được cung cấp)
        validate_required_fields("ATS-Institution", {
            "institution_name": institution_name,
            "location": location or doc.location,
            "type": type or doc.type
        })

        # Cập nhật các trường nếu có giá trị mới
       
        doc.institution_name = institution_name
        doc.location = location
        doc.type = type

        # Lưu và commit
        doc.save()

        return {"message": "yyy updated successfully"}

    except frappe.exceptions.DoesNotExistError:
        frappe.local.response["http_status_code"] = 404
        return {
            "message": "Không tìm thấy bản ghi với ID đã cung cấp.",
            "error": "Not Found"
        }

    except frappe.exceptions.ValidationError as e:
        frappe.db.rollback()
        frappe.local.response["http_status_code"] = 400
        return {
            "message": "Cập nhật không thành công.",
            "error": "Validation Error",
            "details": str(e)
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.local.response["http_status_code"] = 500
        return {
            "message": "Cập nhật không thành công.",
            "error": "Unknown Error",
            "details": str(e)
        }
        
def validate_required_fields(doctype, data):
    """
    Hàm kiểm tra các trường bắt buộc từ Doctype.
    :param doctype: Tên Doctype cần kiểm tra.
    :param data: dict chứa các trường và giá trị của chúng.
    :raises frappe.exceptions.ValidationError: nếu trường bắt buộc bị thiếu.
    """
    # Lấy meta của Doctype
    meta = frappe.get_meta(doctype)

    # Lấy danh sách các trường bắt buộc
    required_fields = [df.fieldname for df in meta.fields if df.reqd]

    # Tìm các trường bị thiếu
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        raise frappe.exceptions.ValidationError(
            f"Các trường sau đây là bắt buộc: {', '.join(missing_fields)}"
        )        