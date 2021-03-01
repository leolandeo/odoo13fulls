{
    "name": "Generación y Emisión de comprobantes electrónicos XML a SUNAT",
    "author": "Gestión IT",
    "description": "",
    "depends": [
        "base",
        "account",
        "sale", "stock"
    ],
    "category": "invoicing",
    "data": [
        'views/product/view_product_uom.xml',
        'views/sale_order/view_sale_order.xml',
        'views/account/view_account_journal.xml',
        'views/account/view_account_move.xml',
        'views/account/view_acc_inv_factura.xml',
        'views/account/view_acc_inv_boleta.xml',
        'views/account/view_acc_log_status.xml',
        'views/account/view_account_log_status.xml',
        'views/user/view_users.xml',
        'views/stock/view_stock_warehouse.xml',
        'views/company/view_company.xml',
        'data/product_uom.xml',
        'data/tax_group.xml',
        'data/account_journal.xml',
        'security/res_groups.xml'
    ],
    "external_dependencies": {"python": ["signxml"]}
}
