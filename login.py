import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin with a corrected file path
cred = credentials.Certificate(r"C:\Users\naman\Downloads\cp-spsu-db-firebase-adminsdk-2v29c-1830ac9c7c.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

print("---------------Login / Sign Up--------------------\n")
print("Input 1 for Login.")
print("Input 2 for Sign Up.\n")
print("--------------------------------------------------\n")

userinput = int(input("Select Your Choice: "))

def TakeUserData():
    while True:
        fullname = str(input('Enter your Full Name: '))
        if fullname == '':
            print('worng input try again.')
            continue

        DoB = str(input("Enter Dob (eg. dd/mm/yyyy): "))
        if len(DoB) != 10:
            print('worng input try again.')
            continue

        Branch = str(input("Enter Your Branch: "))
        if Branch == '':
            print('worng input try again.')
            continue

        doc = {
            'FullName': fullname,
            'DoB': DoB,
            'Branch': Branch,
            'Balance': 0 
        }
        return doc

def MakeUserName():
    while True:
        UserName = str(input("Enter Your UserName: "))
        doc_path = db.collection('users').document(UserName)
        finddoc = doc_path.get()

        if finddoc.exists:
            print("username already taken try another.")
            continue
        else:
            return UserName

def GetValidPassword():
    while True:
        password = str(input('Select Your 4-digit password: '))
        if len(password) == 4 and password.isdigit():
            return int(password)
        else:
            print('worng input try again.')

def withdrawMoney(userName):
    newAmmount =  int(input('Enter Amount To be withdraw: '))

    if newAmmount < 0:
        print("Worng Input")
    
    doc_path = db.collection('users').document(userName)
    doc = doc_path.get()
    doc = doc.to_dict()

    if doc['Balance'] > newAmmount:
        confirm = str(input(f'Are Youe Sure Your Want to withdraw {str(newAmmount)} (yes/no): '))

        if confirm == 'yes':
            updatedamt = doc['Balance'] - newAmmount
            doc = doc_path.update({
                'Balance' : updatedamt
            })

            print(f'{str(newAmmount)} Ammount withdraw')
            print(f'updated balance: {str(updatedamt)}')
        elif confirm == 'no':
            print('withdraw canncled.')
        else:
            print('worng input')
    else:
        print('insufficent balance.')


def dipostieMoney(userName):
    newAmmount =  int(input('Enter Amount To be diposited: '))

    if newAmmount < 0:
        print("Worng Input")
    
    doc_path = db.collection('users').document(userName)
    doc = doc_path.get()
    doc = doc.to_dict()

    updatedamt = doc['Balance'] + newAmmount
    doc = doc_path.update({
        'Balance' : updatedamt
    })

    print(f'{str(newAmmount)} Ammount added')
    print(f'updated balance: {str(updatedamt)}')

def accountClosing(userName):
    doc_path = db.collection('users').document(userName)
    doc = doc_path.get()
    doc = doc.to_dict()

    if doc['Balance'] > 0:
        print('You Need To withdraw your money first.')
    else:
        doc = doc_path.get()
        doc.delete()
        print('Your Account Has Closed.')

def showService(userName):
    doc_path = db.collection('users').document(userName)
    doc = doc_path.get()
    doc = doc.to_dict()

    print(f"\n--------------------- Wellcome {doc['FullName']} -------------------------\n")

    print('Sevrice Avalable: ')
    print('1. withdraw money')
    print('2. deposite money')
    print('3. balance check')
    print('4. Account Closing')
    print('5. Logout')

    choise = int(input("\nEnter your Choise: "))


    if choise == 1:
        withdrawMoney(userName)
        showService(userName)
    elif choise == 2:
        dipostieMoney(UserName)
        showService(UserName)
    elif choise == 3:
        print(f'your Account Balance is {str(doc['Balance'])}')
        showService(UserName)
    elif choise == 4:
        accountClosing(userName)
        showService(userName)
    elif choise == 5:
        print('Logout Done!.')


if userinput == 2:
    UserDoc = TakeUserData()
    
    DocName = MakeUserName()

    password = GetValidPassword()

    UserDoc['password'] = password

    doc_path = db.collection('users').document(DocName)
    doc_path.set(UserDoc)

    print('You are now registered.')

elif userinput == 1:
    while True:
        UserName = str(input("username: "))

        doc_path = db.collection('users').document(UserName)
        doc = doc_path.get()

        if doc.exists:
            doc = doc.to_dict()

            password = int(input("password: "))

            if password == doc['password']:
                print("\nYou have successfully logged in.\n")
                showService(UserName)
                break
            else:
                print("Wrong password")
        else:
            print("User not found try again.")




