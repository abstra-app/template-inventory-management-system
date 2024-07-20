import abstra.workflows as aw
import abstra.tables as at
from google_utils import upload_to_folder

import os

inventory = aw.get_data("inventory_data")
equipment_loan_data = aw.get_data("equipment_loan_data")


# Add the expense data to the database
expense_id = at.insert("inventory_expenses", 
                {
                    "amount": inventory["amount"],
                    "invoice_number": inventory["invoice_number"],
                    "created_at": inventory["expense_date"],
                    "supplier_id": inventory["supplier_id"]
                })

# Add the equipment data to the database
equipment_id = at.insert("equipments", 
          {
              "description": inventory["item_description"],
              "model": inventory["model"],
              "serial_number": inventory["serial_number"],
              "brand": inventory["brand"],
              "depreciation_id": inventory["depreciation_id"],
              "expense_id": expense_id["id"]
          })

if equipment_loan_data:
    # Add the equipment loan data to the database
    at.insert("inventory_allocations", 
              {
                  "equipment_id": equipment_id["id"],
                  "user_id": equipment_loan_data["team_member_id"],
                  "start_date": equipment_loan_data["loan_start_date"],
                  "status": "loaned"
              })
    
    at.insert("inventory_transactions",
                {
                    "equipment_id": equipment_id["id"],
                    "transaction_type": "loan"
                })
              
# Add file to google drive
folder_id = os.getenv("GOOGLE_DRIVE_INVOICES_FOLDER")
invoice_filepath = inventory["invoice_path"]
upload_to_folder(folder_id, invoice_filepath)