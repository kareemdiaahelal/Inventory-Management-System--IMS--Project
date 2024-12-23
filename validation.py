def is_valid_name(name):
    return len(name) > 0 and name.isalpha()

def is_valid_age(age):
    return age.isdigit() and int(age) > 0 and len(age) < 3

def is_valid_email(email):
    if "@" in email and "." in email.split("@")[-1]:
        local, domain = email.split("@")
        return len(local) > 0 and len(domain) > 0
    return False

def is_valid_password(password):
    return len(password) >= 6

def is_valid_role(role):
    return role in ["admin", "user"]
