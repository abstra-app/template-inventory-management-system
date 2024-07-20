
import pandas as pd
import os

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_to_folder(folder_id, filepath):
    """Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded
    """
    creds, _ = google.auth.default()

    filename = os.path.basename(filepath)

    try:
        service = build('drive', 'v3', credentials=creds)

        folder_id = folder_id
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(filepath, resumable=True)

        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')
