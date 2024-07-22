import abstra.hooks as ah
from abstra.common import get_persistent_dir
import os
from datetime import datetime
from uuid import uuid4
import hashlib
import hmac
import requests

from google_utils import *


def calculate_hmac(raw_body, hook_secret):
    secret_bytes = hook_secret.encode('utf-8')
    body_bytes = raw_body.encode('utf-8')

    hashed = hmac.new(secret_bytes, body_bytes, hashlib.sha256)

    hmac_hex = hashed.hexdigest()

    return hmac_hex


body, query, headers = ah.get_request()
raw_body, _, __ = ah.get_raw_request()


hook_secret = os.getenv("CLICKSIGN_WEBHOOK_SECRET")
hmac_value = calculate_hmac(raw_body, hook_secret)

received_hash = headers['Content-Hmac'].replace("sha256=", "")


if hmac_value != received_hash:
    print(
        f'Invalid received hash. Expected {hmac_value}, but received {received_hash}')
    exit(1)
document = body["document"]

persistent_dir = get_persistent_dir()
contract_folder = os.path.join(persistent_dir, "liability_statement")
new_contract_folder = os.path.join(
    persistent_dir, "liability_statement_signed")
os.makedirs(new_contract_folder, exist_ok=True)

file_path = os.path.join(contract_folder, document["filename"])
new_file_path = os.path.join(new_contract_folder, document["filename"])


req_sig = f"{datetime.now()} - {uuid4()}"
ah.send_response(f"[{req_sig}] Processed")

if os.path.exists(file_path):
    # get signed_file_url and upload in drive
    signed_file_url = document["downloads"]["signed_file_url"]

    # change extension to pdf

    if os.path.exists(new_file_path):
        print(
            f"File {document['filename']} already exists in the persistent dir.")
        exit(0)

    else:
        response = requests.get(signed_file_url)

        if response.status_code == 200:
            if new_file_path.endswith(".docx"):
                new_file_path = new_file_path.replace(".docx", ".pdf")

            with open(new_file_path, "wb") as file:
                file.write(response.content)
            print("Signed file downloaded successfully!")
        else:
            print(
                f"Failed to download the file. Status code: {response.status_code}")
            exit(1)

        print("Uploading file to Google Drive...")
        upload_to_folder(os.getenv(
            "GOOGLE_DRIVE_EQUIPMENTS_CONTRACTS_DOCUMENT_FOLDER"), new_file_path)

else:
    print(f"File {document['filename']} not found in the directory.")
