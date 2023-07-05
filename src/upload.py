from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = service_account.Credentials.from_service_account_file(
        key_file_location
    )

    scoped_credentials = credentials.with_scopes(scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=scoped_credentials)

    return service


def upload_basic():
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    see scopes in:

    https://developers.google.com/drive/api/guides/api-specific-auth
    """
    scope = "https://www.googleapis.com/auth/drive"
    key_file_location = '.secrets/gdrive.json'
    # creds, _ = google.auth.default()

    try:
        # create drive api client
        # service = build("drive", "v3", credentials=creds)
        # Authenticate and construct service.
        service = get_service(
            api_name='drive',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)



        file_metadata = {"name": "download.jpeg"}
        media = MediaFileUpload("download.jpeg", mimetype="image/jpeg")
        # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("id")


if __name__ == "__main__":
    upload_basic()
