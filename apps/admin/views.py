from flask import Blueprint, request

from apps.admin.services import Admin

admin_view = Blueprint('admin_view', __name__)

@admin_view.route("/admin/close-account", methods=['POST'])
def close_account():
    data = request.get_json()
    return Admin.close_account(data)

@admin_view.route("/admin/activate-account", methods=['POST'])
def activate_account():
    data = request.get_json()
    return Admin.activate_account(data)

@admin_view.route("/admin/suspend-account", methods=['POST'])
def suspend_account():
    data = request.get_json()
    return Admin.suspend_account(data)