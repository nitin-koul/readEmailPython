from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import email
import os #to clear screen using cls command

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
   
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    print("Connected to server.")
    key = input("Enter the key term:") #the mail(most recent one) with this term will be searched
    flag = False
    if not messages:
        print("No messages found.")
    else:
        os.system('cls')
        print("Searching your messages. Please wait...")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
            if(key in msg['snippet'].lower()):
                msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
                mime_msg = email.message_from_bytes(msg_str)
                print(mime_msg[Content-Type][text/plain])
                print('-------------------------------------------------------')
                flag = True
                break
        if(flag==False):
            print("No such message found! :(")
            

if __name__ == '__main__':
    main()