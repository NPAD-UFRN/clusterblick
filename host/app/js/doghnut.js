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
            data: [300, 100, 50],//alloc,idle,down
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

