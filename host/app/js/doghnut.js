var ctx = "donut";

var options = { 
    responsive: false,
    maintainAspectRatio: true
}
var data = {
    labels: [
        "Alloc",
        "Idle",
        "Down"
    ],
    datasets: [
        {
            data: [stats.allocs,stats.idles,stats.downs],//alloc,idle,down,//alloc,idle,down
            backgroundColor: [
                "#1F8261",//alloc
                "#FFA500",//idle
                "#CB4B16"//down
            ],
            hoverBackgroundColor: [
                "#1F8261",//alloc
                "#FFA500",//idle
                "#CB4B16"//down
            ]
        }]
};

//doughnut chart
var myDoughnutChart = new Chart(ctx, {
    type: 'doughnut',
	data: data,
	animation:{
        animateScale:true
    }    
});

