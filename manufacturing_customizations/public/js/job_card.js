frappe.ui.form.on("Job Card", {
    refresh: function(frm){
		if(frm.doc.total_completed_qty>0 && frm.doc.custom_completed_stock_qty!==frm.doc.for_quantity){
			frm.add_custom_button(__('Finish'), function(){
				create_stock_entry(frm)
			});
		}
    },
	on_submit: function(frm){
		if(frm.doc.total_completed_qty>0 && frm.doc.custom_completed_stock_qty!==frm.doc.for_quantity){
			create_stock_entry(frm)
		}
	}
})

function create_stock_entry(frm){
	frappe.call({
		method: "manufacturing_customizations.customizations.job_card.make_stock_entry",
		args:{
			job_card:frm.doc.name,
			work_order_id: frm.doc.work_order,
			purpose: "Manufacture",
			qty: frm.doc.total_completed_qty,
		},
		callback: function(r) {
			let stock_entry = r.message;
			frappe.model.sync(stock_entry);
			frappe.set_route("Form", stock_entry.doctype, stock_entry.name);
		}
	});
}