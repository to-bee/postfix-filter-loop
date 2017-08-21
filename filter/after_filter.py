import asyncore
import smtpd
import smtplib
import traceback
import urllib
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import logging

import os

# os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
# django.setup()
import sys

server_addr = '0.0.0.0'
server_port = 10020
forward_addr = '192.168.2.59'
forward_port = 10021

base_rest_endpoint = 'http://django:8000' # docker
# base_rest_endpoint = 'http://0.0.0.0:8000'
email_endpoint = '%s/monitoring/email/' % base_rest_endpoint
log_dir = '/var/postfix_monitoring'
logging.basicConfig(filename='%s/filter.log' % log_dir, level=logging.DEBUG)


class Email:
    def __init__(self, sender, recipient, content_type, reply_to, mime_version, message_id, received, references, user_agent, x_sender, subject, body, x_virus_scanned):
        self.sender = sender
        self.recipient = recipient
        self.content_type = content_type
        self.reply_to = reply_to
        self.mime_version = mime_version
        self.message_id = message_id
        self.received = received
        self.references = references
        self.user_agent = user_agent
        self.x_sender = x_sender
        self.subject = subject
        self.body = body
        self.x_virus_scanned = x_virus_scanned

    def save(self):
        json = {'sender': self.sender,
                'recipient': self.recipient,
                'content_type': self.content_type,
                'reply_to': self.reply_to,
                'mime_version': self.mime_version,
                'message_id': self.message_id,
                'received': self.received,
                'references': self.references,
                'user_agent': self.user_agent,
                'x_sender': self.x_sender,
                'subject': self.subject,
                'body': self.body,
                'x_virus_scanned': self.x_virus_scanned,
                }

        try:
            logging.info('Saving email message at: %s' % email_endpoint)
            request = Request(email_endpoint, urlencode(json).encode())
            json_response = urlopen(request).read().decode()
            logging.info(json_response)
            return json_response
        except urllib.error.URLError as e:
            logging.error('Could not save email')
            logging.error(e, exc_info=True)
            return None


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, origin, sender, recipients, data, **kwargs):
        logging.info('\n')
        try:
            sender.replace('\'', '')
            sender.replace('\"', '')

            # for idx,recipient in enumerate(recipients):
            #     recipients[idx].replace('\'', '')
            #     recipients[idx].replace('\"', '')

            logging.info('Parsing message content')
            map = dict()
            body = str(data)
            attributes = body.replace('\'', '').split('\\n')
            for attribute in attributes:
                # logging.info(attribute)
                tuple = attribute.split(':')
                if len(tuple) == 2:
                    (key, value) = attribute.split(':')
                    map[key.lower()] = value

            logging.info(map)

            recipients_str = ",".join(recipients)
            logging.info('Saving email')
            email = Email(sender=sender,
                          recipient=recipients_str,
                          content_type=map.get('content-type', ''),
                          reply_to=map.get('in-reply-to', ''),
                          mime_version=map.get('mime-version', ''),
                          message_id=map.get('message-id', ''),
                          received=map.get('received', ''),
                          references=map.get('references', ''),
                          user_agent=map.get('user-agent', ''),
                          x_sender=map.get('x-sender', ''),
                          subject=map.get('subject', ''),
                          body=body,
                          x_virus_scanned=True if map.get('x-virus-scanned') is not None else False
                          )
            response = email.save()

            logging.info('Forward email to the queue')
            server = smtplib.SMTP(forward_addr, forward_port)
            # recipients must not contain ip addresses
            server.sendmail(sender, recipients, data)
            server.quit()

            # return '541 Your error'
        except smtplib.SMTPException:
            logging.error('Exception SMTPException')
            pass
        except smtplib.SMTPServerDisconnected:
            logging.error('Exception SMTPServerDisconnected')
            pass
        except smtplib.SMTPResponseException:
            logging.error('Exception SMTPResponseException')
            pass
        except smtplib.SMTPSenderRefused:
            logging.error('Exception SMTPSenderRefused')
            pass
        except smtplib.SMTPRecipientsRefused:
            logging.error('Exception SMTPRecipientsRefused')
            pass
        except smtplib.SMTPDataError:
            logging.error('Exception SMTPDataError')
            pass
        except smtplib.SMTPConnectError:
            logging.error('Exception SMTPConnectError')
            pass
        except smtplib.SMTPHeloError:
            logging.error('Exception SMTPHeloError')
            pass
        except smtplib.SMTPAuthenticationError:
            logging.error('Exception SMTPAuthenticationError')
            pass
        except:
            logging.error('Undefined exception')
            logging.error(traceback.format_exc())

        logging.info('Successful')

        return


server = CustomSMTPServer((server_addr, server_port), None)
asyncore.loop()
