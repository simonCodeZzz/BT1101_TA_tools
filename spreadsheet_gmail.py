import random
import pandas as pd
import smtplib
import time
import configparser
import re
import os
import argparse

def send_email(folder, subject):
    # Get the directory of the script and set directory
    script_dir = os.path.dirname(__file__)
    os.makedirs(script_dir, exist_ok=True)
    
    config = configparser.ConfigParser()
    config.read('config.ini')

    # User inputs
    your_email = config.get('user', 'email')
    your_password = config.get('user', 'password')

    # Validate inputs
    if not re.match(r"[^@]+@[^@]+\.[^@]+", your_email):
        print("Invalid email address")
        exit()

    if len(your_password) < 8:
        print("Password is too short")
        exit()

    try:
        # establishing connection with gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(your_email, your_password)

            # reading the spreadsheet
            email_list = pd.read_csv(f'{folder}/emails.csv')

            # getting the names and the emails
            names = email_list['Message']
            emails = email_list['Email']

            # iterate through the records
            total_emails = len(emails)
            sent_emails = 0
            success_emails = []

            for i, email in enumerate(emails):
                # for every record get the name and the email addresses
                name = names[i]

                # the message to be emailed
                message = f"Subject: {subject}\n\n{name}".encode('utf-8')

                # sending the email
                try:
                    server.sendmail(your_email, [email], message)
                    success_emails.append(email)
                    print(f"Email sent to: {email}")
                except smtplib.SMTPException as e:
                    print(f"An error occurred while sending email to {email}: {e}")

                sent_emails += 1
                print(f"{sent_emails} of {total_emails} emails sent")
                time.sleep(random.randint(2, 5)) # avoid overloading the gmail server

        # Save successful emails to Excel file
        success_df = pd.DataFrame({'Email': success_emails})
        success_df.to_excel(f'{folder}/success_emails.xlsx', index=False)
        print(f"{len(success_emails)} emails successfully sent and saved to 'success_emails.xlsx'")

    except smtplib.SMTPAuthenticationError:
        print("Incorrect email address or password")
    except smtplib.SMTPConnectError:
        print("Could not connect to SMTP server")
    except pd.errors.EmptyDataError:
        print("The spreadsheet is empty or could not be read")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send email to students based on student_emails.csv in the specified folder')
    parser.add_argument('folder', type=str, help='Path to the input Excel file')
    parser.add_argument('subject', type=str, help='Subject of the email')
    args = parser.parse_args()

    send_email(args.folder, args.subject)
