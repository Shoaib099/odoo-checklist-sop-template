# Checklist & SOP Templates for Odoo 19

A reusable checklist and SOP management module for Odoo 19.

This module allows users to create reusable checklist/SOP templates, generate trackable checklist instances, assign checklists to users, monitor progress, and attach checklist instances to different Odoo records.

## Overview

Many business processes require the same sequence of tasks to be completed repeatedly, such as:

- Employee onboarding
- Quality checks
- Safety procedures
- Approval processes
- Internal operational procedures

This module provides reusable checklist templates that can be converted into working checklist instances.

## Features

- Create reusable checklist and SOP templates
- Add ordered checklist items
- Mark items as mandatory or optional
- Generate checklist instances from templates
- Attach checklist instances to different Odoo records
- Track checklist completion progress
- Track who completed each item and when
- Prevent completion when mandatory items are incomplete
- Chatter and activities support
- Draft, In Progress, Done and Cancelled states
- Checklist User and Checklist Manager access levels
- Search and group checklist records

## How It Works

The basic workflow is:

**Create Template → Add Checklist Items → Mark Mandatory/Optional Items → Generate Checklist → Assign User → Complete Items → Track Progress → Validate Mandatory Items → Mark as Done**

## Example Use Case

### Employee Onboarding

An organization can create an **Employee Onboarding** checklist containing tasks such as:

1. Prepare laptop and accounts
2. Complete employment documentation
3. Introduce employee to the team
4. Complete required training
5. Complete onboarding formalities

Mandatory items must be completed before the checklist can be marked as **Done**.

## Technical Architecture

### Main Models

| Model | Purpose |
|---|---|
| `checklist.template` | Stores reusable checklist/SOP templates |
| `checklist.template.line` | Stores template checklist items |
| `checklist.instance` | Stores generated checklist instances |
| `checklist.instance.line` | Stores checklist instance items |

### Module Structure

```text
checklist_sop_template/
├── demo/
│   └── checklist_demo.xml
├── models/
│   ├── __init__.py
│   ├── checklist_template.py
│   ├── checklist_template_line.py
│   ├── checklist_instance.py
│   └── checklist_instance_line.py
├── security/
│   ├── checklist_security.xml
│   └── ir.model.access.csv
├── static/
│   └── description/
│       └── icon.png
├── views/
│   ├── checklist_template_views.xml
│   ├── checklist_instance_views.xml
│   └── checklist_menus.xml
├── __init__.py
└── __manifest__.py
```

## Installation

### Requirements

- Odoo 19.0
- Odoo `mail` module

### Steps

1. Copy the `checklist_sop_template` folder into your Odoo addons directory.
2. Restart the Odoo server.
3. Update the Apps list.
4. Search for **Checklist & SOP Templates**.
5. Install the module.

## Usage

### 1. Create a Template

Create a checklist template and define the required checklist items.

### 2. Configure Checklist Items

For each item, configure:

- Item name
- Sequence
- Suggested owner
- Mandatory or optional status

### 3. Generate a Checklist

Generate a checklist instance from an existing template.

### 4. Assign the Checklist

Assign the checklist to the responsible user.

### 5. Complete Checklist Items

Users can complete individual items while the system tracks overall progress.

### 6. Complete the Checklist

The checklist can be marked as **Done** once all mandatory items have been completed.

## Security

The module provides two access levels:

### Checklist User

Allows users to work with checklist instances according to the configured access rules.

### Checklist Manager

Provides additional permissions for managing checklist templates.

## Technical Stack

- Odoo 19
- Python
- XML
- Odoo ORM
- PostgreSQL
- Odoo Security & Access Control
- Odoo Mail / Chatter

## Dependency

The module currently depends on:

```text
mail
```

## Future Enhancements

- Email notifications for checklist deadlines
- Recurring checklists
- Checklist reporting and analytics
- Conditional checklist items
- Automatic checklist generation based on business events
- Additional Odoo application integrations

## Project Information

**Version:** 19.0.1.0.0

**Category:** Productivity

**License:** LGPL-3

## Author

**Shoaib Saifi**

GitHub: https://github.com/Shoaib099

## License

This project is licensed under the **LGPL-3** license.
