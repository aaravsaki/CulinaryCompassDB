from email.message import EmailMessage
import ssl
import smtplib
import menu_scrape
# smtp is simple mail transfer protocol :)

def _to_string(file: str):
    f = open(file, 'r')
    result = ''
    for line in f.read():
        result += line
    
    f.close()
    return result


def _extract_menus():
    menu_scrape.main()

    menus = _to_string("BrandywineMenu.txt") + '\n\n' + _to_string("AnteateryMenu.txt")
    return menus


def send():
    sender = "brandonhoang7541@gmail.com"
    password = "nhad rahl ptsc qbsz"

    receiver = 'marig10058@javnoi.com'

    topic = "Don't forget to eat breakfast!"
    content = _extract_menus()

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['subject'] = topic
    em.set_content(content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())

send()
