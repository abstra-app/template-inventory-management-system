import abstra.forms as af
import abstra.workflows as aw
import abstra.tables as at
from datetime import datetime

suppliers = [{"label": s["name"], "value": s["id"]} for s in at.select("suppliers")]
depreciation_categories = [{"label": d["equipment_category"], "value": d["id"]} for d in at.select("depreciation")]

expense_date = af.Page().display("Inventory Registration - Expense data", size="large")\
                             .read_currency("Amount", key="amount")\
                             .read("Invoice Number", key="invoice_number")\
                             .read_date("Expense Date", key="expense_date")\
                             .read_dropdown("Supplier", suppliers, key="supplier_id")\
                             .read_file("Upload Invoice", key="invoice")\
                            
inventory_date = af.Page().display("Inventory Registration - Inventory data", size="large")\
                          .read("Item Description", key="item_description")\
                          .read_dropdown("Equipment Item Category (For depreciation)", depreciation_categories, key="depreciation_id")\
                          .read("Model", key="model")\
                          .read("Serial Number", key="serial_number")\
                          .read("Brand", key="brand")\
                          .read_checkbox("Will this equipment be immediately loaned out?", required=False, key="equipment_loan")\
                          

inventory = af.run_steps([expense_date, inventory_date])


if inventory["equipment_loan"]:
    team = [{"label": s["name"], "value": s["id"]} for s in at.select("team")]

    equipment_loan_page = af.Page().display("Inventory Registration - Equipment Loan data", size="large")\
                                    .read_date("Loan Start Date", key="loan_start_date")\
                                    .read_dropdown("Team member", team, key="team_member_id")\
                                    .run()
    
    aw.set_data("equipment_loan_data", {
        "team_member_id": equipment_loan_page["team_member_id"],
        "loan_start_date": datetime.strftime(equipment_loan_page["loan_start_date"], "%Y-%m-%d")
    })

invoice_path = inventory["invoice"].file.name                        


aw.set_data("inventory_data", {
    "amount": inventory["amount"],
    "invoice_number": inventory["invoice_number"],
    "expense_date": datetime.strftime(inventory["expense_date"], "%Y-%m-%d"),
    "supplier_id": inventory["supplier_id"],
    "item_description": inventory["item_description"],
    "model": inventory["model"],
    "serial_number": inventory["serial_number"],
    "brand": inventory["brand"],
    "depreciation_id": inventory["depreciation_id"],
    "invoice_path": invoice_path
})

