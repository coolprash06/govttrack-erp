{
    "name": "GovtTrack ERP",
    "version": "1.4",
    "author": "GovtTrack Team",
    "license": "LGPL-3",
    "depends": ["base", "mail", "web"],
    "application": True,
    "assets": {
        "web.assets_backend": [
            "govttrack_erp/static/src/css/govttrack_erp.css",
            "govttrack_erp/static/src/js/dashboard.js",
            "govttrack_erp/static/src/xml/dashboard.xml"
        ]
    },
    "data": [
        "security/ir.model.access.xml",
        "views/dashboard_views.xml",
        "views/project_views.xml",
        "views/category_views.xml",
        "views/constituency_views.xml",
        "views/grievance_views.xml",
        "views/menus.xml"
    ],
    "demo": [
        "data/demo_data.xml"
    ]
}