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
			var value = Math.round(Number(dfh1[0]["Use%"].replace('%','').replace(',','.')));
		}
		if (key=='lustre'){
			var value = Math.round(Number(dfh1[3]["Use%"].replace('%','').replace(',','.')));
		}
		if (key=='service0cpu'){
			var value = s0cpu;
		}
		gauges[key].redraw(value);
	}
}
