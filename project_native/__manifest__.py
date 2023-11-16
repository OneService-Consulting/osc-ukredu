# -*- coding: utf-8 -*-
{
    "name": """Gantt Native view for Projects""",
    "summary": """One price = web_gant_native, project_native, project_native_report_advance, project_native_exchange hr_holidays_gantt_native, mrp_gantt_native""",
    "category": "Project",
    "images": ['static/description/banner.gif'],
    "version": "16.23.08.24.0",
    "description": """
        Gantt View for Project and Project Task
    """,
    "author": "Viktor Vorobjov",
    "license": "OPL-1",
    "website": "https://www.youtube.com/watch?v=ewE4HMxlDcM",
    "support": "vostraga@gmail.com",
    "live_test_url": "https://demo16.garage12.eu",

    "depends": [
        "project",
        "hr_timesheet",
        "web_gantt_native",
        "web_widget_time_delta",
        "web_widget_colorpicker",
        "project_native_update_duration",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/project_task_view.xml',
        'views/project_task_resource_view.xml',
        'views/project_task_detail_plan_view.xml',
        'views/project_calendar_access_view.xml',
        'views/resource_views.xml',
        'views/project_project_view.xml',
        'security/ir.model.access.csv',
    ],
    "qweb": [],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "assets": {},
    "installable": True,
    "auto_install": False,
    "application": False,
}
