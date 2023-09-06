from odoo import api, fields, models
from odoo.exceptions import ValidationError

# Librerias Necesarias
import gspread
import base64
import tempfile
import os
import json


##

class GoogleSheetsSync(models.Model):
    _name = "googlesheets.sync"
    _rec_name = "name"
    _order = "id asc"

    reference = fields.Char(string="Referencia")
    name = fields.Char(string="Nombre del Archivo", required=True)
    sheet_name = fields.Char(string="Nombre de la Hoja", required=True)

    model_id = fields.Many2one('ir.model', 'Modelo a Actualizar', ondelete='cascade', required=True)
    json = fields.Binary(string="Credenciales JSON", required=True)
    active = fields.Boolean(string="Activo")

    description = fields.Text(string="Descripción")

    def SyncGoogleSheets(self):
        for rec in self:
            if rec.json and rec.active:
                try:
                    credentials_data = base64.decodestring(rec.json)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
                        temp_file.write(credentials_data)

                    credentials_path = temp_file.name
                    gc = gspread.service_account(filename=credentials_path)
                    sh = gc.open(rec.name)
                    wks = sh.worksheet(rec.sheet_name)
                    all_values_wks = wks.get_all_values()
                    selected_model = self.env[rec.model_id.model]
                    count = 1
                    claves = all_values_wks[0]
                    valores = all_values_wks[1:]
                    list_json = []

                    for lista_valor in valores:
                        json2 = {}
                        for i, key in enumerate(claves):
                            valor = lista_valor[i]
                            json2[key] = valor

                        list_json.append(json2)

                    #Armando domain
                    for diccionario in list_json:
                        wksA1 = wks.acell("A1").value

                        record_created = selected_model.search([(wksA1, '=', diccionario[wksA1])])
                        if not record_created:
                            selected_model.create(diccionario)
                        else:
                            record_created.write(diccionario)



                except Exception as e:
                    raise ValidationError(e)
                    pass

                finally:
                    os.unlink(credentials_path)
