import requests


def send_email(subject: str, content: str) -> None: 
        recipient = 'technotransllc@mail.ru'
        ip = '5.35.84.189'
        url = 'https://sendemail.space/send-email/'
        data = {
            'recipient': recipient, 
            'subject': subject, 
            'content': content,
            'ip': ip,
        }
        response = requests.post(url, data=data) 