var ctx = document.getElementById("queueHist").getContext("2d");

var queueHistChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: label_hist,
        datasets: [
            {
                type: 'line',
                label: "Nós PD",
                fill: false,
                backgroundColor: "rgba(255,153,51, 0.7)",
                borderColor: "rgba(255,153,51,1)",
                pointBorderColor: "rgba(255,153,51,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 0,
                pointHoverRadius: 10,
                pointHoverBackgroundColor: "rgba(255,153,51,1)",
                pointRadius: 2,
                pointHitRadius: 10,
                data: sumnodepd,
            },
            {
                type: 'bar',
                label: 'Jobs PD',
                fill: true,
                backgroundColor: "rgba(0,102,204, 0.7)",
                borderColor: "rgba(0,102,204,1)",
                pointBorderColor: "rgba(0,102,204,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 0,
                pointHoverRadius: 10,
                pointHoverBackgroundColor: "rgba(0,102,204,1)",
                pointRadius: 2,
                pointHitRadius: 10,
                data: sumjobspd,
            }

        ]
    },
    options: {
            title:{
              display:true,
              text: "squeue",
              fontSize:28,
            },
            legend:{
              position:'bottom'
            },
            scales: {
              xAxes: [{
                display:false
              }],
              yAxes: [{
                ticks: {
                    stepSize: 10
                }
              }]
            },
            responsive:false,
            maintainAspectRatio: false
        }
});
