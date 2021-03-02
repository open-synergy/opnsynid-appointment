# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class Appointment(models.Model):
    _name = "appointment.appointment"
    _description = "Appointment"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "custom.info.mixin",
        "ir.needaction_mixin",
    ]
    _order = "date, time_slot_id"
    _state_from = ["draft", "confirm"]
    _state_to = ["approve"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_policy(self):
        _super = super(Appointment, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Appointment",
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
        required=False,
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
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "confirm": [
                ("required", True),
            ],
            "approve": [
                ("required", True),
            ],
            "open": [
                ("required", True),
            ],
            "done": [
                ("required", True),
            ],
            "cancel": [
                ("required", True),
            ],
        },
    )
    appointee_id = fields.Many2one(
        string="Appointee",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Appointment Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_type_ids = fields.Many2many(
        string="Allowed Type User",
        comodel_name="appointment.type",
        related="appointee_id.allowed_type_ids",
        store=False,
    )
    type_ids = fields.Many2many(
        string="Allowed Type",
        comodel_name="appointment.type",
        required=False,
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
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
                ("required", False),
            ],
            "confirm": [
                ("required", True),
            ],
            "approve": [
                ("required", True),
            ],
            "open": [
                ("required", True),
            ],
            "done": [
                ("required", True),
            ],
            "cancel": [
                ("required", True),
            ],
        },
    )
    appointment_method = fields.Selection(
        string="Method",
        selection=[
            ("online", "Online"),
            ("offline", "Offline"),
        ],
        copy=False,
        default="online",
        required=True,
    )
    link_method = fields.Text(
        string="Link",
    )
    time_slot_id = fields.Many2one(
        string="Time Slot",
        comodel_name="appointment.time_slot",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Schedulled"),
            ("open", "In Progress"),
            ("done", "Done"),
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
    open_date = fields.Datetime(
        string="Start Date",
        readonly=True,
        copy=False,
    )
    open_user_id = fields.Many2one(
        string="Start By",
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
    open_ok = fields.Boolean(
        string="Can Force Start",
        compute="_compute_policy",
    )
    finish_ok = fields.Boolean(
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
    def action_approve(self):
        for record in self:
            record.write(record._prepare_approve_data())

    @api.multi
    def action_start(self):
        for record in self:
            record.write(record._prepare_start_data())

    @api.multi
    def action_finish(self):
        for record in self:
            record.write(record._prepare_finish_data())

    @api.multi
    def action_cancel(self):
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
    def _prepare_approve_data(self):
        self.ensure_one()
        sequence = self._create_sequence()
        return {
            "state": "approve",
            "name": sequence,
        }

    @api.multi
    def _prepare_start_data(self):
        self.ensure_one()
        return {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_finish_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }

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
            "open_date": False,
            "open_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "type_id": False,
            "partner_id": False,
            "title": False,
        }

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(Appointment, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(Appointment, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(Appointment, self)
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

    @api.constrains("state")
    def _check_type_id(self):
        error_msg = _("Please select type")
        for document in self:
            if document.state != "draft" and not document.type_id:
                raise UserError(error_msg)

    @api.constrains("state")
    def _check_partner_id(self):
        error_msg = _("Please select partner")
        for document in self:
            if document.state != "draft" and not document.partner_id:
                raise UserError(error_msg)

    @api.constrains("state")
    def _check_title(self):
        error_msg = _("Please input title")
        for document in self:
            if document.state != "draft" and not document.title:
                raise UserError(error_msg)

    @api.constrains("state")
    def _check_timeslot(self):
        error_msg = _("Time slot already schedulled")
        for document in self:
            criteria = [
                ("date", "=", document.date),
                ("appointee_id", "=", document.appointee_id.id),
                ("time_slot_id", "=", document.time_slot_id.id),
                ("id", "!=", document.id),
            ]
            appointment_count = self.env["appointment.appointment"].search_count(
                criteria
            )
            if appointment_count > 0:
                raise UserError(error_msg)

    @api.onchange(
        "appointee_id",
    )
    def onchange_type_id(self):
        self.type_ids = False
