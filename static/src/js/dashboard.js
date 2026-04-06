/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export class GovtTrackDashboard extends Component {
    static template = "govttrack_erp.dashboard";

    setup() {
        this.state = useState({ data: {} });

        onWillStart(async () => {
            this.state.data = await rpc("/govttrack/dashboard", {});
        });
    }
}

registry.category("actions").add("govttrack_dashboard", GovtTrackDashboard);
console.log("GovtTrack Dashboard Loaded! OWL Component Registered.");
