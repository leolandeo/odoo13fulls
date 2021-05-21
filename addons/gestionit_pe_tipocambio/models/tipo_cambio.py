import odoo
import requests
from odoo import api, models, fields
from datetime import date
import datetime
import json
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)


class Tipocambio(models.Model):
    _inherit = "res.currency.rate"

    fecha = fields.Date("Fecha")
    cambio_compra = fields.Float("Compra", digits=(1, 3))
    cambio_venta = fields.Float("Venta", digits=(1, 3))

    def actualizar_ratio_compra_venta(self, fecha=False):
        currency_usd = self.env['res.currency'].search([['name', '=', 'USD']])
        user_id = self.env.context.get('uid', False)

        # if user_id:
        user = self.env["res.users"].sudo().browse(user_id)
        token = user.company_id.api_migo_token
        if not fecha:
            ruta = "exchange/latest"
            data = {
                "token": token
            }
        else:
            ruta = "exchange/date"
            data = {
                "token": token,
                "fecha": fecha
            }
        url = user.company_id.api_migo_endpoint + ruta

        try:
            headers = {
                'Content-Type': 'application/json'
            }

            res = requests.request(
                "POST", url, headers=headers, data=json.dumps(data))
            res = res.json()

            if res.get("success", False):
                tipo_cambio = float(res.get("precio_venta", False))
                tipo_cambio = 1/tipo_cambio if tipo_cambio != 0.0 else 0.0
                fecha_cambio = res.get("fecha", False)
                return self.env['res.currency.rate'].create({
                    'name': fecha_cambio,
                    'currency_id': currency_usd.id,
                    'rate': tipo_cambio,
                    'fecha': date.today(),
                    'cambio_compra': float(res.get("precio_compra", False)),
                    'cambio_venta': float(res.get("precio_venta", False))
                })

            return None
        except Exception as e:
            return None


class invoice(models.Model):
    _inherit = "account.move"

    tipo_cambio = fields.Float(string="T/C", digits=(1, 3))
    fecha_cambio = fields.Date(string="Fecha de cambio")

    @api.onchange("invoice_date")
    def _change_fecha_cambio(self):
        self.fecha_cambio = self.invoice_date

    @api.constrains('tipo_cambio')
    def _check_tipo_cambio(self):
        for record in self:
            if record.tipo_cambio <= 0:
                raise ValidationError(
                    "Valor del tipo de Cambio incorrecto. Debe actualizar la fecha de facturación.")

    @api.onchange("invoice_date", "fecha_cambio")
    def get_ratio(self):
        if self.fecha_cambio:
            rate_obj = self.env['res.currency.rate']
            rate = rate_obj.search([('name', "=", self.fecha_cambio)])

            if rate.exists():
                if self.type == "in_invoice" or self.type == "in_refund":
                    self.tipo_cambio = rate[0].cambio_venta

                if self.type == "out_invoice" or self.type == "out_refund":
                    self.tipo_cambio = rate[0].cambio_compra
            else:
                self.fecha_cambio = self.fecha_cambio + \
                    datetime.timedelta(days=-1)
                self.get_ratio()
                # _logger.info(self.fecha_cambio)
                # current_date_temp = datetime.datetime.strptime(
                #     str(self.fecha_cambio), "%Y-%m-%d")
                # newdate = current_date_temp + datetime.timedelta(days=-1)
                # self.get_ratio(newdate)
                # else:
                #     if fecha:
                #         gr = rate_obj.actualizar_ratio_compra_venta(str(fecha))
                #     else:
                #         gr = rate_obj.actualizar_ratio_compra_venta(
                #             str(self.fecha_cambio))

                #     _logger.info(gr)
                #     if gr is None:
                #         current_date_temp = datetime.datetime.strptime(
                #             str(self.fecha_cambio), "%Y-%m-%d")
                #         newdate = current_date_temp + datetime.timedelta(days=-1)
                #         self.get_ratio(newdate)
