def new_user(login, nick_name, password):
    


def login_chek(login):
    with open('login.json', 'r') as jfr:
        jf_file = json.load(jfr)
        for users in (jf_file[0]['users']):
            if users['login'] == login:
                return True

def pass_chek(login, password):
    with open('login.json', 'r') as jfr:
        jf_file = json.load(jfr)
        for users in (jf_file[0]['users']):
            if (users['login'] == login) and users['password'] == password:
                return True

def displayMenu():
    global status
    status = input("Are you registered user? y/n? Press q to quit\n")
    if status == "y":
        oldUser()
    elif status == "n":
        newUser()

def newUser():
    global status
    global login
    login = input("Create login name: ")
    if login_chek(login) == True:
        print("\nLogin name already exist!\n")
        status = "name_exist"
    else:
        create_pass = input("Create password: ")
        write_to_json_new_user(login, create_pass)
        status = "new_user"
        print("\nUser created\n")

def oldUser():
    global status
    global login
    login = input("Enter login name: ")
    passw = input("Enter password: ")
    if pass_chek(login, passw) == True:
        print("\nLogin successful\n")
        status = "successful"
    else:
        print("\nUser doesn't exist or wrong password!\n")
        status = "wrong!!!"

def login_sys():
    while status != "q" and status != "successful":
        displayMenu()
        return print(status, login)