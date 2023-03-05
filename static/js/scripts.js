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
	}).then(data => callback(data)).catch(error => console.trace(error));
};

graph_colour_list = ['#5F295F','#0074D9','#FF4136','#2ECC40','#FF851B','#7FDBFF','#B10DC9','#FFDC00','#001f3f','#39CCCC','#01FF70','#85144b','#F012BE','#3D9970','#111111','#AAAAAA'];
//Creates a chart and places it in supplied canvas
function createChart(ctx,type,top_label,labels,data,options) {
	if (options == 'horizontal') {
		axis = 'y';
	} else {
		axis = '';
	}
	const chart = new Chart(ctx, {
		type: type,
		responsive: true,
		maintainAspectRatio: false,
		data: {
			labels: labels,
			datasets: [{
				label: top_label,
				data: data,
				backgroundColor: graph_colour_list.sort( () => .5 - Math.random() ),
				borderWidth: 1
			}]
		},
		options: {
			indexAxis: axis		
		}
	});
	return chart;
};

/* -------------------------------------------------------------------------- */
/*                                    Index                                   */
/* -------------------------------------------------------------------------- */
//asnyc function to reduce spam
async function index_bar_asyncCall(type,count) {
	document.getElementById('more-'+type).disabled = true;
	document.getElementById('less-'+type).disabled = true;
	result = await update_index_bar_chart(type, count);
	document.getElementById('more-'+type).disabled = false;
	if(count > 5) {
		document.getElementById('less-'+type).disabled = false;
		document.getElementById('less-'+type).style.cursor = 'pointer';
	} else {
		document.getElementById('less-'+type).style.cursor = 'not-allowed';
	}
}

function update_index_bar_chart(type, count) {
	chart = (type == 'tags' ? index_tag_chart : index_badge_chart);
	return new Promise((resolve, reject) => {
		if (count < chart.data.labels.length) {
			chart.data.labels.splice(-5, 5); // remove the label first
			chart.data.datasets.forEach(dataset => {
				dataset.data.pop();
			});
			chart.update();
			resolve(true);
		} else {
			makeHttpRequest('/ajax/update_index_bar_chart?count='+count+'&type='+type,'GET','JSON','',function(response) {
				if (response.success) {
					for (let index = chart.data.labels.length; index < response.data.count.length; ++index) {
						chart.data.labels.push(response.data.names[index]);
						chart.data.datasets[0].data[index] = response.data.count[index];
					}
					chart.update();
					resolve(true);
				} else {
					document.getElementById(type+'-wrapper').innerHTML = '<h1 class="grid-w-9 grid-sw12 text-red">An error occured, if the problem persists please contact the administration staff<h1>';
					reject(false);
				}		
			});
		}
	});
}

/* -------------------------------------------------------------------------- */
/*                                  Trending                                  */
/* -------------------------------------------------------------------------- */
function load_trending_table(page_no) {
	let api_url;
	if (page_no == 1) {
		api_url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=month&site=stackoverflow';
	} else {
		api_url = 'https://api.stackexchange.com/2.3/questions?page='+page_no+'&order=desc&sort=month&site=stackoverflow';
	}
	makeHttpRequest(api_url,'GET','JSON','',function(response) {
		try {
			if(page_no == 1) {
				datatable = new simpleDatatables.DataTable('#api-box table',{
					perPage: 15,
					columns: [{
						select: [5,6],
						sortable: false
					},{
						select: [3,4],
						type: 'number'
					}]
				});
			}
			for (let i = 0; i < response.items.length; i++){
				let is_answered = (response.items[i]['is_answered'] ? `<i class="text-green fa-solid fa-check"></i>` : `<i class="text-red fa-solid fa-xmark"></i>`);
				let newrow = [{
					'Title':response.items[i]['title'],
					'User':'<a href="'+response.items[i]['owner']['link']+'"target="_blank" rel="noopener noreferrer">'+response.items[i]['owner']['display_name']+'</a>',
					'Tags':response.items[i]['tags'].join(', '),
					'Score':response.items[i]['score'],
					'Views':response.items[i]['view_count'],
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

/* -------------------------------------------------------------------------- */
/*                                    Tags                                    */
/* -------------------------------------------------------------------------- */

function load_tags_table(response) {
		datatable = new simpleDatatables.DataTable('.tags-main table',{
			perPage: 15,
			columns: [{
				select: 7,
				sortable: false
			},{
				select: [1,2,3,4,5],
				type: 'number'
			}]
		});
		let rows = response.top_tags.data;
		for (let i = 0; i < rows.tag_name.length; i++) {
			let newrow = [{
				'Tag':rows.tag_name[i],
				'Question Count':rows.question_count[i],
				'Answers Count':rows.answer_count[i],
				'Comments Count':rows.comment_count[i],
				'Total Score':rows.score[i],
				'Total Views':rows.view_count[i],
				'Sentiment Score':rows.sentiment[i],
				'About':'<a href="'+rows.link[i]+'" target="_blank" rel="noopener noreferrer"><i class="text-blue fa-solid fa-link"></i></a>'
			}];
			datatable.insert(newrow);
		}

}


/* -------------------------------------------------------------------------- */
/*                                     NAV                                    */
/* -------------------------------------------------------------------------- */
// Nav menu Called on resize and closing
function reset_nav_menu() {
	document.getElementById('side-nav-container').style.width = 0;
	document.querySelector('body').style.marginLeft = 0;
	document.querySelector('aside nav').style.opacity = 0;
	document.getElementById('nav-btn-open').style.opacity = 100;
	document.getElementsByClassName('active')[0].style.opacity = 0;
}

document.addEventListener("DOMContentLoaded", () => {
	// Header animation handling
	document.getElementById('nav-btn-open').addEventListener('click', () => {
		document.getElementById('side-nav-container').style.width = '6rem';
		document.querySelector('body').style.marginLeft = '6rem';
		document.querySelector('aside nav').style.opacity = 100;
		document.getElementById('nav-btn-open').style.opacity = 0;
		document.getElementsByClassName('active')[0].style.opacity = 100;
	});
	
	document.getElementById('nav-btn-close').addEventListener('click', () => {
		reset_nav_menu();
	});
	
	window.addEventListener('resize', () => {
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

	// Info panel handling
	document.getElementById('info-modal-open').addEventListener('click', () => {
		document.querySelector('main').style.filter = 'blur(2px)';
		document.getElementById('info-modal').showModal();
	});

	document.getElementById('info-modal-close').addEventListener('click', () => {
		document.querySelector('main').style.filter = 'none';
		document.getElementById('info-modal').close();
	});

	/* ---------------------------------- index --------------------------------- */
	document.querySelectorAll('.index-tag').forEach(el => el.addEventListener('click', e => {
		if(e.target && ((e.target.id || e.target.parentNode.id) == 'more-tags')) {
			count = tag_count = tag_count + 5;
			type = 'tags';
		} else if(e.target && (e.target.id || e.target.parentNode.id) == 'less-tags') {
			count = tag_count = tag_count - 5;
			type = 'tags';
		} else if(e.target && (e.target.id || e.target.parentNode.id) == 'more-badges') {
			count = badge_count = badge_count + 5;
			type = 'badges';
		} else if(e.target && (e.target.id || e.target.parentNode.id) == 'less-badges') {
			count = badge_count = badge_count - 5;
			type = 'badges';
		}
		index_bar_asyncCall(type, count);
	}));
});