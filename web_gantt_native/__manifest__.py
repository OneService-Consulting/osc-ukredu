# -*- coding: utf-8 -*-
{
    "name": """Gantt Native Web view""",
    "summary": """One price = web_gant_native, project_native, project_native_report_advance, project_native_exchange hr_holidays_gantt_native, mrp_gantt_native""",
    "category": "Project",
    "images": ['static/description/banner.gif'],
    "version": "16.24.01.04.0",
    "description": """
        Main Module for Gantt Native

    """,

    "author": "Viktor Vorobjov",
    "license": "OPL-1",
    "website": "https://www.youtube.com/watch?v=xbAoC_s5Et0&list=PLmxcMU6Ko0NkqpGLcC44_GXo3_41pyLNx",
    "support": "vostraga@gmail.com",
    "live_test_url": "https://demo15.garage12.eu",
    "price": 299.00,
    "currency": "EUR",

    "depends": [
        "web", "web_widget_time_delta"
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
    ],
    "qweb": [
    ],
    "demo": [],
    'assets': {

        'web.assets_backend': [
            'web_gantt_native/static/src/css/gantt_native.css',
            'web_gantt_native/static/src/css/gantt_native_ztree.css',
            'web_gantt_native/static/src/lib/twix.js',
            'web_gantt_native/static/src/lib/jquery.ztree.core.js',
            'web_gantt_native/static/src/lib/jquery.ztree.exedit.js',
            'web_gantt_native/static/src/js/native_gantt_view.js',
            'web_gantt_native/static/src/js/native_gantt_controller.js',
            'web_gantt_native/static/src/js/native_gantt_model.js',
            'web_gantt_native/static/src/js/native_gantt_renderer.js',
            'web_gantt_native/static/src/js/gantt_tool_field.js',
            'web_gantt_native/static/src/js/gantt_pager.js',
            'web_gantt_native/static/src/js/gantt_timeline_head.js',
            'web_gantt_native/static/src/js/gantt_timeline_data.js',
            'web_gantt_native/static/src/js/gantt_tool_tip.js',
            'web_gantt_native/static/src/js/gantt_tool_hint.js',
            'web_gantt_native/static/src/js/gantt_timeline_arrow_draw.js',
            'web_gantt_native/static/src/js/gantt_timeline_arrow.js',
            'web_gantt_native/static/src/js/gantt_timeline_ghost.js',
            'web_gantt_native/static/src/js/gantt_timeline_bar_summary.js',
            'web_gantt_native/static/src/js/gantt_timeline_bar_first.js',
            'web_gantt_native/static/src/js/gantt_timeline_header.js',
            'web_gantt_native/static/src/js/gantt_timeline_header_hint.js',
            'web_gantt_native/static/src/js/gantt_timeline_scroll.js',
            'web_gantt_native/static/src/js/gantt_timeline_info.js',
            'web_gantt_native/static/src/js/gantt_timeline_res_level.js',
            'web_gantt_native/static/src/js/gantt_timeline_res_bar.js',
            'web_gantt_native/static/src/js/gantt_timeline_intersection.js',
            'web_gantt_native/static/src/js/gantt_timeline_bar_docs.js',
            'web_gantt_native/static/src/js/gantt_item_options.js',
            'web_gantt_native/static/src/js/gantt_item_ztree.js',
            'web_gantt_native/static/src/js/gantt_item_action.js',
            'web_gantt_native/static/src/js/gantt_item_info.js',
            'web_gantt_native/static/src/js/native_gantt_data.js',
            'web_gantt_native/static/src/xml/*.xml',
        ],

    },

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}
