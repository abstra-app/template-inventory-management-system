import os
from datetime import datetime, date
from docx import Document
from docxtpl import DocxTemplate
import abstra.workflows as aw
from abstra.common import get_persistent_dir
import pypandoc
import shutil

persistent_dir = get_persistent_dir()
REGEX = r"\{\{(.*?)\}\}"


def create_new_doc_with_tags(context, template_path, output_path):
    doc = DocxTemplate(template_path)
    try:
        doc.render(context)
        doc.save(output_path)

        docx_doc = Document(output_path)
        docx_doc.save(output_path)
        print(f"Succesfully rendered and saved document: {output_path}")
    except Exception as e:
        problematic_tags = [k for k in context.keys() if k in str(e)]
        print(
            f"Error: {e}. Please check the following tags: {problematic_tags}")
        return None
    return output_path


def convert_with_pandoc(input_path):
    try:
        # Check if Pandoc is installed on the system
        if not shutil.which('pandoc'):
            print(
                "Error: Pandoc not found. Make sure Pandoc is installed and accessible through the PATH.")
            return None

        # Check if the input file exists
        if not os.path.isfile(input_path):
            print(f"Error: Input file '{input_path}' does not exist.")
            return None

        final_output_path = input_path.replace('.docx', '_converted.docx')

        # Try to convert the file using pypandoc
        try:
            pypandoc.convert_file(input_path, 'docx',
                                  outputfile=final_output_path)
        except RuntimeError as e:
            print(f"Error converting document with Pandoc: {e}")
            return None

        # Check if the output file was created
        if not os.path.isfile(final_output_path):
            print(
                f"Error: Conversion failed, output file not created: {final_output_path}")
            return None

        print(
            f"Successfully converted and saved document: {final_output_path}")
        return final_output_path
    except Exception as e:
        print(f"Unexpected error during conversion: {e}")
        return None


def generate_document(file_response, team_member_name, contract_folder, contract_data={}):
    filename = f"{date.today().strftime('%Y%m%d')}_{team_member_name}.docx"
    filepath = os.path.join(contract_folder, filename)
    with open(filepath, "wb") as out_file:
        out_file.write(file_response)
    intermediate_path = create_new_doc_with_tags(
        contract_data, filepath, filepath)
    if intermediate_path is not None:
        final_path = convert_with_pandoc(intermediate_path)
        return final_path
    return None


contract_folder = f"{persistent_dir}/liability_statement"
if not os.path.exists(contract_folder):
    os.makedirs(contract_folder)


team_data = aw.get_data("team_data")
equipment_description = aw.get_data("equipment_description")

name = team_data["team_name"]
address = team_data["team_address"]
email = team_data["team_email"]

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

current_date = datetime.now()
current_day = current_date.strftime("%d")
current_month = current_date.strftime("%m")
current_month = months[int(current_month) - 1]
current_year = current_date.strftime("%Y")
current_date_str = f"{current_year}-{current_month}-{current_day}"


contract_data = {
    'liability_date_statement': current_date_str,
    'borrower_name': name,
    'borrrower_address': address,
    'equipment_description': equipment_description["equipment_description"]
}

filepath = f"./Liability Statement for Loaned Equipment Model.docx"
contract = open(filepath, 'rb').read()

output_filepath = generate_document(
    contract, name, contract_folder, contract_data)

aw.set_data("output_filepath", output_filepath)
