import traceback

from flask import jsonify, request

from apps.admin.admininterface import AdminInterface
from apps.admin.models import AuditLog
from apps.auth.models import User
from apps.auth.status import AccountStatus


class Admin(AdminInterface):

    def close_account(self,data):

        try:
            email = data.get('email')
            user = User.objects(email=email).first()

            if user is None:
                return jsonify({"status": "error", "message": "User not found"}), 401

            if user.status == AccountStatus.INACTIVE:
                return jsonify({"status": "error", "message": "This account is already deactivated"}), 401

            if user.status == AccountStatus.ACTIVE:
                user.update(set__status=AccountStatus.INACTIVE.value)
                user.save()
                return jsonify({"status": "success",
                                "message": "User account is deactivated successfully"}), 200

            return jsonify({"status": "error",
                            "message": "Invalid account status"}), 401

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"status": False, "message": str(e)}), 500


    def suspend_account(self,data):

        try:
            email = data.get('email')
            user = User.objects(email=email).first()

            if user is None:
                return jsonify({"status": "error", "message": "User not found"}), 401

            if user.status == AccountStatus.INACTIVE:
                return jsonify({"status": "error", "message": "This account is deactivated"}), 401


            if user.status == AccountStatus.ACTIVE:
                user.update(set__status=AccountStatus.SUSPENDED.value)
                user.save()
                return jsonify({"status": "success",
                                "message": "User account is suspended successfully"}), 200

            return jsonify({"status": "error",
                            "message": "Invalid account status"}), 401

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"status": False, "message": str(e)}), 500



    def activate_account(self, data):
        try:
            email = data.get('email')
            user = User.objects(email=email).first()

            if user is None:
                return jsonify({"status": False, "message": "User not found"})

            if user.status not in [AccountStatus.SUSPENDED, AccountStatus.INACTIVE]:
                return jsonify({"status": False, "message": "This account is active"}), 401

            user.update(set__status=AccountStatus.ACTIVE.value)
            user.save()
            return jsonify({"status": "success",
                            "message": "User account is activated successfully"}), 200

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"status": False, "message": str(e)}), 500



    def view_audit_logs(self):
        logs = AuditLog.objects()

        log_list = [
            {
            "id": str(log.id),
            "user" : str(log.user.id),
            "action": log.action,
            "details": log.details,
        "ip_address": log.ip_address,
        "device_info": log.device_info,
        "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for log in logs
        ]
        return jsonify({f"status": "success","log_list": log_list}), 200



