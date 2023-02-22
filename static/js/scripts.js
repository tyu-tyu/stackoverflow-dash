// Nav menu Called on resize and closing
function reset_nav_menu() {
	document.getElementById('side-nav-container').style.width = 0;
	document.querySelector('body').style.marginLeft = 0;
	document.querySelector('aside nav').style.opacity = 0;
	document.getElementById('nav-btn-open').style.opacity = 100;
	document.getElementsByClassName('active')[0].style.opacity = 0;
}
//Creates a chart and places it in supplied canvas
function createChart(ctx,type,top_label,labels,data,options) {
	new Chart(ctx, {
		type: type,
		responsive: false,
		maintainAspectRatio: false,
		data: {
			labels: labels,
			datasets: [{
				label: top_label,
				data: data,
				backgroundColor: ['Red','Blue','Yellow','Green','Purple','Orange'],
				borderWidth: 1
			}]
		},
		options: {
			options
		}
	});
};

//Inits a datatable example 
// 	const t = document.getElementById("testTable");
// const data = {
// headings: [
// 	"Tag",
// 	"Count"
// ],
// data: [
// 	{{ data['top_100_tags']['data'] | tojson }}
// ]
// };

// document.getElementById('tags-box').appendChild(t);

// window.dt = new simpleDatatables.DataTable(t, {
// fixedHeight: true,
// data
// });

document.addEventListener("DOMContentLoaded", function(e) {
	// Header animation handling
	document.getElementById('nav-btn-open').addEventListener('click', function() {
		document.getElementById('side-nav-container').style.width = '6rem';
		document.querySelector('body').style.marginLeft = '6rem';
		document.querySelector('aside nav').style.opacity = 100;
		document.getElementById('nav-btn-open').style.opacity = 0;
		document.getElementsByClassName('active')[0].style.opacity = 100;
	});
	
	document.getElementById('nav-btn-close').addEventListener('click', function() {
		reset_nav_menu();
	});
	// Dynamic resizing for window changes
	window.addEventListener('resize', function(event){
		if (this.window.innerWidth < 600){
			document.getElementById('nav-btn-close').style.display = 'none';
			document.getElementById('nav-btn-open').style.display = 'none';
			document.getElementById('side-nav-container').style.width = '100%';
			document.getElementById('side-nav-container').style.height = '3rem'
			document.querySelector('body').style.marginLeft = 0;
			document.querySelector('aside nav').style.opacity = 100;
			document.getElementsByClassName('active')[0].style.opacity = 100;
		} else {
			document.getElementById('nav-btn-close').style.display = 'block';
			document.getElementById('nav-btn-open').style.display = 'block';
			document.getElementById('side-nav-container').style.height = '100%';
			reset_nav_menu();
		}
	});
});