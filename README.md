# Ecorobotix Retrofit Warranty Analysis

This repository contains a small script to help gather warranty costs from an Odoo instance. It focuses on sale orders tagged **"SAV retrofit"** and accounting entries related to the customer *Abemec*.

## Requirements
- Python 3
- Access to the company Odoo instance with the XML‑RPC API enabled.

## Usage
1. Set the following environment variables with your Odoo credentials:
   - `ODOO_URL` – URL of the Odoo server (e.g. `https://mycompany.odoo.com`)
   - `ODOO_DB` – database name
   - `ODOO_USERNAME` – login username
   - `ODOO_PASSWORD` – password

   On Windows you can make these variables persistent by opening
   **System Properties → Environment Variables** and adding them under *User
   variables*. Alternatively, run the following commands in a Command Prompt:

   ```cmd
   setx ODOO_URL "https://mycompany.odoo.com"
   setx ODOO_DB "mydb"
   setx ODOO_USERNAME "myuser"
   setx ODOO_PASSWORD "mypassword"
   ```
2. Run the script:
   ```bash
   python warranty_analysis.py
   ```
3. The script prints the total **external** warranty cost calculated from relevant sale orders and the **internal** cost from accounting entries. Adjust the search domains in the script if your data model differs.

The current implementation fetches sale order lines without applying any discount so that the value represents the cost of parts before discount.
