# Inventory Management System

## How It Works

This project includes an inventory management system implemented with Abstra and Python scripts. The system's capabilities include adding, updating, and deleting inventory items, processing expenses, and managing equipment loans. The system integrates with Docusign for document signing and makes use of a custom `google_utils` module for uploading data to Google Drive.

Integrations:

- Docusign
- Google drive
- Pandoc

To customize this template for your team and build a lot more, [book a demonstration here](https://meet.abstra.app/demo?url=template-inventory-management-system).

![An inventory management system workflow built using Abstra](https://github.com/user-attachments/assets/884b687f-b754-46ff-b651-0f190c7ea5d3)

## Initial Configuration

To use this project, some initial configurations are necessary:

1. **Python Version**: Ensure Python version 3.9 or higher is installed on your system.
2. **Integrations**: To connect to Google Drive and DocuSign, this template uses Abstra connectors. To connect, simply open your project in [Abstra Cloud Console](https://cloud.abstra.io/projects/), add the Google Drive and DocuSign connectors, and authorize them.
3. **Environment Variables**: The following environment variables are required for both local development and online deployment:

   - `GOOGLE_DRIVE_INVOICES_FOLDER`: Your Google Drive folder ID for invoices.
   - `DOCUSIGN_WEBHOOK_SECRET`: Secret key for DocuSign webhook verification.
   - `COMPANY_SIGNER_NAME`: Name of the company signer
   - `COMPANY_SIGNER_EMAIL`: Email of the company signer
   - `DOCUSIGN_API_ID`: API ID for DocuSign
   - `DOCUSIGN_AUTH_SERVER`: Authentication server URL for DocuSign
   - `API_BASE_PATH`: Base path for the DocuSign API
   - `GOOGLE_DRIVE_EQUIPMENTS_CONTRACTS_DOCUMENT_FOLDER`: Your Google Drive folder ID for signed contracts.

   For local development, create a `.env` file at the root of the project and add the variables listed above (refer to `.env.examples`). For online deployment, configure these variables in your [environment settings](https://docs.abstra.io/cloud/envvars).

4. **Dependencies**: To install the necessary dependencies for this project, a `requirements.txt` file is provided. This file includes all the required libraries.

   Follow these steps to install the dependencies:

   1. Open your terminal and navigate to the project directory.
   2. Run the following command to install the dependencies from `requirements.txt`:

      ```sh
      pip install -r requirements.txt
      ```
   3. Install Pandoc. To test it locally, you need to install Pandoc. You can do this through various package managers depending on your operating system. Detailed installation instructions are available in the [Pandoc documentation](https://pandoc.org/installing.html).
      

5. **Access Control**: The generated form is protected by default. For local testing, no additional configuration is necessary. However, for cloud usage, you need to add your own access rules. For more information on how to configure access control, refer to the [Abstra access control documentation](https://docs.abstra.io/concepts/access-control).

6. **Database Configuration**: Set up your database tables in Abstra Cloud Tables according to the schema defined in `abstra-tables.json`.

   To automatically create the table schema, follow these steps:

   1. Open your terminal and navigate to the project directory.
   2. Run the following command to install the table schema from `abstra-tables.json`:

      ```sh
      abstra restore
      ```

   For guidance on creating and managing tables in Abstra, refer to the [Abstra Tables documentation](https://docs.abstra.io/cloud/tables).
7. **Local Usage**: To access the local editor with the project, use the following command:

   ```sh
      abstra editor path/to/your/project/folder/
   ```
## General Workflows

To interact with the inventory system (add, update, delete items), process expenses, and manage equipment loans, use the following scripts:

#### Inventory Item Registration

For registering inventory items, use the scripts:

- **inventory_item_registration.py**: Main script for registering inventory items.
- **inventory_item_registration_data_processing.py**: Script responsible for processing inventory item data.

#### Equipment Loan

For managing equipment loans, where a liability statement is generated and sent for signing, use:

- **equipment_loan.py**: Script to manage equipment loans.
- **generate_liability_statement.py**: Script to generate the liability statement. The model for building this document is saved in `Liability Statement for Loaned Equipment Model.docx`.
- **sending_equipment_loan_to_sign.py**: Script to send the liability statement for signing.

#### Equipment Loan Return

For managing the return of loaned equipment, use:

- **equipment_loan_return.py**: Script to manage equipment returns.

#### Depreciation Calculation

For calculating the monthly depreciation of all equipment, use:

- **depreciation_calculation.py**: Script to calculate monthly depreciation.

#### Handling Signed Liability Statements

For processing and handling the signed liability statements received via webhooks, use:

- **process_signed_liability_statement.py**: Script to download and upload signed liability statements to Google Drive.

If you're interested in customizing this template for your team in under 30 minutes, [book a customization session here.](https://meet.abstra.app/demo?url=template-inventory-management-system)
