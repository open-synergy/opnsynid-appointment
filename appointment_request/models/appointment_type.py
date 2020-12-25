# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class AppointmentType(models.Model):
    _name = "appointment.type"
    _inherit = "appointment.type"

    request_sequence_id = fields.Many2one(
        string="Appointment Request Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    request_date_offset = fields.Integer(
        string="Appointment Request Date Offset",
        default=1,
    )
    appointment_request_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Appointment Request",
        comodel_name="res.groups",
        relation="rel_appointment_type_confirm_appointment_request",
        column1="type_id",
        column2="group_id",
    )
    appointment_request_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Appointment Request",
        comodel_name="res.groups",
        relation="rel_appointment_type_restart_approval_appointment_request",
        column1="type_id",
        column2="group_id",
    )
    appointment_request_done_grp_ids = fields.Many2many(
        string="Allow To Force Finish Appointment Request",
        comodel_name="res.groups",
        relation="rel_appointment_type_finish_appointment_request",
        column1="type_id",
        column2="group_id",
    )
    appointment_request_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Appointment Request",
        comodel_name="res.groups",
        relation="rel_appointment_type_cancel_appointment_request",
        column1="type_id",
        column2="group_id",
    )
    appointment_request_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Appointment Request",
        comodel_name="res.groups",
        relation="rel_appointment_type_restart_appointment_request",
        column1="type_id",
        column2="group_id",
    )
