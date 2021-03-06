# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta
from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AppointmentRequest(models.Model):
    _name = "appointment.request"
    _description = "Appointment Request"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "custom.info.mixin",
        "ir.needaction_mixin",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["open"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_policy(self):
        _super = super(AppointmentRequest, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "type_id",
        "appointee_id",
        "date",
        "date_offset",
        "state",
    )
    def _compute_allowed_appointment_ids(self):
        obj_appointment = self.env["appointment.appointment"]
        for document in self:
            result = []
            # if document.type_id and document.date and document.state == "open":
            if document.date and document.state == "open":
                date_min = datetime.strptime(document.date, "%Y-%m-%d")
                date_min = date_min + relativedelta(days=document.date_offset)
                criteria = [
                    ("date", ">=", date_min),
                    ("state", "=", "draft"),
                ]
                if document.type_id:
                    criteria.append(
                        ("type_ids", "in", document.type_id.id),
                    )
                if document.appointee_id:
                    criteria.append(
                        ("appointee_id", "=", document.appointee_id.id),
                    )
                result = obj_appointment.search(criteria).ids
            document.allowed_appointment_ids = result

    name = fields.Char(
        string="# Request",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    title = fields.Char(
        string="Title",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    appointee_id = fields.Many2one(
        string="Appointee",
        comodel_name="res.users",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Request Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_offset = fields.Integer(
        string="Days Offset",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="appointment.type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_appointee_ids = fields.Many2many(
        string="Allowed Appointee on Request",
        comodel_name="res.users",
        related="type_id.allowed_appointee_ids",
        store=False,
    )
    allowed_appointment_ids = fields.Many2many(
        string="Allowed Appointments",
        comodel_name="appointment.appointment",
        compute="_compute_allowed_appointment_ids",
        store=False,
    )
    appointment_id = fields.Many2one(
        string="# Appointment",
        comodel_name="appointment.appointment",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
            "done": [
                ("required", True),
            ],
        },
    )
    appointment_date = fields.Date(
        string="Appointment Date",
        related="appointment_id.date",
        readonly=True,
        store=True,
    )
    appointment_time_slot_id = fields.Many2one(
        string="Appointment Time Slot",
        comodel_name="appointment.time_slot",
        related="appointment_id.time_slot_id",
        store=True,
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "Waiting for Schedulle"),
            ("done", "Schedulled"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    confirm_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
        copy=False,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
        string="Can Force Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.multi
    def action_confirm(self):
        for record in self:
            record.write(record._prepare_confirm_data())
            record.request_validation()

    @api.multi
    def action_open(self):
        for record in self:
            record.write(record._prepare_open_data())

    @api.multi
    def action_done(self):
        for record in self:
            record.write(record._prepare_done_data())
            record._confirm_appointment()

    @api.multi
    def action_cancel(self):
        if self.state == "done":
            self.ensure_one()
            list_partner_ids = [
                self.appointment_id.create_uid.partner_id.id,
                self.appointment_id.appointee_id.partner_id.id,
            ]
            self.appointment_id.write(
                {
                    "partner_id": False,
                    "title": False,
                    "type_id": False,
                    "name": "/",
                    "message_follower_ids": [(6, 0, list_partner_ids)],
                    "state": "draft",
                    "confirm_date": False,
                    "confirm_user_id": False,
                    "open_date": False,
                    "open_user_id": False,
                    "done_date": False,
                    "done_user_id": False,
                    "cancel_date": False,
                    "cancel_user_id": False,
                }
            )
        for record in self:
            record.write(record._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        sequence = self._create_sequence()
        return {
            "state": "open",
            "name": sequence,
        }

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        if self.appointment_id:
            return {
                "state": "done",
                "done_date": fields.Datetime.now(),
                "done_user_id": self.env.user.id,
            }
        else:
            strWarning = _("You have to select appointment first")
            raise UserError(strWarning)

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "appointment_id": False,
        }

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AppointmentRequest, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(AppointmentRequest, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_open()

    @api.multi
    def restart_validation(self):
        _super = super(AppointmentRequest, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    @api.multi
    def _confirm_appointment(self):
        self.ensure_one()
        self.appointment_id.write(
            {
                "type_id": self.type_id.id,
                "partner_id": self.partner_id.id,
                "title": self.title,
                "message_follower_ids": [(6, 0, self.message_follower_ids.ids)],
            }
        )
        self.appointment_id.action_confirm()

    @api.onchange(
        "type_id",
    )
    def onchange_date_offset(self):
        self.date_offset = 0
        if self.type_id:
            self.date_offset = self.type_id.request_date_offset

    @api.onchange(
        "type_id",
    )
    def onchange_appointee_id(self):
        self.appointee_id = False

    @api.constrains(
        "appointment_id",
    )
    def _check_no_duplicate_appointment(self):
        obj_request = self.env["appointment.request"]
        error_msg = _("Appointment is not available")
        for document in self:
            if document.appointment_id:
                criteria = [
                    ("appointment_id", "=", document.appointment_id.id),
                    ("id", "!=", document.id),
                ]
                request_count = obj_request.search_count(criteria)
                if request_count > 0:
                    raise UserError(error_msg)
