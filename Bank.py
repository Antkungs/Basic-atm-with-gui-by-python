import PySimpleGUI as sg

class BankAccount:
    def __init__(self, accNo,pwd, accName, balance):
        self.accNo = accNo
        self.pwd = pwd
        self.accName = accName
        self.balance = balance

def loadaccbank():
    listacc = []
    with open("log.txt", 'r') as f:
        for line in f:
            data = line.strip().split(',')
            listacc.append(BankAccount(data[0], data[1], data[2],float(data[3])))
    return listacc

def saveaccbank():
    with open("log.txt", 'w') as f:
        for account in dataacc:
            f.write(f"{account.accNo},{account.pwd},{account.accName},{account.balance}\n")

def clearText():
    window['accNo'].update('')
    window['pwd'].update('')
    window['money'].update('')
    window['result'].update("")

dataacc = loadaccbank()

layout = [
    [sg.Text("Bank Account Management")],
    [sg.Text("Account Number:"), sg.InputText(key='accNo')],
    [sg.Text("Password:"), sg.InputText(key='pwd')],
    [sg.Text("Money:"), sg.InputText(key='money')],
    [sg.Button("Deposit Money"), sg.Button("Withdraw Money"),sg.Button("Check Money")],
    [sg.Text("", size=(80, 1), key='result')],
    [sg.Button("Exit")]
]

window = sg.Window("Bank Account Management", layout)

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Deposit Money' or event == 'Withdraw Money':
        if values['accNo']== '' or values['money'] == '':
            sg.popup_error("กรุณากรอกข้อมูลให้ครบ.",title="Error")
            clearText()
            continue

        accNo = values['accNo']
        pwd = values['pwd']
        money = float(values['money'])
        
        for account in dataacc:
                if account.accNo == accNo and account.pwd != pwd:
                    sg.popup_error("รหัสไม่ถูกต้อง.",title="Error")
                    clearText()
                    continue
                elif account.accNo == accNo and account.pwd == pwd:
                    if event == 'Deposit Money':
                        account.balance += money
                        sg.popup(f"ฝากเงิน : {money} บาทสำเร็จ")
                    elif event == 'Withdraw Money':
                        if 0 < money <= account.balance:
                            account.balance -= money
                            sg.popup(f"ถอนเงิน : {money} บาทสำเร็จ")
                        else:
                            window['result'].update(f"You can't withdraw , you have money :{account.balance}")

                            continue
                    
                    saveaccbank()
                    clearText()
                    window['result'].update(f"Account: {account.accName}, Your Money: {account.balance}")

    if event == 'Check Money':

        accNo = values['accNo']
        pwd = values['pwd']

        if values['accNo']== '':
            sg.popup_error("กรุณากรอกเลขบัญชี.",title="Error")
            continue
        for account in dataacc:

            if account.accNo == accNo and account.pwd != pwd or account.pwd == "":
                sg.popup_error("รหัสไม่ถูกต้อง.",title="Error")
                clearText()
                continue
            elif account.accNo == accNo and account.pwd == pwd:
                window['result'].update(f"Account: {account.accName}, Your Money: {account.balance}")



window.close()
