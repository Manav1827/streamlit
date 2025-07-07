import streamlit_authenticator as stauth

# -------------------- USER CREDENTIALS --------------------
names = ["Manav Patel"]
usernames = ["manav"]
passwords = ["123456"]

# Hash passwords (new syntax for streamlit-authenticator >= 0.2.0)
hashed_passwords = stauth.Hasher().generate(passwords)

# Credentials dictionary
credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0]
        }
    }
}
