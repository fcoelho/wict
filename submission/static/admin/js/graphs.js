function plotEvaluations(element, data) {
	var average = 0.0;
	for (var i=0 ; i<data.length ; ++i)
		average += data[i];
	average /= data.length;

	var barClearing = 0.2;

	var commonOptions = {
		bars: {
			show: true,
			fill: 0.9,
			barWidth: 1.0 - barClearing,
			align: "center",
		},
	};

	var plotData1 = [];
	for (var i=0 ; i<data.length ; ++i)
		plotData1.push([i + 1, data[i]]);
	var plotData2 = [[data.length + 1, average]];

	var plot1 = $.extend({}, commonOptions, {data: plotData1});
	var plot2 = $.extend({}, commonOptions, {data: plotData2});

	var xTicksLabels = [];
	for (var i=1 ; i<=data.length ; ++i)
		xTicksLabels.push([i, i.toString()]);
	xTicksLabels.push([data.length + 1, "Average"]);

	var yTicksLabels = [];
	for (var i=1 ; i<=5 ; ++i)
		yTicksLabels.push([i, ""]);

	var plotOptions = {
		xaxis: {
			ticks: xTicksLabels,
			min: 0.3,
			max: data.length + 1.7,
		},
		yaxis: {
			ticks: yTicksLabels,
			min: 0.0,
			max: 5.5,
		},
	};

	$.plot(element, [plot1, plot2], plotOptions);
}
