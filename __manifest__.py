{
    'name': 'Checklist & SOP Templates',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Reusable checklist/SOP templates and trackable checklist instances attachable to any record',
    'description': """
Checklist & SOP Templates
==========================
Build reusable checklist / SOP templates once, then generate trackable
checklist instances from them and attach each instance to ANY record in
Odoo (a Project task, a Helpdesk ticket, a Lead, a Partner, ... anything)
using a generic reference, the same pattern Odoo's own Activities use.

Why
---
Odoo has no built-in way to define a reusable checklist template (e.g. an
"Employee Onboarding" or "New Supplier Approval" checklist) and reuse it
across many records with completion tracking, ownership per item, and a
hard stop if mandatory items are left undone.

Features
--------
* Checklist templates with ordered, mandatory/optional items
* One-click generation of a checklist instance from a template
* Attach an instance to ANY model/record via a generic reference
* Stored progress % computed from item completion
* Per-item "done by" / "done on" tracking
* Blocks closing a checklist while mandatory items are incomplete
* Full chatter, activities and tracked state field on every checklist
* Two access levels: Checklist User and Checklist Manager
""",
    'author': 'Shoaib Saifi',
    'website': 'https://example.com',
    'license': 'LGPL-3',
    'depends': ['mail'],
    'data': [
        'security/checklist_security.xml',
        'security/ir.model.access.csv',
        'views/checklist_template_views.xml',
        'views/checklist_instance_views.xml',
        'views/checklist_menus.xml',
    ],
    'demo': [
        'demo/checklist_demo.xml',
    ],
    'application': True,
    'installable': True,
}
