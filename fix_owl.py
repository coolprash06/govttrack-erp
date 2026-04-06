import os

# Fix dashboard.js
owl_js = """/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class GovtTrackDashboard extends Component {
    static template = "govttrack_erp.dashboard";

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({ data: {} });

        onWillStart(async () => {
            this.state.data = await this.rpc("/govttrack/dashboard", {});
        });
    }
}

registry.category("actions").add("govttrack_dashboard", GovtTrackDashboard);
"""

with open("static/src/js/dashboard.js", "w", encoding="utf-8") as f:
    f.write(owl_js)

# Fix dashboard.xml
with open("static/src/xml/dashboard.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

xml_content = xml_content.replace("widget.data", "state.data")
# In OWL, it usually doesn't like len(), we can use length
xml_content = xml_content.replace("len(state.data.delayed_projects)", "state.data.delayed_projects.length")
xml_content = xml_content.replace("len(state.data.recent_grievances)", "state.data.recent_grievances.length")


with open("static/src/xml/dashboard.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)
