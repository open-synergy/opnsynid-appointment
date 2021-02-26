# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = [
        "res.users",
    ]

    allowed_type_ids = fields.Many2many(
        string="Allowed Type",
        comodel_name="appointment.type",
        relation="rel_user_2_appointment_type",
        column1="user_id",
        column2="type_id",
    )
