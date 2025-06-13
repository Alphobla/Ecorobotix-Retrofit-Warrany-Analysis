# Placeholder script to fetch warranty costs from Odoo.
# This script uses xmlrpc to connect to Odoo and extract data.
# Fill in the ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD environment variables
# before running.

import os
import xmlrpc.client

ODOO_URL = os.environ.get('ODOO_URL')
ODOO_DB = os.environ.get('ODOO_DB')
ODOO_USERNAME = os.environ.get('ODOO_USERNAME')
ODOO_PASSWORD = os.environ.get('ODOO_PASSWORD')

if not all([ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD]):
    raise SystemExit("Please set ODOO_URL, ODOO_DB, ODOO_USERNAME, and ODOO_PASSWORD")

# Common XML-RPC endpoints for Odoo
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
if not uid:
    raise SystemExit("Failed to authenticate with Odoo")
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# Helper for xmlrpc calls
execute_kw = models.execute_kw

# --- External costs from sale orders tagged 'SAV retrofit' ---
# Find the ID of the 'SAV retrofit' tag in 'crm.tag'
tag_ids = execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'crm.tag', 'search',
    [[('name', '=', 'SAV retrofit')]]
)

# Search for sale orders where partner name contains 'Abemec' and tag is set
sale_order_ids = execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'sale.order', 'search',
    [[
        ('partner_id.name', 'ilike', 'Abemec'),
        ('tag_ids', 'in', tag_ids)
    ]]
)

sale_orders = execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'sale.order', 'read', [sale_order_ids],
    {'fields': ['name', 'partner_id', 'amount_untaxed', 'order_line']}
)

external_cost_total = 0.0
for order in sale_orders:
    order_lines = execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'sale.order.line', 'read', [order['order_line']],
        {'fields': ['product_id', 'price_unit', 'product_uom_qty']}
    )
    for line in order_lines:
        line_price = line['price_unit'] * line['product_uom_qty']
        external_cost_total += line_price

print(f"External warranty cost (Abemec): {external_cost_total:.2f}")

# --- Internal costs from accounting entries ---
# This is a placeholder search. Adjust the domain to match your internal accounts.
account_move_line_ids = execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move.line', 'search',
    [[
        ('partner_id.name', 'ilike', 'Abemec'),
        ('name', 'ilike', 'Retrofit')
    ]]
)

account_lines = execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move.line', 'read', [account_move_line_ids],
    {'fields': ['debit', 'credit']}
)

internal_cost_total = sum(line['debit'] - line['credit'] for line in account_lines)

print(f"Internal warranty cost (Abemec): {internal_cost_total:.2f}")
