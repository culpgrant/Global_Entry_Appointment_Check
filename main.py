"""
Python Script to check the Global Enrollment Website to schedule an interview.
If you have found this and are looking for your centers please clone and update the dictionary with your data
Its not perfect it was more to just whip something up quick
"""

import requests
import smtplib
import ssl
import json

# Main Script variables
BASE_SCHEDULE_URL = 'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId='
# Enter your locations
LOCATIONS = {5183: 'Ohare', 1101: 'Rockford', 1198: 'Downtown Chicago'}


def read_secrets(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def format_list_names(data):
    names = []
    # Create the list of location names
    for loc in data:
        # Map the Id to the location name
        name = LOCATIONS[loc['locationId']]
        names.append(name)
    return names

def send_email(data_send, email_data):
    # Formating data for the email
    number_of_appointments = len(data_send)
    list_location_names = format_list_names(data_send)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = email_data['sender_email']
    receiver_email = email_data['receiver_email'] 
    password = email_data['gmail_password']
    message = f"""\
    Subject: Global Entry Appointments

    There are {number_of_appointments} of appointment(s) available at: {list_location_names}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def main():
    # Read in the secret data
    secret_data = read_secrets('secrets.json')

    # Call the API
    # Data returned by the api
    api_data = []

    # Call the Global Enrollment Endpoints to see if there is an appointment available
    for id, name in LOCATIONS.items():
        specific_url = f"{BASE_SCHEDULE_URL}{id}"
        response = requests.get(url=specific_url)
        # Append the data if there is any (we are limiting to only appointment in the api call)
        if len(response.json()) > 0:
            api_data.append(response.json()[0])

    # Only send email if there is data
    if len(api_data) > 0:
        # Send the Email
        send_email(api_data, secret_data)

    return None

if __name__ == "__main__":
   main()