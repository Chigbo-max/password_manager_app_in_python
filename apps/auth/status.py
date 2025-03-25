from enum import Enum


class AccountStatus(Enum):
    ACTIVE =  "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"