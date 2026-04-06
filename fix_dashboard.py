import os

def fix_dashboard():
    dashboard_file = r"views\dashboard_views.xml"
    with open(dashboard_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Create static/src/xml
    os.makedirs(r"static\src\xml", exist_ok=True)
    
    # Write client-side XML
    template_content = ['<?xml version="1.0" encoding="UTF-8"?>\n', '<templates xml:space="preserve">\n'] + lines[15:253] + ['</templates>\n']
    with open(r"static\src\xml\dashboard.xml", "w", encoding="utf-8") as f:
        f.writelines(template_content)

    # Overwrite the old dashboard views to exclude the qweb template
    new_views = lines[:9] + lines[-2:]
    with open(dashboard_file, "w", encoding="utf-8") as f:
        f.writelines(new_views)

if __name__ == "__main__":
    fix_dashboard()
