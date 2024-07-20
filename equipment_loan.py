import abstra.forms as af
import abstra.tables as at
import abstra.workflows as aw


def get_teams():
    return at.select("team")

team = [{"label": t["name"], "value": t["id"]} for t in get_teams()]

# Fetch equipments with a return date
free_equipments = at.run("SELECT e.id, e.description, e.serial_number, e.model, e.brand FROM equipments e LEFT JOIN inventory_allocations ia ON e.id = ia.equipment_id WHERE e.status = 'active' AND (ia.equipment_id IS NULL OR NOT EXISTS ( SELECT * FROM inventory_allocations ia WHERE ia.equipment_id = e.id AND ia.status != 'returned'))")

if free_equipments:
    free_equipments_labels = [{"label": e["description"], "value": e["id"]}
                   for e in free_equipments]
else:
    free_equipments_labels = [{"label": "No equipment available", "value": None}]


equipment_page = af.Page().display("Equipment Loan - Input Data", size="large")\
                       .read_date("Loan Date", key="loan_date")\
                       .read_dropdown("Team Member", team, key="team_member")\
                       .read_dropdown("Equipments", free_equipments_labels, key="equipments")\
                       .run("Loan Equipment")


# add the loaned equipment to the database
if equipment_page.get("equipments"):
    loaned_equipment_team_member = at.select("team", where={"id": equipment_page.get("team_member")})[0]

    equipment_data = [equipment for equipment in free_equipments if equipment["id"] == equipment_page.get("equipments")][0]
    equipment_description = f"{equipment_data['description']} - serial number: {equipment_data['serial_number']}, model: {equipment_data['model']}, brand: {equipment_data['brand']}"


    aw.set_data("team_data", {
        "team_name": loaned_equipment_team_member["name"],
        "team_address": loaned_equipment_team_member["address"],
        "team_email": loaned_equipment_team_member["email"]
    })

    aw.set_data("equipment_description",
                {
                    "equipment_description": equipment_description
                })

    formatted_date = equipment_page.get("loan_date").strftime('%Y-%m-%d')
    at.insert("inventory_allocations", {
        "equipment_id": equipment_page.get("equipments"),
        "user_id": equipment_page.get("team_member"),
        "start_date": formatted_date,
        "status": "loaned"
    })
    at.insert("inventory_transactions", {
        "equipment_id": equipment_page.get("equipments"),
        "transaction_type": "loan"
    })
