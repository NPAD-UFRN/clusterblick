var service0 = ssupervisor_dfh1[0];
var lustre = ssupervisor_dfh1[3];

var gauges = [];

function createGauge(name, label, min, max)
{
	var config = 
	{
		size: 350,
		label: label,
		min: undefined != min ? min : 0,
		max: undefined != max ? max : 100,
		minorTicks: 5
	}

	var range = config.max - config.min;
	config.yellowZones = [{ from: config.min + range*0.75, to: config.min + range*0.9 }];
	config.redZones = [{ from: config.min + range*0.9, to: config.max }];

	gauges[name] = new Gauge(name, config);
	gauges[name].render();
}

function createGauges()
{
	createGauge("service0", "service0",0,Number(service0.Size.replace('T','').replace(',','.')));
	createGauge("lustre", "Lustre",0,Number(lustre.Size.replace('T','').replace(',','.')));
}

function updateGauges()
{
	for (var key in gauges)
	{
		if (key=='service0'){
			var value = Number(service0.Used.replace('T','').replace(',','.'));
		}
		if (key=='lustre'){
			var value = Number(lustre.Used.replace('T','').replace(',','.'));
		}
		gauges[key].redraw(value);
	}
}
