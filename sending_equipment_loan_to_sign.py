from docusign_esign import ApiException, ApiClient, EnvelopesApi, Document, Signer, SignHere, Tabs, Recipients, EnvelopeDefinition
import abstra.workflows as aw
from abstra.common import get_persistent_dir
from abstra.connectors import get_access_token
import os
import base64
import dotenv

dotenv.load_dotenv()

# Set initial variables
persistent_dir = get_persistent_dir()
filepath = aw.get_data("output_filepath")

team_data = aw.get_data("team_data")

name = team_data["team_name"]
email = team_data["team_email"]

ACCESS_TOKEN = get_access_token("docusign").token
DOCUSIGN_AUTH_SERVER = os.getenv('DOCUSIGN_AUTH_SERVER')
API_BASE_PATH = os.getenv('API_BASE_PATH')
ACCOUNT_ID = os.getenv("DOCUSIGN_API_ID")


def make_envelope(args):
    with open(filepath, "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode("ascii")

    # Create a document
    document = Document(
        document_base64=base64_file_content,
        name="Liability Statement",
        file_extension="docx",
        document_id="1"
    )

    # Create models for the signers
    signer_1 = Signer(
        email=args["signer_email_1"],
        name=args["signer_name_1"],
        recipient_id="1",
        routing_order="1"
    )
    signer_2 = Signer(
        email=args["signer_email_2"],
        name=args["signer_name_2"],
        recipient_id="2",
        routing_order="2"
    )

    # Create the tabs for the signers
    sign_here_1 = SignHere(
        anchor_string="/sn1/",
        anchor_units="pixels",
        anchor_y_offset="10",
        anchor_x_offset="20"
    )
    sign_here_2 = SignHere(
        anchor_string="/sn2/",
        anchor_units="pixels",
        anchor_y_offset="10",
        anchor_x_offset="20"
    )

    # Add the tab models (including the sign here tab) to the signers
    signer_1.tabs = Tabs(sign_here_tabs=[sign_here_1])
    signer_2.tabs = Tabs(sign_here_tabs=[sign_here_2])

    envelope_definition = EnvelopeDefinition(
        email_subject="Please sign the Liability Statement",
        documents=[document],
        recipients=Recipients(signers=[signer_1, signer_2]),
        status="sent"
    )

    return envelope_definition


args = {
    "signer_email_1": email,
    "signer_name_1": name,
    "signer_email_2": os.getenv("COMPANY_SIGNER_EMAIL"),
    "signer_name_2": os.getenv("COMPANY_SIGNER_NAME")
}

api_client = ApiClient()
api_client.host = API_BASE_PATH
api_client.set_default_header("Authorization", f"Bearer {ACCESS_TOKEN}")

envelope_definition = make_envelope(args)
envelopes_api = EnvelopesApi(api_client)

try:
    results = envelopes_api.create_envelope(
        ACCOUNT_ID, envelope_definition=envelope_definition)
    print(f"Envelope status: {results.status}")
except ApiException as e:
    print(f"Exception when calling EnvelopesApi->create_envelope: {e}")
