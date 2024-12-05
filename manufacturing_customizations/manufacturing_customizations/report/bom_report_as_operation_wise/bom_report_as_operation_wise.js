// Copyright (c) 2024, Prathamesh Jadhav and contributors
// For license information, please see license.txt

frappe.query_reports["BOM report as Operation Wise"] = {
	filters: [
		{
			fieldname: "bom",
			label: __("BOM"),
			fieldtype: "Link",
			options: "BOM",
			reqd: 1,
		},
	],
};
