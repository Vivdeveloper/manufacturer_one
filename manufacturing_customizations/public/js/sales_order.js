frappe.ui.form.on("Sales Order", {
	refresh: function(frm){
		if(frm.doc.status == "To Deliver and Bill"){
			frm.add_custom_button(
				__("Generate Production Plan"),
				() => {
					generate_production_plan(frm);
				}
			);	
		}
	}
});

function generate_production_plan(frm){
	frappe.call({
		method: "manufacturing_customizations.customizations.sales_order.make_production_plan",
		args:{
			sales_order : frm.doc.name
		},
		callback: function(r) {
			
		}
	});
}