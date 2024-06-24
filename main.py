import mailbox
from email.header import decode_header
import pandas as pd
import os
import threading
import time
import random

#occurrence CONFIG
#Disable/enable extra csv with occurrence of domain parts
occurrence = True
#Disable/enable saving .com
com = False
#exclude/include singles
sing = False

global otputdf,processing,stime
stime = 0
processing = True
loading = True
otputdf = pd.DataFrame()
occurrence_res = []

class color:
   #-credit: Bacara
   #https://stackoverflow.com/questions/8924173/how-can-i-print-bold-text-in-python
   
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def get_time():
    global stime
    if stime == 0:
        stime = time.time()
    elapsed_time  = time.time() - stime
    if elapsed_time < 60:
        return f"{elapsed_time:05.2f}s|-   "
    elif elapsed_time < 3600:
        elapsed_time = elapsed_time / 60
        return f"{elapsed_time:05.2f}m|-   "
    else:
        elapsed_time = elapsed_time / 3600
        return f"{elapsed_time:05.2f}h|-   "
    

def check_occurrence(dom):
    global occurrence_res
    if occurrence:
        for part in dom.split('.'):
            if not com and part == 'com':
                continue
            else:
                occurrence_res.append(part)
        

def handle_user_input():
    """
    Allows to stop and save at any moment
    """
    global processing,loading
    input(get_time()+color.GREEN+color.BOLD +"Press Enter to stop processing!" + color.END)
    loading = False
    processing = False
    exiting()

def loading_animation():
    """
    Displays loding bars wile file is loaded, bigger file longer load time
    """
    global loading
    animations = [{"anim":["   ",".  ", "o. ", "0o.",")0o","()0","0()","o0(", ".o0"," .o", "  ."],"time":0.2},
                  {'anim':["   ",".  ",".. ","..."],'time':0.4},
                  {'anim':["-","\\","|","/"],'time':0.2},
                  {'anim':["o0o","0o0"],'time':0.5},
                  {'anim':['|  |',"\\  /","_  _"," /\\ ",' || '," /\\ ","_  _","\\  /"],'time':0.1},
                  {'anim':["---",'\\--',"|--","/--","---","-\\-","-|-","-/-","---","--\\","--|","--/"],'time':0.1},
                  {'anim':["=--","==-","===",">==","<>=","=<>","==<","-==","--=","---"],'time':0.2},
                  {'anim':["+x+","x+x",],'time':0.2},
                  {'anim':[" <0/ "," <0--"," <o\\"," <o> "," <0> "," /0> ","--o "," \\o> "],'time':0.2},
                  {'anim':['|||','/||','//|',"_//","__/","___","\\__","\\\\_","|\\\\","||\\"],'time':0.2},
                  {'anim':["+x+","x+x",],'time':0.2},
                 ]
    sel = random.choice(animations) 
    animation = sel["anim"]
    t = sel['time']
    idx = 0
    time.sleep(0.3)
    while loading:
        print(f"\r{get_time()}Loading file {animation[idx]} ", end='', flush=True)
        idx += 1
        if idx == len(animation):
            idx = 0
        time.sleep(t)
    print(f"\r", end='', flush=True)

def exiting():
    """
    Exits program
    """
    global otputdf
    if not otputdf.empty:
        print(f"\n{get_time()}Saving...")
        otputdf.to_csv("output.csv")
        if occurrence and occurrence_res:
            df = pd.DataFrame(occurrence_res, columns=['part'])
            df_counts = df['part'].value_counts().reset_index()
            df_counts.columns = ['part', 'count']
            if not sing:
                df_counts = df_counts[df_counts['count'] > 1]
            df_counts.to_csv("occurrence.csv")
    print(f'{get_time()}done!')
    os._exit(0)

def getbody(message): 
    """
    Gets body of Email -credit: Pippo Ramos
    https://github.com/pippo-sci/Phone-number-from-emails-extractor
    """
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    return body

def extract_domain(input_string):
    """Gets domain from Email field -credit: CatGTP"""
    if input_string == None:
        return None,None
    if not isinstance(input_string, str):
        return None, input_string
    # Find the position of the last '<' and '>' characters
    start_pos = input_string.rfind('<')
    end_pos = input_string.rfind('>')
    if start_pos == -1 and end_pos == -1:
        try: 
            domain = input_string.split('@')[-1]
            return domain,input_string
        except:
            return None, input_string
    
    # Extract the email address using the found positions
    if start_pos < end_pos:
        email = input_string[start_pos + 1:end_pos]
        # Split the email to get the domain part
        try:
            domain = email.split('@')[-1]
            return domain,email
        except:
            None, email



def main(mboxs):
    global otputdf,processing,loading
    flen = len(mboxs)
    c = 0
    txt = ""
    time.sleep(0.3)
    for mbox in mboxs:
        loading = True
        processing = True
        c += 1
        print(f"\n{get_time()}{color.BOLD}File {c} of {flen}.{color.END}")
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        i = 0
        length = len(mbox)
        if length == 0:
            continue
        for message in mbox:
            if loading:
                loading = False
                loading_thread.join()
                print(f"{get_time()}Loaded!                   ")
            if processing:
                sender,email = extract_domain(message['From'])
                a,remail = extract_domain(message['To'])
                go = True
                i += 1
                if not(otputdf.empty):
                    if sender in otputdf[["Domain"]].to_numpy():
                        go = False
                        vals  = otputdf.loc[otputdf['Domain'] == sender, 'Received by'].values
                        if remail not in vals:
                            go = True
                if go:
                    body = getbody(message)
                    check_occurrence(sender)
                    dict = {'Send from':email,"Domain":sender,'Received by':remail, "body":body}
                    otputdf = otputdf._append(dict, ignore_index=True)
                    txt = f"Found {color.BLUE}{color.BOLD}{len(otputdf[["Domain"]])}{color.END} unique domains..."
                print(f"\r{get_time()}Message {i} of {length}.   {txt}",end='', flush=True)

            
        
    
    
print(f"{get_time()}working!")
user_input_thread = threading.Thread(target=handle_user_input)
user_input_thread.start()
mboxs =[]
for file in os.listdir('input'):
    filename = os.fsdecode(file)
    mbox = mailbox.mbox('input/'+filename)
    mboxs.append(mbox)
main(mboxs)
exiting()