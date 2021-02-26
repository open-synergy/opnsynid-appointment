# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class AppointmentType(models.Model):
    _name = "appointment.type"
    _description = "Appointment Type"

    name = fields.Char(
        string="Type",
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
    note = fields.Text(
        string="Note",
    )
    appointment_sequence_id = fields.Many2one(
        string="Appointment Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    allowed_appointee_ids = fields.Many2many(
        string="Allowed Appointee",
        comodel_name="res.users",
        relation="rel_user_2_appointment_type",
        column1="type_id",
        column2="user_id",
    )
    appointment_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Appointment",
        comodel_name="res.groups",
        relation="rel_appointment_type_confirm_appointment",
        column1="type_id",
        column2="group_id",
    )
    appointment_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Appointment",
        comodel_name="res.groups",
        relation="rel_appointment_type_restart_approval_appointment",
        column1="type_id",
        column2="group_id",
    )
    appointment_start_grp_ids = fields.Many2many(
        string="Allow To Start Appointment",
        comodel_name="res.groups",
        relation="rel_appointment_type_start_appointment",
        column1="type_id",
        column2="group_id",
    )
    appointment_finish_grp_ids = fields.Many2many(
        string="Allow To Finish Appointment",
        comodel_name="res.groups",
        relation="rel_appointment_type_finish_appointment",
        column1="type_id",
        column2="group_id",
    )
    appointment_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Appointment",
        comodel_name="res.groups",
        relation="rel_appointment_type_cancel_appointment",
        column1="type_id",
        column2="group_id",
    )
    appointment_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Appointment",
        comodel_name="res.groups",
        relation="rel_appointment_type_restart_appointment",
        column1="type_id",
        column2="group_id",
    )
