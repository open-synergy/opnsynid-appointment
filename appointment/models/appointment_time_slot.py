# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class AppointmentTimeSlot(models.Model):
    _name = "appointment.time_slot"
    _description = "Appointment Time Slot"

    name = fields.Char(
        string="Time Slot",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    time_start = fields.Float(
        string="Start",
        required=True,
    )
    time_end = fields.Float(
        string="End",
        required=True,
    )
    note = fields.Text(
        string="Note",
    )
