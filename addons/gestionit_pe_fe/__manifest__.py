{
    "name": "GIT - Facturación electrónica - SUNAT",
    "author": "Gestión IT",
    "description": "Generación y Emisión de comprobantes electrónicos XML a SUNAT",
    "depends": ["base", "account", "sale_management", "stock", "l10n_pe", "account_debit_note", "gestionit_pe_ubicaciones", "gestionit_pe_consulta_ruc_dni"],
    "category": "invoicing",
    "data": [
        'views/account/menu.xml',
        'views/product/view_product_uom.xml',
        'views/sale_order/view_sale_order.xml',
        'views/account/view_account_journal.xml',
        'views/account/view_account_move.xml',
        'views/account/view_acc_inv_factura.xml',
        'views/account/view_acc_inv_boleta.xml',
        'views/account/view_acc_inv_nota_credito.xml',
        'views/account/view_acc_inv_nota_debito.xml',
        'views/account/view_acc_summary.xml',
        'views/account/view_acc_com_baja.xml',
        'views/account/view_acc_log_status.xml',
        'views/account/view_account_log_status.xml',
        'views/account/view_acc_mis_comprobantes.xml',
        'views/guia_remision/guia_remision_electronica.xml',
        'views/guia_remision/popup_form_seleccion_ubigeo.xml',
        'views/guia_remision/res_partner_destinatario.xml',
        'views/guia_remision/view_catalogo_motivo_traslado.xml',
        'views/guia_remision/view_transporte.xml',
        'views/guia_remision/menu.xml',
        'views/user/view_users.xml',
        'views/stock/view_stock_warehouse.xml',
        'views/company/view_company.xml',
        'views/reportes/external_layout_background_gestionit.xml',
        'views/reportes/report_invoice_document.xml',
        'data/product_uom.xml',
        'data/tax_group.xml',
        'data/account_journal.xml',
        'data/motivo_traslado.xml',
        'data/modalidad_transporte.xml',
        'security/res_groups.xml',
        'cron/account_move_cron.xml',
        'cron/account_summary_cron.xml',
        'cron/comunicacion_baja_cron.xml',
        'cron/guia_remision_cron.xml',
        'cron/validez_comprobante_cron.xml',
    ],
    'application': True,
    "external_dependencies": {"python": ["signxml"]}
}
