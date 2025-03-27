
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from apps.admin.services import Admin
from helpers.decorators import admin_required

admin_view = Blueprint('admin_view', __name__)
admin = Admin()
@admin_view.route("/admin/close-account", methods=['POST'])
@jwt_required()
@admin_required
def close_account():
    data = request.get_json()
    return admin.close_account(data)

@admin_view.route("/admin/activate-account", methods=['POST'])
@jwt_required()
@admin_required
def activate_account():
    data = request.get_json()
    return admin.activate_account(data)

@admin_view.route("/admin/suspend-account", methods=['POST'])
@jwt_required()
@admin_required
def suspend_account():
        data = request.get_json()
        return admin.suspend_account(data)

@admin_view.route("/admin/view-audit-logs", methods=['GET'])
@jwt_required()
@admin_required
def view_audit_logs():
    return admin.view_audit_logs()
