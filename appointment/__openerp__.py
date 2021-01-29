# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Appointment Management",
    "version": "8.0.2.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_print_policy",
        "base_multiple_approval",
        "base_cancel_reason",
        "base_custom_information",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "views/appointment_type_views.xml",
        "views/appointment_time_slot_views.xml",
        "views/appointment_appointment_views.xml",
    ],
    "demo": [
        "demo/appointment_time_slot_demo.xml",
        "demo/appointment_type_demo.xml",
    ],
}
