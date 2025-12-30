from enum import IntEnum, unique


@unique
class Privileges(IntEnum):
    USER_ACTIVE = 1 << 0
    ADMIN_ACCESS_PANEL = 1 << 1

    @classmethod
    def max_privilege(cls):
        return sum(p.value for p in cls)

    @classmethod
    def has_privilege(cls, privileges, user_privileges: int = -1) -> bool:
        if user_privileges == -1:
            return False
        return (privileges & user_privileges) > 0

    @classmethod
    def get_privileges_list(cls, user_privileges: int = 3, gd: bool = False) -> list[dict[str, str]]:
        privileges_list: list = []

        for privilege in Privileges:
            if privilege.value <= 0:
                continue
            
            privileges_list.append({
                "name": privilege.name,
                "value": privilege.value,
                "checked": "checked" if (user_privileges & privilege.value) > 0 else "",
                "disabled": "disabled" if (privilege.value <= 2 and not gd) else "",
                "gd": "disabled" if gd else False
            })
        return privileges_list