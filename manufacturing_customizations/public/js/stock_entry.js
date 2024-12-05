frappe.ui.form.on("Stock Entry", {
	on_submit: function(frm){
		(frm.doc.items).forEach((item) => {
		  if(item.is_finished_item == 1 && frm.doc.custom_job_card !== undefined){
			  frappe.db.set_value('Job Card', frm.doc.custom_job_card, 'custom_completed_stock_qty', item.qty)
				.then(r => {
					let doc = r.message;
				})
		  }
		});
	}
})