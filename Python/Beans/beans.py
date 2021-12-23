import os
import linecache
import platform
import sys
import time
import socket


forbidden_names = ['panel', 'back', 'create']


def load():
    print("Establishing connection to the Bean Network...")
    time.sleep(2.5)
    print(f"Connecting with IP {socket.gethostbyname(socket.gethostname())}...")
    time.sleep(4)
    print("Connection successful!")
    ctrl()


def info():
    arc = platform.architecture()
    print(f"""Bean Network Client v{platform.python_version()}

Interpreter compiled with {platform.python_compiler()}
Written with Python {platform.python_version()}
Development environment: IDLE, PyCharm

Running on {platform.system()} {platform.release()}, version {platform.version()} ({arc[0][:2] + '-' + arc[0][2:]}) 


Type 'back' to return to the control panel.
""")
    infoback = input()
    if infoback.lower() == "back":
        ctrl()
    else:
        info()


def passchange_confirm(acc_selection, index, passinp):
    passconfirm = input("Please confirm your new password... ")

    if passconfirm == passinp:
        passchange = open('accounts/' + acc_selection + '.bean', 'w')
        index[1] = passinp + '\n'
        passchange.writelines(index)
        passchange.close()
        print("Your password has been successfully changed.")
        ctrl()
    else:
        print("Oops, that password doesn't match!")
        change_pass(acc_selection, index)
        

def change_pass(acc_selection, index):
    passinp = input("Please enter a new password for your account... ")

    if passinp == '':
        print("Please enter a password!")
        change_pass(acc_selection, index)
    else:
        passchange_confirm(acc_selection, index, passinp)


def change_name(acc_selection, index):
    nameinp = input("Please enter a new name for your account...")

    file_check = os.path.isfile('accounts/' + nameinp + '.bean')

    if nameinp == '':
        print("Please enter a valid name!")
        change_name(acc_selection, index)
    elif file_check:
        print("Sorry, this name is already in use. Please try again.")
        change_name(acc_selection, index)
    else:
        namechange = open('accounts/' + acc_selection.capitalize() + '.bean', 'w')
        index[0] = nameinp.capitalize() + '\n'
        namechange.writelines(index)
        namechange.close()
        print(f"Changing name to '{nameinp.capitalize()}'...")
        
        os.rename('accounts/' + acc_selection + '.bean', 'accounts/' + nameinp.capitalize() + '.bean')
        print(f"Account name successfully changed to '{nameinp}'!")
        ctrl()


def change(acc_selection, index):
    change_choice = input()
    if change_choice == '1':
        change_name(acc_selection, index)
    elif change_choice == '2':
        change_pass(acc_selection, index)
    elif change_choice == '3':
        ctrl()


def acc_change():
    acc_selection = input("Please enter the name of the account you wish to change... ")

    file_check = os.path.isfile('accounts/' + acc_selection + '.bean')
    if file_check:
        found_acc = open('accounts/' + acc_selection + '.bean')
        index = found_acc.readlines()
        found_acc.close()

        password = input(f"Please enter your current password to log in to '{acc_selection}` ")

        if password == index[1].strip('\n'):
            print(f"""Logged in successfully!

[1] to change account name
[2] to change account password
[3] to return to control panel
        """)
            change(acc_selection, index)
        else:
            print("Incorrect password; please try logging in again.")
            acc_change()

    else:
        print(f"Error: Couldn't find account '{acc_selection}'")
        acc_change()


def acc_delete():
    acc_selection = input("Please enter the name of the account you wish to delete... ")

    file_check = os.path.isfile('accounts/' + acc_selection + '.bean')
    if file_check:
        found_acc = open('accounts/' + acc_selection + '.bean')
        index = found_acc.readlines()
        found_acc.close()
        print("""
        WARNING: By deleting this account you will permanently lose access to all of its data including bean credits.
        If you wish to make a new account, your bean credits will NOT roll over.
    """)
        password = input(f"Please type the password for {acc_selection.capitalize()} to confirm the deletion, or type "
                         f"'back' to go back. ")

        if password == index[1].strip('\n'):
            os.remove('accounts/' + acc_selection + '.bean')
            print(f"Account '{acc_selection}' deleted successfully.")
            ctrl()
        elif password.lower() == 'back':
            ctrl()
        else:
            print("Incorrect password, please try again...")
            acc_delete()
    else:
        print(f"Error: Couldn't find account '{acc_selection}'")
        acc_delete()


def ctrl():
    print(f"""
BEAN NETWORK CLIENT CONTROL PANEL

<< Main >>
    [1] to start the main program
    [2] to view technical information about the program

<< Accounts >>
    [3] to delete an account
    [4] to change an account's information

<< Exit >>
    [5] to exit
""")
    ctrl_choice = input()
    if ctrl_choice == '1':
        login()
    elif ctrl_choice == '2':
        info()
    elif ctrl_choice == '3':
        acc_delete()
    elif ctrl_choice == '4':
        acc_change()
    elif ctrl_choice == '5':
        sys.exit("Program exited by user")
    else:
        ctrl()


def confirm(new_beanuser, new_beanpass):
    bean_confirmpass = input("Account created successfully. Please confirm your password to activate it... ")
    if bean_confirmpass == new_beanpass:
        os.rename('accounts/' + new_beanuser + '.tempbean', 'accounts/' + new_beanuser.capitalize() + '.bean')
        print("Password confirmed! Your account has been activated.")
        login()
    else:
        print("Oops, that password doesn't match. Please try again.")
        confirm(new_beanuser, new_beanpass)


def user_create():
    new_beanuser = input("""
    CREATE A NEW BEAN ACCOUNT

    Enter your name to get started... """)

    file_check = os.path.isfile('accounts/' + new_beanuser + '.bean')

    if new_beanuser.lower() in forbidden_names:
        print("Sorry, you can't use this name. Please try another.")
        user_create()
    elif new_beanuser == '':
        print("Please enter a valid name!")
        user_create()
    elif file_check:
        print("Sorry, this name has been taken. Please try another name.")
        user_create()

    new_beanpass = input("Now, create a password for your new bean account... ")

    print("Creating your account...")
    if not os.path.exists('accounts'):
        os.makedirs('accounts')
        
    create_bean = open('accounts/' + new_beanuser.capitalize() + '.tempbean', 'w')
    create_bean.write(f"""{new_beanuser.capitalize()}
{new_beanpass}
0""")

    create_bean.close()
    confirm(new_beanuser, new_beanpass)


def pass_check(bean_user):
    login_data = open('accounts/' + bean_user + '.bean', 'r')

    bean_credit = int(linecache.getline('accounts/' + bean_user + '.bean', 3))

    index = login_data.readlines()

    password = input("Please enter your password to log in... ")

    if password == index[1].strip('\n'):
        login_data.close()
        print("Logged in successfully!")
        bean_ask(bean_credit, bean_user, index)
    else:
        print("That password is incorrect, please try again.")
        pass_check(bean_user)


def login():
    print(f"""
    BEAN NETWORK LOGIN

    Enter your name below to access your bean account.

    If you wish to create a bean account, type 'create'.
    If you wish to return to the control panel, type 'panel'
    """)
    bean_user = input()

    file_check = os.path.isfile('accounts/' + bean_user + '.bean')
    if file_check:
        print(f"Welcome, {bean_user.capitalize()}")
        pass_check(bean_user)
    elif bean_user.lower() == "create":
        user_create()
    elif bean_user.lower() == "panel":
        ctrl()
    else:
        print(f"Oops! '{bean_user}' could not be found. If you wish to create a new bean user, type 'create'.")
        print("")
        login()


def credit_check(bean_credit, bean_user, index):
    if int(index[2]) < 0:
        print("WARNING: YOUR BEAN CREDIT(TM) IS NEGATIVE. YOU ARE REQUIRED TO INCREASE YOUR BEAN CREDIT(TM) TO AN "
              "ACCEPTABLE NUMBER ASAP.")
    elif int(index[2]) == 0:
        print("Your bean credit is 0. While this isn't an offence it's recommended to increase it nonetheless. "
              "Please increase whenever you can.")
    elif int(index[2]) >= 10000:
        print("Woohoo! your bean credit is through the roof! rock on!- Or should I say, bean on!!")
    print("")
    print(f"Your current bean credit is {bean_credit}")
    return_to_bean = input("Nothing's like getting more bean credit - type 'bean' to make some more! ")

    if return_to_bean.lower() == "bean":
        bean_ask(bean_credit, bean_user, index)
    else:
        credit_check(bean_credit, bean_user, index)


def bean_ask(bean_credit, bean_user, index):
    print(f"""Welcome, {bean_user.capitalize()}!

If you wish to check your current bean credit, type 'credit'
If you wish to log out of your account, type 'logout'
""")

    beans = input("Do you like beans? ")

    if beans.lower() == "yes":
        login_data = open('accounts/' + bean_user + '.bean', 'w')
        print("Yay :D")
        bean_credit += 100

        origin = int(index[2])
        new_beans = origin + 100
        index[2] = str(new_beans)

        login_data.writelines(index)
        print(f"Your bean credit is now {bean_credit}!")
        login_data.close()

        bean_ask(bean_credit, bean_user, index)
    elif beans.lower() == "no":
        login_data = open('accounts/' + bean_user + '.bean', 'w')
        bean_credit -= 9999

        origin = int(index[2])
        deducted_beans = origin - 9999
        index[2] = str(deducted_beans)
        login_data.writelines(index)
        print("Go away >:(")
        login_data.close()
        
        bean_ask(bean_credit, bean_user, index)
    elif beans.lower() == "credit":
        credit_check(bean_credit, bean_user, index)
    elif beans.lower() == "logout":
        print(f"Logging out of account '{bean_user.capitalize()}'...")
        login()
    else:
        print("Sorry, I didn't get that. Please specify either yes/no, or 'credit' for credit check.")
        bean_ask(bean_credit, bean_user, index)


def os_check():
    if sys.platform == 'win32':
        load()
    else:
        print(f"""Warning:
Your system was detected as running {platform.system()}. It is important to note that this program was designed
for Windows-based systems and has not been tested on others. As a result, certain things might not function as intended.

Type 'ok' to acknowledge and continue, or 'exit' to quit.""")
        choice = input()
        if choice.lower() == 'ok':
            load()
        elif choice.lower() == 'exit':
            sys.exit("Program exited by user")
        else:
            os_check()


os_check()
