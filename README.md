# Inventory Management System

This project includes an inventory management system implemented with Abstra and Python scripts. The system's capabilities include adding, updating, and deleting inventory items, processing expenses, and managing equipment loans. The system integrates with Docusign for document signing and makes use of a custom `google_utils` module for uploading data to Google Drive.

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

3. **Environment Variables**

   The following environment variables are required for both local development and online deployment:

   - `GOOGLE_DRIVE_INVOICES_FOLDER`: Your Google Drive folder ID for invoices.
   - `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google service account JSON file.
   - `DOCUSIGN_WEBHOOK_SECRET`: Secret key for DocuSign webhook verification.
   - `DOCUSIGN_CLIENT_ID`: Client ID for DocuSign API.
   - `DOCUSIGN_CLIENT_SECRET`: Client secret for DocuSign API.
   - `DOCUSIGN_ACCESS_TOKEN`: Access token for DocuSign API.
   - `COMPANY_SIGNER_NAME`: Name of the company signer
   - `COMPANY_SIGNER_EMAIL`: Email of the company signer
   - `DOCUSIGN_API_ID`: API ID for DocuSign
   - `DOCUSIGN_AUTH_SERVER`: Authentication server URL for DocuSign
   - `API_BASE_PATH`: Base path for the DocuSign API
   - `GOOGLE_DRIVE_EQUIPMENTS_CONTRACTS_DOCUMENT_FOLDER`: Your Google Drive folder ID for signed contracts.

   For local development, create a `.env` file at the root of the project and add the variables listed above. For online deployment, configure these variables in your [environment settings](https://docs.abstra.io/cloud/envvars).


5. **Dependencies**: To install the necessary dependencies for this project, a `requirements.txt` file is provided. This file includes all the required libraries.

   Follow these steps to install the dependencies:

   1. Open your terminal and navigate to the project directory.
   2. Run the following command to install the dependencies from `requirements.txt`:

      ```sh
      pip install -r requirements.txt
      ```

6. **Database Configuration**: Set up your database tables in Abstra Cloud Tables according to the schema defined in the [Database Schema](#database-schema) section of this document. Ensure each table is correctly configured to match the application's data structure requirements. For guidance on creating and managing tables in Abstra, refer to the [Abstra Tables documentation](https://docs.abstra.io/cloud/tables).

## Database Schema

The project involves the use of seven different tables within the database. Below are the schemas for each table:

#### 1. Depreciation

  | useful_life_months |  equipment_category | residual_value_percentage |
  | :-: | :-: | :-: |
  | ```int``` | ```str``` | ```float``` |

#### 2. Equipments

  | description | serial_number | model | brand |
  | :-: | :-: | :-: | :-: |
  | ```str``` | ```str``` | ```str``` | ```str``` |

#### 3. Inventory Allocations

  | equipment_id | user_id | start_date | end_date | status |
  | :-: | :-: | :-: | :-: | :-: |
  | ```UUID``` | ```UUID``` | ```date``` | ```date``` | ```str``` |

#### 4. Inventory Expenses

  | amount | invoice_number | supplier_id | is_cash_expense |
  | :-: | :-: | :-: | :-: |
  | ```int``` | ```str``` | ```UUID``` | ```bool``` |

#### 5. Inventory Transactions

  | equipment_id | transaction_type |
  | :-: | :-: |
  | ```UUID``` | ```str``` |

#### 6. Suppliers

  | name | contact_email |
  | :-: | :-: |
  | ```str``` | ```str``` |

#### 7. Team

  | name | email |
  | :-: | :-: |
  | ```str``` | ```str``` |

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

## How It Works

This project facilitates inventory management, expense processing, and equipment loan handling through automated processes.

## Contributions

Contributions are welcome! If you wish to improve this project, feel free to create a pull request.
