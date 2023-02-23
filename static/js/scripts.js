
ehu_colour_list = ['#5f295f','#fedd00','#2d2926','#007749','#041e42','#1d1d1d','#e5e5e5','#af94af','#9b799b','#875f87','#471f47','#3b1a3b','#301530','#884a93','#5f2944','#9f8a00','#60aa8d','#409977','#208860','#006840','#005937','#004a2e','#f2aab1','#eb5160','#f2d5f8','#f2b1b7','#e15c6e','#dc4155','#d7263d','#bc2135','#a11d2e','#912739','#e9c76e','#e4bc51','#e0b134','#dba617','#c09114','#a47d11','#89680e','#9ed48f','#8bcb79','#77c362','#64ba4c','#4b8b39','#325d26','#005232'];

// HTTP request function for GET and POST methods
function makeHttpRequest(url, request_type, data_response_type, data, callback) {
	let settings = {};

	switch (request_type) {
		case 'GET':
			settings = {
				method: 'GET',
				cache: 'no-cache'
			};
			break;
		case 'POST':
			let formData;
			if(data instanceof FormData) {
				formData = data;
			} else {
				formData = new FormData();
				for (const[key,value] of Object.entries(data)) {
					formData.append(key,value);
				}
			}
			settings = {
				method: 'POST',
				cache: 'no-cache',
				body: formData
			};
			break;
		default:
			throw new Error('request_type does not match available methods');
	}
	
	fetch(url, settings).then(response => {
		switch(data_response_type) {
			case 'JSON':
				return response.json();
			case 'HTML':
				return response.text();
			default:
				throw new Error('Data response type does not match available response types');
		}
	}).then(data => callback(data)).catch(error => console.log(error));
};

//Creates a chart and places it in supplied canvas
function createChart(ctx,type,top_label,labels,data,options) {
	new Chart(ctx, {
		type: type,
		responsive: true,
		maintainAspectRatio: false,
		data: {
			labels: labels,
			datasets: [{
				label: top_label,
				data: data,
				backgroundColor: ehu_colour_list.sort( () => .5 - Math.random() ),
				borderWidth: 1
			}]
		},
		options: {
			options
		}
	});
};

// Nav menu Called on resize and closing
function reset_nav_menu() {
	document.getElementById('side-nav-container').style.width = 0;
	document.querySelector('body').style.marginLeft = 0;
	document.querySelector('aside nav').style.opacity = 0;
	document.getElementById('nav-btn-open').style.opacity = 100;
	document.getElementsByClassName('active')[0].style.opacity = 0;
}

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
			document.getElementById('side-nav-container').style.height = '4rem';
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


/* -------------------------------- Trending -------------------------------- */
function load_trending_table(page_no) {
	let api_url;
	if (page_no == 1) {
		api_url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=month&site=stackoverflow';
	} else {
		api_url = 'https://api.stackexchange.com/2.3/questions?page='+page_no+'&order=desc&sort=month&site=stackoverflow';
	}
	makeHttpRequest(api_url,'GET','JSON','',function(response){
		try {
			if(page_no == 1) {
				datatable = new simpleDatatables.DataTable('#api-box table',{
					perPage: 15,
					scrollY: '100%',
					columns: [{
						select: [4,5],
						sortable: false
					},{
						select: [2,3],
						type: 'number'
					}]
				});
			}
			for (let i = 0; i < response.items.length; i++){
				let is_answered = (response.items[i]['is_answered'] ? `<i class="text-green fa-solid fa-check"></i>` : `<i class="text-red fa-solid fa-xmark"></i>`);
				let newrow = [{
					'Title':response.items[i]['title'],
					'Tags':response.items[i]['tags'].join(', '),
					'Score':response.items[i]['score'],
					'View count':response.items[i]['view_count'],
					'Answered':is_answered,
					'Link':'<a href="'+response.items[i]['link']+'" target="_blank" rel="noopener noreferrer"><i class="text-blue fa-solid fa-link"></i></a>'
				}];
				datatable.insert(newrow);
			}
		} catch {
			console.log(response);
			document.getElementById('api-box').innerHTML = '<p class="text-red grid-w-12"><i class="fa-solid fa-triangle-exclamation"></i> Stack Overflow is not available at the moment, please try again later</p>';
		}
	});
}