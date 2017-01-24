var gauges = [];

function createGauges()
{
	createGauge("service0", "service0",0,Number(ssupervisor_dfh1[0].Size.replace('T','').replace(',','.')));
	createGauge("lustre", "Lustre",0,Number(ssupervisor_dfh1[3].Size.replace('T','').replace(',','.')));
}

function updateGauges()
{
	for (var key in gauges)
	{
		if (key=='service0'){
			var value = Number(ssupervisor_dfh1[0].Used.replace('T','').replace(',','.'));
		}
		if (key=='lustre'){
			var value = Number(ssupervisor_dfh1[3].Used.replace('T','').replace(',','.'));
		}
		gauges[key].redraw(value);
	}
}
