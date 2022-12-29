const ctx = document.getElementById('myChart');
new Chart(ctx, {
	type: 'bar',
	data: {
		labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
		datasets: [{
			label: '# of Votes',
			data: [12, 19, 3, 5, 2, 3],
			backgroundColor: ['Red','Blue','Yellow','Green','Purple','Orange'],
			borderWidth: 1
	  	}]
	},
	options: {
		scales: {
			y: {
		  		beginAtZero: true
			}
	  	}
	}
});