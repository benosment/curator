import logging
import praw
import argparse
import os
import smtplib
from email.generator import Generator
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import StringIO


def parse_args():
    # build the command line parser
    parser = argparse.ArgumentParser(description='get the top 10 posts from the previous week')
    parser.add_argument('subreddit_name',
                        help='subreddit to pull the top 10 posts',
                        action='store')
    return parser.parse_args()


def send_email(subject, body):
    gmail_user = os.environ.get('MAIL_USERNAME')
    gmail_password = os.environ.get('MAIL_PASSWORD')

    if not gmail_user or not gmail_password:
        raise EnvironmentError('invalid user or password for sending mail')

    from_address = ['curator', gmail_user]
    recipient = ['Master', gmail_user]

    print(subject, body)
    # 'alternative' MIME type - HTML and plaintext bundled in one email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '%s' % Header(subject, 'utf-8')
    msg['From'] = '"%s" <%s>' % (Header(from_address[0], 'utf-8'),
                                 from_address[1])
    msg['To'] = '"%s" <%s>' % (Header(recipient[0], 'utf-8'), recipient[1])

    htmlpart = MIMEText(body, 'html', 'UTF-8')
    msg.attach(htmlpart)
    str_io = StringIO()
    gen = Generator(str_io, False)
    gen.flatten(msg)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, str_io.getvalue())
        server.close()
    except smtplib.SMTPException:
        logging.error('Failed to send mail')


args = parse_args()


# get the top 10 posts from the previous week

# TODO - create your own app string for curator

# TODO - what kind of tests can you add?

# TODO - what if the number of posts is less than 10?

# TODO - what if reddit is experiencing a network issue?

# TODO - include a link to the comments [article | comments]

# TODO - email the results

subreddit_name = args.subreddit_name
reddit = praw.Reddit('pycomic')
subreddit = reddit.subreddit(subreddit_name)

# TODO - include which days (i.e. 2/4 - 2/11)
subject = f'Top 10 posts of the week for the {subreddit_name} subreddit'
body = ''
# TODO - can you change this into an list comprehension?
for submission in subreddit.top('week', limit=10):
    body = body + f'{submission.title} - <a href="{submission.url}">Article</a> ' \
           f'<a href="https://www.reddit.com{submission.permalink}">Comments</a><br>'
send_email(subject, body)

