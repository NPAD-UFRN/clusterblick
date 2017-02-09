var margin = { top: 50, right: 0, bottom: 100, left: 30 },
          width = 900 - margin.left - margin.right,
          height = 900 - margin.top - margin.bottom,
          gridSize = Math.floor(width / 20),
          legendElementWidth = 50,
          buckets = 3,
          colors = ["#CB4B16","#FFA500","#0066CC","#000","#1F8261"],//["#000","00f","#CB4B16","#FFA500","#0066CC", "#1F8261"],
          nnns = ["n0", "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12", "n13", "n14", "n15","n16","n17"],
          times = ["i0", "i1", "i2", "i3","service"];
          datasets = ["nodes.tsv"];

      var svg = d3.select("#nodegrid").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var nnnLabels = svg.selectAll(".nnnLabel")
          .data(nnns)
          .enter().append("text")
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return i * gridSize; })
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
            .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "nnnLabel mono axis axis-workweek" : "nnnLabel mono axis"); });

      var timeLabels = svg.selectAll(".timeLabel")
          .data(times)
          .enter().append("text")
            .text(function(d) { return d; })
            .attr("x", function(d, i) { return i * gridSize; })
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + gridSize / 2 + ", -6)")
            .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

      var heatmapChart = function(tsvFile) {
        d3.tsv(tsvFile,
        function(d) {
          return {
            nnn: +d.nnn,
            iii: +d.iii,
            value: +d.value
          };
        },
        function(error, data) {
          var colorScale = d3.scale.quantile()
              .domain([0, buckets-1  , d3.max(data, function (d) { return d.value; })])
              .range(colors);

          var cards = svg.selectAll(".iii")
              .data(data, function(d) {return d.nnn+':'+d.iii;});

          cards.append("title");

          cards.enter().append("rect")
              .attr("x", function(d) { return (d.iii - 1) * gridSize; })
              .attr("y", function(d) { return (d.nnn - 1) * gridSize; })
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("class", "iii bordered")
              .attr("width", gridSize)
              .attr("height", gridSize)
              .style("fill", colors[0]);

          cards.transition().duration(1000)
              .style("fill", function(d) { return colorScale(d.value); });

          cards.select("title").text(function(d) { return d.value; });

          cards.exit().remove();



        });
      };

heatmapChart(datasets[0],1);
