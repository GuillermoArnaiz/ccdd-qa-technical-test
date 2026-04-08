import uuid


def unique_id():
    return uuid.uuid4().hex[:8]


def generate_user():
    uid = unique_id()
    return {
        "username": f"testuser_{uid}",
        "email": f"test_{uid}@example.com",
        "password": f"Pass_{uid}!",
    }


def generate_plan(prefix="Plan"):
    uid = unique_id()
    return {
        "name": f"{prefix}_{uid}",
        "phone1": f"+346{uid}",
        "phone2": f"+346{uid[::-1]}",
    }
