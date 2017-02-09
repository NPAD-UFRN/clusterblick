var canvas = document.getElementById('updating-chart'),
    ctx = canvas.getContext('2d'),

    startingData = {
      labels: label_hist,
      datasets: [
          {
            label: "Down",
            fill: true,
            backgroundColor: "rgba(203, 75, 22, 0.7)",
            borderColor: "rgba(203, 75, 22,1)",
            pointBorderColor: "rgba(203, 75, 22,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 5,
            pointHoverRadius: 10,
            pointHoverBackgroundColor: "rgba(203, 75, 22,1)",
            pointRadius: 2,
            pointHitRadius: 10,
            data: down_hist
          },
          {
            label: "Idle",
            fill: true,
            backgroundColor: "rgba(255, 165, 0, 0.7)",
            borderColor: "rgba(255, 165, 0,1)",
            pointBorderColor: "rgba(255, 165, 0,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 5,
            pointHoverRadius: 10,
            pointHoverBackgroundColor: "rgba(255, 165, 0,1)",
            pointRadius: 2,
            pointHitRadius: 10,
            data: idle_hist
          },
          {
            label: "Resv/Mant",
            fill: true,
            backgroundColor: "rgba(0,102,204,0.7)",
            borderColor: "rgba(0,102,204,1)",
            pointBorderColor: "rgba(0,102,204,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 5,
            pointHoverRadius: 10,
            pointHoverBackgroundColor: "rgba(0,102,204,1)",
            pointRadius: 2,
            pointHitRadius: 10,
            data: resvmant_hist
          },
          {
            label: "Other",
            fill: true,
            backgroundColor: "rgba(0,0,0,0.7)",
            borderColor: "rgba(0,0,0,1)",
            pointBorderColor: "rgba(0,0,0,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 5,
            pointHoverRadius: 10,
            pointHoverBackgroundColor: "rgba(0,0,0,1)",
            pointRadius: 2,
            pointHitRadius: 10,
            data: other_hist
          },
          {
            label: "Allocated",
            fill: true,
            backgroundColor: "rgba(31, 130, 97,0.7)",
            borderColor: "rgba(31, 130, 97,1)",
            pointBorderColor: "rgba(31, 130, 97,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 5,
            pointHoverRadius: 10,
            pointHoverBackgroundColor: "rgba(31, 130, 97,1)",
            pointRadius: 2,
            pointHitRadius: 10,
            data: alloc_hist
          }



      ]
    };

var sinfoHistChart = new Chart(ctx, {
  type:'line',
  data:startingData,
  options: {
          title:{
            display:true,
            text: "sinfo",
            fontFamily:"modern",
            fontStyle:"oblique",
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
              stacked: true,
              ticks: {
                  stepSize: 10
              }
            }]
          },
          responsive:false,
          maintainAspectRatio: false
      }
});
