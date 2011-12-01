function animate() {

	position = $(".tank-level").css("background-position").split(' ');
	x = parseInt(position[0]);
	y = parseInt(position[1]);
	
	if (x > -3058) {
		$(".tank-level").css("background-position", (x-160) + "px " + y + "px");
	} else {
		$(".tank-level").css("background-position", "-18px " + y + "px");
	}
	
}

function round5(x) {
    return (x % 5) >= 2.5 ? parseInt(x / 5) * 5 + 5 : parseInt(x / 5) * 5;
}

function generateChart(tapNumber, chartData) {

	$("#" + tapNumber + " .chart").sparkline(chartData,
			{
				width: '300px',
				height: "80px",
				lineColor: "#555",
				spotColor: "#555",
				minSpotColor: "#555",
				maxSpotColor: "#555",
				fillColor: "rgba(0,0,0,.1)",
				type: 'line',
				spotRadius: 1.5
			}
		);
}

function setLevel(tapNumber, level) {

	y = -40;
	x = -4000;
	
	if (level >= 0 && level <= 100) {
		x = -3058-((round5(level)/5-1)*-160);
		//x = level;
	} else {
		alert("level out of range (must be 0-100)");
	}
		
	$("#" + tapNumber + " .tank-level").css("background-position", x + "px " + y + "px");

}

function updatePerson(tapID, elementID, name, time, gravitar) {

	//NAME
	$("#" + tapID + " ." + elementID).find("h3").html(name);
	
	//TIME
	$("#" + tapID + " ." + elementID).find("span.detail").html("(" + time + ")");
	
	//GRAVITAR
	$("#" + tapID + " ." + elementID).find("img").attr("src", gravitar);

}

function requestTapData(tapID) {

	if(tapID == "one") {
		number = 1;
	} else if (tapID == "two") {
		number = 2;
	}
	
	//REQUEST DATA
	$.ajax({
		type: 'GET',
		url: "/get_tap/" + number + "/",
		success: function(data){
			
			console.log(data);
			setLevel(tapID, data.level*100);

		}

	});
	
	$("#" + tapID + " .meta h2").text("name!");
	$("#" + tapID + " .meta h4").text(data.amountLeft + " beers left");
	$("#" + tapID + " .meta .age .item-value").text(data.age);
	$("#" + tapID + " .meta .volume .item-value").text(data.volume);
	$("#" + tapID + " .meta .ibu .item-value").text(data.ibu);
	$("#" + tapID + " .meta .abv .item-value").text(data.abv);

}

function requestTapGraph(tapID) {

	if(tapID == "one") {
		number = 1;
	} else if (tapID == "two") {
		number = 2;
	}
	
	//REQUEST DATA
	$.ajax({
		type: 'GET',
		url: "/get_graph/" + number + "/",
		success: function(data){
			
			generateChart(tapID, data.values);
			
			$("#" + tapID + " .chart-desc").text("Consumption Trend (" + data.total + " people)")

		}

	});
	
}

function requestLastToDrink(tapID, elementID) {

	if(tapID == "one") {
		number = 1;
	} else if (tapID == "two") {
		number = 2;
	}
	
	//REQUEST DATA
	$.ajax({
		type: 'GET',
		url: "/get_last/" + number + "/",
		success: function(data){
			
			console.log(data);
			updatePerson(tapID, elementID, data.name, data.time, data.gravitar);

		}

	});
		
}

function requestHighestConsumption(tapID, elementID) {

	if(tapID == "one") {
		number = 1;
	} else if (tapID == "two") {
		number = 2;
	}
	
	//REQUEST DATA
	$.ajax({
		type: 'GET',
		url: "/get_highest/" + number + "/",
		success: function(data){
			
			console.log(data);
			updatePerson(tapID, elementID, data.name, data.amount, data.gravitar);

		}

	});
		
}

function requestFastestBeer(tapID, elementID) {

	if(tapID == "one") {
		number = 1;
	} else if (tapID == "two") {
		number = 2;
	}
	
	//REQUEST DATA
	$.ajax({
		type: 'GET',
		url: "/get_fastest/" + number + "/",
		success: function(data){
			
			console.log(data);
			updatePerson(tapID, elementID, data.name, data.time, data.gravitar);

		}

	});
	
}

function updateValues() {

	console.log("checking values...");

	//TAP LEVEL
	requestTapData("one");
	requestTapData("two");
	
	//GRAPHS
	requestTapGraph("one");
	requestTapGraph("two");
	
	//LAST TO DRINK
	requestLastToDrink("two", "last");
	requestLastToDrink("one", "last");
	
	//HIGHEST CONSUPTION
	requestHighestConsumption("two", "consumption");
	requestHighestConsumption("one", "consumption");
	
	//FASTEST BEER
	requestFastestBeer("two", "fastest");
	requestFastestBeer("one", "fastest");
	
}

$(document).ready(function(){

	var interval = setInterval("updateValues()", 2000);
	updateValues();
	
});
