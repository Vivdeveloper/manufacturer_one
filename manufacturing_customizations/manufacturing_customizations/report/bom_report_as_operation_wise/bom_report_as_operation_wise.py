# Copyright (c) 2024, Prathamesh Jadhav and contributors
# For license information, please see license.txt

import frappe


import frappe
from frappe import _


def execute(filters=None):
	data = []
	columns = get_columns()
	get_data(filters, data)
	return columns, data


def get_data(filters, data):
	get_exploded_items(filters.bom, data)


def get_exploded_items(bom, data, indent=0, qty=1):
	bom_doc = frappe.get_doc("BOM",bom).as_dict()
	for idx,op in enumerate(bom_doc.operations):
		if idx == 0:
			data.append({
				"item_code": bom_doc.item,
				"bom": bom_doc.name,
				"qty": bom_doc.quantity,
				"uom": bom_doc.uom,
				"operation": op.operation,
				"workstation":op.workstation_type,
				"time_in_mins":op.time_in_mins
			})
		else:
			data.append({
				"item_code": "",
				"bom": "",
				"qty": "",
				"uom": bom_doc.uom,
				"operation": op.operation,
				"workstation":op.workstation_type,
				"time_in_mins":op.time_in_mins
			})
	exploded_items = frappe.get_all(
		"BOM Item",
		filters={"parent": bom},
		fields=["qty", "bom_no", "qty", "item_code", "item_name", "description", "uom"],
		order_by = "bom_no"
	)

	for item in exploded_items:
		if not item.bom_no:
			data.append(
			{
				"item_code": "",
				"raw_item": item.item_name,
				"bom": item.bom_no,
				"qty": "",
				"uom": item.uom
			})
		else:
			get_exploded_items(item.bom_no, data, indent=indent, qty=item.qty)
	return data
	

def get_columns():
	return [
		{
			"label": _("BOM Item"),
			"fieldtype": "Link",
			"fieldname": "item_code",
			"width": 250,
			"options": "Item",
		},
		{
			"label": _("Raw Item"),
			"fieldtype": "Link",
			"fieldname": "raw_item",
			"width": 100,
			"options": "Item",
		},
		{"label": _("UOM"), "fieldtype": "data", "fieldname": "uom", "width": 100},
		{"label": _("Qty"), "fieldtype": "data", "fieldname": "qty", "width": 50},
		{"label": _("BOM"), "fieldtype": "Link", "fieldname": "bom", "width": 150, "options": "BOM"},
		{"label": _("Operation"), "fieldtype": "Link", "fieldname": "operation", "width": 150, "options": "Operation"},
		{"label": _("Workstation"), "fieldtype": "Link", "fieldname": "workstation", "width": 150,"options": "Workstation Type"},
		{"label": _("Operation Time"), "fieldtype": "data", "fieldname": "time_in_mins", "width": 150},
		{"label": _("Costing"), "fieldtype": "Currency", "fieldname": "costing", "width": 100}
		
	]

