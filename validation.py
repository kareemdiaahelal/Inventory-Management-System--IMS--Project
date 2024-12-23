def is_valid_age(age):
    return age.isdigit() and int(age) > 0

def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]

