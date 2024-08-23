import abstra.hooks as ah
from abstra.common import get_persistent_dir
from abstra.connectors import get_access_token
import os
from datetime import datetime
from uuid import uuid4
import hashlib
import hmac
from google_utils import *
from docusign_esign import ApiClient,  ApiException, EnvelopesApi
import base64


def calculate_hmac(raw_body, hook_secret):
    secret_bytes = hook_secret.encode('utf-8')
    body_bytes = raw_body.encode('utf-8')
    hmac_hash = hmac.new(secret_bytes, body_bytes,
                         hashlib.sha256)
    result = base64.b64encode(hmac_hash.digest()).decode('utf-8')
    return result


def create_api_client(base_path, access_token):
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", f"Bearer {access_token}")
    return api_client


def download_document(api_client, account_id, envelope_id, document_id, new_file_path):
    envelopes_api = EnvelopesApi(api_client)
    try:
        document = envelopes_api.get_document(
            account_id=account_id, envelope_id=envelope_id, document_id=document_id)
        with open(new_file_path, "wb") as file:
            with open(document, 'rb') as f:
                file.write(f.read())
        print(f"Signed file downloaded successfully to: {new_file_path}")
    except ApiException as e:
        print(f"Error downloading document: {e}")
        exit(1)


hook_secret = os.getenv("DOCUSIGN_WEBHOOK_SECRET")
ACCOUNT_ID = os.getenv("DOCUSIGN_API_ID")
persistent_dir = get_persistent_dir()
contract_folder = os.path.join(persistent_dir, "liability_statement")
new_contract_folder = os.path.join(
    persistent_dir, "liability_statement_signed")
os.makedirs(new_contract_folder, exist_ok=True)

ACCESS_TOKEN = get_access_token("docusign").token
API_BASE_PATH = os.getenv('API_BASE_PATH', 'https://demo.docusign.net/restapi')
DOCUSIGN_AUTH_SERVER = os.getenv(
    'DOCUSIGN_AUTH_SERVER', 'https://account-d.docusign.com')

# Read webhook data
body, query, headers = ah.get_request()
raw_body, _, __ = ah.get_raw_request()


hmac_value = calculate_hmac(raw_body, hook_secret)

received_hash = headers.get(
    'X-Docusign-Signature-1', '').replace("sha256=", "")


# Verify the HMAC hash
if hmac_value != received_hash:
    print(
        f'Invalid received hash. Expected {hmac_value}, but received {received_hash}')
    exit(1)

envelope_id = body.get('data').get('envelopeId')
api_client = create_api_client(API_BASE_PATH, ACCESS_TOKEN)
envelopes_api = EnvelopesApi(api_client)

try:
    # List envelope documents
    document_list = envelopes_api.list_documents(ACCOUNT_ID, envelope_id)
    documents = document_list.envelope_documents

    for document in documents:
        file_name = document.name
        document_id = document.document_id
        new_file_path = os.path.join(new_contract_folder, file_name)

        download_document(api_client, ACCOUNT_ID, envelope_id,
                          document_id, new_file_path)

        if new_file_path.endswith(".docx"):
            new_file_path = new_file_path.replace(".docx", ".pdf")

        print("Uploading file to Google Drive...")
        upload_to_folder(
            os.getenv("GOOGLE_DRIVE_EQUIPMENTS_CONTRACTS_DOCUMENT_FOLDER"), new_file_path)

except ApiException as e:
    print(f"Exception when calling EnvelopesApi->list_documents: {e}")

ah.send_response(f"[{datetime.now()} - {uuid4()}] Processed")
