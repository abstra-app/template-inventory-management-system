import abstra.tables as at 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser

def calculate_monthly_depreciation(equipment, date):
    '''
    Calculate the monthly depreciation value for each equipment category using the straight line method.
    
    Parameters:
    equipment (dict): The equipment information.
    date (datetime): The current date to calculate the depreciation.
    
    Returns:
    int: The monthly depreciation value in the smallest currency unit (e.g., cents for USD).
    '''
    # Fetch relevant details from the database using the provided IDs
    depreciation_id = equipment["depreciation_id"]
    depreciation = at.select("depreciation", where={"id": depreciation_id})[0]
    useful_life = depreciation["useful_life_months"]
    residual_value_percentage = depreciation["residual_value_percentage"]

    equipment_expense_id = equipment["expense_id"]
    equipment_expense = at.select("inventory_expenses", where={"id": equipment_expense_id})[0]
    equipment_cost = equipment_expense["amount"]  # Assume this is already in the smallest currency unit (e.g., cents)
    equipment_purchase_date = parser.parse(equipment_expense["created_at"])

    # Calculate the number of months and days since the equipment was purchased
    purchase_date = datetime(equipment_purchase_date.year, equipment_purchase_date.month, equipment_purchase_date.day)
    delta = relativedelta(date, purchase_date)
    months_since_purchase = delta.years * 12 + delta.months
    days_since_purchase = (date - purchase_date).days

    # Calculate depreciation
    if months_since_purchase >= useful_life:
        return 0
    else:
        # Straight-line depreciation formula for monthly depreciation
        monthly_depreciation = (equipment_cost - (residual_value_percentage / 100 * equipment_cost)) / useful_life
        
        if months_since_purchase == 0:
            # Calculate proportional depreciation if less than a month since purchase
            daily_depreciation = monthly_depreciation / 30  # Approximates a month as 30 days
            return round(daily_depreciation * days_since_purchase)
        else:
            return round(monthly_depreciation)

# Calculate the monthly depreciation for each equipment
equipments = at.select("equipments")
current_date = datetime.today()
for equipment in equipments:
    monthly_depreciation = calculate_monthly_depreciation(equipment, current_date)
    at.insert("inventory_expenses", 
              {
              "amount": monthly_depreciation,
              "created_at": current_date,
              "is_cash_expense": False
            })
    
print(f"Monthly depreciation calculated for {len(equipments)} equipments")