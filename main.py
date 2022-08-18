from config import login, password
import time
import requests
import imaplib
import email

get_code_link = 'https://api.step.app/v1/auth/otp-code?email='
send_code_link = 'https://api.step.app/v1/auth/token?email=&code='

with open('emails.txt', 'r') as f:
    emails = f.readlines()

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI2MjdiOGQ1ZDdkMzg2MzZmYzA4NzZmNTYiLCJleHAiOjE2NTI4NjkwODV9.mQtLiRjk3Uk-rbnDPO_aVnBQzo4HqWFXz9-mUl8Vmw4',
    'Connection': 'keep-alive',
    'Content-Length': '23',
    'Content-Type': 'application/json',
    'Host': 'api.step.app',
    'Origin': 'https://app.step.app',
    'Referer': 'https://app.step.app/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',

}

data = {
    "referrer": "CRNZTZT0"
}

proxies = {
        'http': 'http://KXzsYw:FPQWQE@45.142.116.71:8000',
        'https': 'http://KXzsYw:FPQWQE@45.142.116.71:8000',
    }

def get_code():
    code = ''
    imap_server = 'imap.gmail.com'
    email_address = login
    email_password = password

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, email_password)
    print('Login was successful!')

    imap.select('Inbox')
    _, msgnums = imap.search(None, '(FROM "StepApp")')

    for msgnum in msgnums[0].split():
        _, data = imap.fetch(msgnum, "(RFC822)")

        message = email.message_from_bytes(data[0][1])
        # print(f'Message from: {message.get("From")}')
        # print(f'Message date: {message.get("Date")}')
        # print("Content:")
        code = str(message.get_payload(decode=True)).split(':')[1][1:-5:]

    return code


def verif(email_add):
    session = requests.session()
    session.headers.update(headers)
    session.get('https://app.step.app?r=CRNZTZT0', proxies=proxies)
    time.sleep(1)
    response = session.get(f'{get_code_link + email_add}', proxies=proxies)
    if response.text == 'OK':
        print("Code was sended")
    time.sleep(10)
    code = get_code()
    print(code)
    time.sleep(1)
    send_code = session.get(f'https://api.step.app/v1/auth/token?email={email_add}&code={code}', proxies=proxies).json()
    token = send_code["access"]["token"]
    print(token)
    headers["Authorization"] = f'Bearer {token}'
    print(headers)
    session.headers.update(headers)
    time.sleep(2)
    print(session.patch(url='https://api.step.app/v1/user/me', data=data, proxies=proxies))

    print("Cool!!!")

def main():
    for email in emails:
        verif(email[:-1:])


if __name__ == "__main__":
    main()
