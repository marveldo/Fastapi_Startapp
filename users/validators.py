import re



def password_validator(password : str) :
        if not any(c.islower() for c in password):
            raise ValueError("password must include at least one lowercase character")
        if not any(c.isupper() for c in password):
            raise ValueError("password must include at least one uppercase character")
        if not any(c.isdigit() for c in password):
            raise ValueError("password must include at least one digit")
        # if not any(c in ['!','@','#','$','%','&','*','?','_','-'] for c in password):
        #     raise ValueError("password must include at least one special character")

def email_is_valid(email : str) :
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return  re.match(email_regex , email)
         