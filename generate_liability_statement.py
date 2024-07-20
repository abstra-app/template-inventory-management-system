import abstra.tables as at
import abstra.workflows as aw
from abstra.common import get_persistent_dir
from datetime import datetime, date
import os

import re
from docx import Document
from docxtpl import DocxTemplate


REGEX = r"\{\{(.*?)\}\}"
persistent_dir = get_persistent_dir()


def create_new_doc_with_tags(tags_values_dict, filepath):
    doc = DocxTemplate(filepath)
    context = tags_values_dict
    try:
        doc.render(context)
    except Exception as e:
        problematic_tags = [k for k in context.keys() if k in str(e)]
        print(
            f"Error: {e}. Please check the following tags: {problematic_tags}")

    doc.save(filepath)

    return filepath


def generate_document(file_response, team_member_name, contract_folder, contract_data={}):

    filename = f"{date.today().strftime('%Y%m%d')}_{team_member_name}"
    filename += ".docx"

    filepath = os.path.join(contract_folder, f"{filename}")

    with open(filepath, "wb") as out_file:
        out_file.write(file_response)

    doc = Document(filepath)

    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    tags = re.findall(REGEX, text)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell_tags = re.findall(REGEX, cell.text)
                if cell_tags:
                    tags.append(cell_tags[0])

    tags_dict = dict.fromkeys(tags)
    tags_original_list = list(tags_dict.keys())
    tags_original = [t.strip() for t in tags_original_list]

    print(tags_original)
    # for inputs in tags_with_underscores:

    tags_response = {}

    tags_response.update(contract_data)

    output_filepath = create_new_doc_with_tags(
        tags_response, filepath)

    return output_filepath


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
    'equipment_description': equipment_description
}

filepath = f"./Liability Statement for Loaned Equipment Model.docx"
contract = open(filepath, 'rb').read()

output_filepath = generate_document(
    contract, name, contract_folder, contract_data)

aw.set_data("output_filepath", output_filepath)
