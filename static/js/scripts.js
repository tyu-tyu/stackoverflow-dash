document.addEventListener("DOMContentLoaded", function(event) {
	document.getElementById('nav-btn-open').addEventListener('click', function() {
		document.getElementById('side-nav-container').style.width = '6rem';
		document.querySelector('body').style.marginLeft = '6rem';
		document.querySelector('aside nav').style.opacity = 100;
		document.getElementById('nav-btn-open').style.opacity = 0;
		document.getElementsByClassName('active')[0].style.opacity = 100;
	});
	
	document.getElementById('nav-btn-close').addEventListener('click', function() {
		document.getElementById('side-nav-container').style.width = 0;
		document.querySelector('body').style.marginLeft = 0;
		document.querySelector('aside nav').style.opacity = 0;
		document.getElementById('nav-btn-open').style.opacity = 100;
		document.getElementsByClassName('active')[0].style.opacity = 0;
	});
	
	const ctx = document.getElementById('myChart');
	new Chart(ctx, {
		type: 'bar',
		responsive: false,
		maintainAspectRatio: false,
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
});
