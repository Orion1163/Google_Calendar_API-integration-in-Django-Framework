import os
import django
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings
from httplib2 import Credentials

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Update with your project's settings module
django.setup()

# Scopes required for accessing Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    creds = None

    # Check if token file exists
    if os.path.exists(settings.GOOGLE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(settings.GOOGLE_TOKEN_FILE)

    # If credentials are not valid or do not exist, initiate OAuth2 flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # Path to your OAuth2 credentials file
            creds = flow.run_local_server(port=8000)

        # Save the credentials for the next run
        with open(settings.GOOGLE_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == '__main__':
    main()
