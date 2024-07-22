# Inventory Management System

This Python script is designed to process inventory management system, including expenses and equipment loan data. It integrates with the `abstra` library for workflow and table operations and utilizes a custom `google_utils` module for uploading data to Google Drive.

## Initial Configuration

To use this project, some initial configurations are necessary:

1. **Python Version**: Ensure Python version 3.9 or higher is installed on your system.
2. **Service Account Credentials**: Obtain the service account credentials as follows:

   1. Access the [Google Cloud Console](https://console.cloud.google.com/).
   2. Navigate to the **IAM & Admin** section.
   3. Select **Service Accounts**.
   4. Create a new service account or select an existing one.
   5. Generate a new key.
   6. Download the JSON file containing the credentials.

   These credentials are used to authenticate and authorize requests to Google APIs. Save this JSON file to a secure location in your project directory, for example: `./path/to/your/service-account-file.json`

3. **Environment Variables**: Create a `.env` file at the root of the project and add the following variables for your environment:

   ```ini
   GOOGLE_DRIVE_INVOICES_FOLDER="your_google_drive_folder_id"
   GOOGLE_APPLICATION_CREDENTIALS="./path/to/your/service-account-file.json"
   ADM_CLICKSIGN_KEY="your_admin_signer_clicksign_key"
   CLICKSIGN_TOKEN="your_clicksign_key"
   CLICKSIGN_WEBHOOK_SECRET="your_webhook_secret"
   GOOGLE_DRIVE_EQUIPMENTS_CONTRACTS_DOCUMENT_FOLDER="your_google_drive_signed_contract_folder_id"
   ```

4. **Dependencies**: To install the necessary dependencies for this project, a `requirements.txt` file is provided. This file includes all the required libraries.

   Follow these steps to install the dependencies:

   1. Open your terminal and navigate to the project directory.
   2. Run the following command to install the dependencies from `requirements.txt`:

      ```sh
      pip install -r requirements.txt
      ```

5. **Database Configuration**: Set up your database tables in Abstra Cloud Tables according to the schema defined in the [Database Schema](#database-schema) section of this document. Ensure each table is correctly configured to match the application's data structure requirements. For guidance on creating and managing tables in Abstra, refer to the [Abstra Tables documentation](https://docs.abstra.io/cloud/tables).

## Database Schema

The project involves the use of seven different tables within the database. Below are the schemas for each table:

### 1. Depreciation

- `useful_life_months`: Integer, represents the useful life of the equipment in months.
- `equipment_category`: String, the category to which the equipment belongs.
- `residual_value_percentage`: Float, the percentage of the equipment's value that remains after its useful life.

### 2. Equipments

- `description`: String, a brief description of the equipment.
- `serial_number`: String, the unique serial number of the equipment.
- `model`: String, the model of the equipment.
- `brand`: String, the brand of the equipment.

### 3. Inventory Allocations

- `equipment_id`: UUID, foreign key linking to the `equipments` table.
- `user_id`: UUID, the ID of the user to whom the equipment is allocated.
- `start_date`: Date, the start date of the equipment allocation.
- `end_date`: Date, the end date of the equipment allocation (if any).
- `status`: String, the current status of the allocation (e.g., active, returned).

### 4. Inventory Expenses

- `amount`: Integer, the amount of the expense (in cents).
- `invoice_number`: String, the invoice number associated with the expense.
- `supplier_id`: UUID, foreign key linking to the `suppliers` table.
- `is_cash_expense`: Boolean, indicates whether the expense was paid in cash.

### 5. Inventory Transactions

- `equipment_id`: UUID, foreign key linking to the `equipments` table.
- `transaction_type`: String, the type of transaction (e.g., acquisition, disposal).

### 6. Suppliers

- `name`: String, the name of the supplier.
- `contact_email`: String, the contact email of the supplier.

### 7. Team

- `name`: String, the name of the team member.
- `department`: String, the department to which the team member belongs.
- `role`: String, the role of the team member within the organization.
- `address`: String, the address of the team member.
- `email`: String, the email address of the team member.

## General Workflows

To interact with the inventory system (add, update, delete items), process expenses, and manage equipment loans, use the following scripts:

### Inventory Item Registration

For registering inventory items, use the scripts:

- **inventory_item_registration.py**: Main script for registering inventory items.
- **inventory_item_registration_data_processing.py**: Script responsible for processing inventory item data.

### Equipment Loan

For managing equipment loans, where a liability statement is generated and sent for signing, use:

- **equipment_loan.py**: Script to manage equipment loans.
- **generate_liability_statement.py**: Script to generate the liability statement. The model for building this document is saved in `Liability Statement for Loaned Equipment Model.docx`.
- **sending_equipment_loan_to_sign.py**: Script to send the liability statement for signing.

### Equipment Loan Return

For managing the return of loaned equipment, use:

- **equipment_loan_return.py**: Script to manage equipment returns.

### Depreciation Calculation

For calculating the monthly depreciation of all equipment, use:

- **depreciation_calculation.py**: Script to calculate monthly depreciation.

### Handling Signed Liability Statements

For processing and handling the signed liability statements received via webhooks, use:

- **process_signed_liability_statement.py**: Script download and upload signed liability statements to Google Drive.

## How It Works

This project facilitates inventory management, expense processing, and equipment loan handling through automated processes.

## Contributions

Contributions are welcome! If you wish to improve this project, feel free to create a pull request.
