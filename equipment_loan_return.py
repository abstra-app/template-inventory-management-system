import abstra.forms as af
import abstra.tables as at


def get_teams():
    return at.select("team")


def get_equipments_render(partial):
    equipments_list = at.run("SELECT e.description, ia.equipment_id, ia.id FROM inventory_allocations ia INNER JOIN equipments e ON ia.equipment_id = e.id WHERE ia.user_id = $1 AND ia.status = 'loaned'", [
        partial.get("team_member")])


    equipments = [{"label": e["description"], "value": {
        "equipment_loan_id": e["id"], "equipment_id": e["equipment_id"]}} for e in equipments_list]
    if equipments_list == []:
        equipments = [{"label": "No equipments to return", "value": None}]

    return af.Page().read_dropdown("Equipments", equipments, key="equipments")


team = [{"label": t["name"], "value": t["id"]} for t in get_teams()]

equipment_return_page = af.Page().display("Equipment Return - Input Data", size="large")\
    .read_date("Return Date", key="return_date")\
    .read_dropdown("Team Member", team, key="team_member")\
    .reactive(get_equipments_render)\
    .run("Send")

if equipment_return_page.get("equipments") is not None:
    formatted_date = equipment_return_page.get(
        "return_date").strftime('%Y-%m-%d')
    at.update("inventory_allocations",
              set={"status": "returned",
                   "end_date": formatted_date},
              where={"id": equipment_return_page.get("equipments")["equipment_loan_id"]}
    )
    at.insert("inventory_transactions", {
        "equipment_id": equipment_return_page.get("equipments")["equipment_id"],
        "transaction_type": "return"
    })
