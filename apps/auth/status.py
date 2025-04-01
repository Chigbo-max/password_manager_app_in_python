from enum import Enum


class AccountStatus(Enum):
    ACTIVE =  "active"
    INACTIVE = "deactivated"
    SUSPENDED = "suspended"