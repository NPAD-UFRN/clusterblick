var gauges = [];

function createGauges()
{
	createGauge("service0mem", "HD",0,100);
	createGauge("service0cpu", "CPU",0,100);
	createGauge("lustre", "HD",0,100);
}

function updateGauges()
{
	for (var key in gauges)
	{
		if (key=='service0mem'){
			var value = Math.round(100*Number(dfh1[0].Used.replace('T','').replace(',','.'))/Number(dfh1[0].Size.replace('T','').replace(',','.')));
		}
		if (key=='lustre'){
			var value = Math.round(100*Number(dfh1[3].Used.replace('T','').replace(',','.'))/Number(dfh1[3].Size.replace('T','').replace(',','.')));
		}
		if (key=='service0cpu'){
			var value = s0cpu;
		}
		gauges[key].redraw(value);
	}
}
