import frappe
from erpnext.manufacturing.doctype.production_plan.production_plan import ProductionPlan

@frappe.whitelist()
def make_production_plan(sales_order):
    pp_doc = frappe.new_doc("Production Plan")
    pp_doc.get_items_from = "Sales Order"
    pp_doc.append('sales_orders', {
        'sales_order': sales_order,
        'customer': frappe.db.get_value("Sales Order", sales_order, "customer"),
        'sales_order_date': frappe.db.get_value("Sales Order", sales_order, "transaction_date"),
        'grand_total': frappe.db.get_value("Sales Order", sales_order, "grand_total"),
    })

    pp_doc.run_method("get_so_items")
    pp_doc.save(ignore_permissions=True)
    frappe.db.commit()

    # Update custom fields for items in po_items after save
    for item in pp_doc.po_items:
        # Fetch total_qty from Bin
        total_qty = frappe.db.sql("""
            SELECT SUM(actual_qty) AS total_qty
            FROM `tabBin`
            WHERE item_code = %s
        """, item.item_code, as_dict=True)

        custom_total_qty = total_qty[0].get("total_qty", 0) if total_qty else 0

        # Set custom fields
        frappe.db.set_value(
            "Production Plan Item",
            item.name,
            "custom_total_qty",
            custom_total_qty
        )
        frappe.db.set_value(
            "Production Plan Item",
            item.name,
            "custom_sales_order_qty",
            item.planned_qty  # planned_qty == custom_sales_order_qty
        )

    frappe.msgprint(f"Production Plan '<a href='/app/production-plan/{pp_doc.name}'>{pp_doc.name}</a>' Created")
