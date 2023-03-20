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
/* ---------------------------- init autoComplete --------------------------- */
function make_auto_complete(selector,placeholder,data) {
	const autoCompleteJS = new autoComplete({
		selector: selector,
		placeHolder: placeholder,
		data: {
			src: data,
			cache: true,
			keys: ['tag'] 
		},
		resultsList: {
			element: (list, data) => {
				if (!data.results.length) {
					// Create "No Results" message element
					const message = document.createElement("div");
					// Add class to the created element
					message.setAttribute("class", "no_result");
					// Add message text content
					message.innerHTML = `<span>Found No Results for "${data.query}"</span>`;
					// Append message element to the results list
					list.prepend(message);
				}
			},
			noResults: true,
			maxResults: 50
		},
		resultItem: {
			highlight: true
		},
		events: {
			input: {
				selection(event) {
					add_to_filters(event.detail.selection.value.id,event.detail.selection.value.tag);
				}
			}
		}
	});
	return autoCompleteJS;
};

function add_to_filters(key,name) {
	document.getElementsByClassName('filter-list')[0].innerHTML+='<li data-id="'+key+'"><span>'+name+'</span><i class="fa-solid fa-xmark remove-filter"></li>';
	document.getElementById('hidden-form').innerHTML+='<input type="hidden" name="'+name+'" value="'+key+'">';
}

function init_tag_form(url) {
	document.addEventListener('click', function(e) {
		if(e.target && e.target.classList.contains('remove-filter')) {
			document.querySelector('input[value="'+e.target.parentElement.dataset.id+'"]').remove();
			e.target.parentElement.remove();
		}
	});
	//Form submission
	let tag_filter_form = document.getElementById('tag-filter-form');
	tag_filter_form.addEventListener('submit', function(e) {
		document.getElementById('submit-form').disabled = true;
		e.preventDefault();
		let data = new FormData(tag_filter_form);
		makeHttpRequest(url,'POST','JSON',data,function(response) {
			if(response['success']) {
				document.getElementById('submit-form').disabled = false;
				switch(url) {
					case '/ajax/filtered_tags':
						load_tags_table(response['data']);
						break;
					case '/ajax/filtered_posts':
						load_posts_keyword_table(response.post_keywords.data);
						load_posts_top_table(response.top_posts.data);
						create_post_charts(response);
						break;
					case '/ajax/filtered_users':
						load_user_keyword_table(response.user_keywords.data);
						load_badges_table(response.filtered_top_badges.data);
						load_user_year_chart(response.user_years);
						break;
					case '/ajax/filtered_locations':
						load_location_table(response.locations.data);
						break;
				}
			} else {
				tag_filter_form.innerHTML = '<h1 class="grid-w-9 grid-sw12 text-red">An error occured, if the problem persists please contact the administration staff<h1>';
			}
		});
	});
}

// Handles Exporting Datatable logic
function export_datatable(table) {
	document.querySelector("button.csv").addEventListener("click", () => {
		simpleDatatables.exportCSV(table, {
			download: true,
			lineDelimiter: "\n",
			columnDelimiter: ","
		})
	});
	document.querySelector("button.sql").addEventListener("click", () => {
		simpleDatatables.exportSQL(table, {
			download: true,
			tableName: "export_table"
		});
	});
	document.querySelector("button.txt").addEventListener("click", () => {
		simpleDatatables.exportTXT(table, {
			download: true
		});
	});
	document.querySelector("button.json").addEventListener("click", () => {
		simpleDatatables.exportJSON(table, {
			download: true,
			space: 3
		});
	});
}

/* -------------------------------------------------------------------------- */
/*                                    Index                                   */
/* -------------------------------------------------------------------------- */
function init_index() {
	let tag_count;
	let badge_count;
	let index_tag_chart;
	let index_badge_chart;
	let accept_doughnut_chart;
	let user_line_chart;
	makeHttpRequest('/ajax/load_index','GET','JSON','',function(response) {
		tag_count = response.top_tags.data.count.length;
		badge_count = response.top_badges.data.count.length;
		let acceptance = [
			response.question_details.data[0],
			response.question_details.data[1],
			response.table_row_count.data.question - response.question_details.data[0] - response.question_details.data[1]
		];
		//Chart initialisation
		let tag_ctx = document.getElementById('tagChart');
		let accept_ctx = document.getElementById('acceptanceChart');
		let badge_ctx = document.getElementById('badgeChart');
		let user_ctx = document.getElementById('userChart');
		index_tag_chart = createChart(tag_ctx,'bar','Questions with this tag',response.top_tags.data.names,response.top_tags.data.count,'');
		index_badge_chart = createChart(badge_ctx, 'bar', 'Most earned badge',response.top_badges.data.names,response.top_badges.data.count,'');
		accept_doughnut_chart = createChart(accept_ctx, 'doughnut','',['Unanswered','Not Accepted', 'Accepted'],acceptance,'');
		user_line_chart = createChart(user_ctx, 'line','Age of users by year',response.user_years.data.years,response.user_years.data.count,'');
		//Accessibility
		document.querySelector('#tagChart p').innerHTML = 'Tag names:'+response.top_tags.data.names+'Count:'+response.top_tags.data.count;
		document.querySelector('#badgeChart p').innerHTML = 'Badge names:'+response.top_badges.data.names+'Count:'+response.top_badges.data.count;
		document.querySelector('#acceptanceChart p').innerHTML = 'Unanswered:'+acceptance[0]+'Answered, not accepted:'+acceptance[1]+'Accepted:'+acceptance[2];
		document.querySelector('#userChart p').innerHTML = 'Years:'+response.user_years.data.years+'Users created that year:'+response.user_years.data.count;
	});
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
}
/* -------------------------------------------------------------------------- */
/*                                  Trending                                  */
/* -------------------------------------------------------------------------- */
function init_trending() {
	let page_no = 1;
	load_trending_table(page_no);
	document.getElementById('load-api-posts').addEventListener('click', function() {
		page_no++;
		load_trending_table(page_no);
	});
}

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
function init_tags() {
	//Page Load
	makeHttpRequest('/ajax/load_tags','GET','JSON','',function(response) {
		tag_list = make_auto_complete('#tag_search','Search for tags...',response.tag_list.data);
		load_tags_table(response.top_tags.data);
		init_tag_form('/ajax/filtered_tags');
	});
}

function load_tags_table(rows) {
	if (typeof datatable !== 'undefined') {
		datatable.destroy();
	}
	datatable = new simpleDatatables.DataTable('.tags-main table',{
		perPage: 25,
		columns: [{
			select: 7,
			sortable: false
		},{
			select: [1,2,3,4,5,6],
			type: 'number'
		}]
	});
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
	export_datatable(datatable);
}
/* -------------------------------------------------------------------------- */
/*                                    Posts                                   */
/* -------------------------------------------------------------------------- */
function init_posts() {
	makeHttpRequest('/ajax/load_posts','GET','JSON','',function(response) {
		tag_list = make_auto_complete('#tag_search','Search for tags...',response.tag_list.data);
		load_posts_keyword_table(response.post_keywords.data);
		load_posts_top_table(response.top_posts.data);
		create_post_charts(response);
		init_tag_form('/ajax/filtered_posts');
	});
}

function create_post_charts(response) {
	if (typeof accept_doughnut_chart !== 'undefined') {
		accept_doughnut_chart.destroy();
	}
	if (typeof engagement_chart !== 'undefined') {
		engagement_chart.destroy();
	}
	let acceptance = [
		response.question_details.data[0],
		response.question_details.data[1],
		response.table_row_count.data.question - response.question_details.data[0] - response.question_details.data[1]
	];
	let engagement = [
		response.table_row_count.data.question / response.question_details.data[0],
		response.table_row_count.data.question / response.question_details.data[1]
	];
	let accept_ctx = document.getElementById('acceptanceChart');
	let engagement_ctx = document.getElementById('engagementChart');
	accept_doughnut_chart = createChart(accept_ctx, 'doughnut','',['Unanswered','Not Accepted', 'Accepted'],acceptance,'');
	engagement_chart = createChart(engagement_ctx, 'bar','Engagement level',['Average Answers','Average Comments'], engagement,'');
		//Accessibility
	document.querySelector('#acceptanceChart p').innerHTML = 'Unanswered:'+acceptance[0]+'Answered, not accepted:'+acceptance[1]+'Accepted:'+acceptance[2];
	document.querySelector('#engagementChart p').innerHTML = 'Average Answers:'+engagement[0]+'Average Comments:'+engagement[1];
}

function load_posts_keyword_table(rows) {
	if (typeof key_word_datatable !== 'undefined') {
		key_word_datatable.destroy();
	}
	key_word_datatable = new simpleDatatables.DataTable('.posts-main article table',{
		perPageSelect: false,
		perPage: 25,
		columns: [{
			select: [1,2,3,4,5,6],
			type: 'number'
		}]
	});
	for (let i = 0; i < rows.keyword.length; i++) {
		let newrow = [{
			'Keyword':rows.keyword[i],
			'Question Count':rows.question_count[i],
			'Answers Count':rows.answer_count[i],
			'Comments Count':rows.comments_count[i],
			'Total Views':rows.view_count[i],
			'Total Score':rows.total_score[i],
			'Sentiment Score':rows.sentiment[i]
		}];
		key_word_datatable.insert(newrow);
	}
	export_datatable(key_word_datatable);
}

function load_posts_top_table(rows) {
	if (typeof posts_datatable !== 'undefined') {
		posts_datatable.destroy();
	}
	posts_datatable = new simpleDatatables.DataTable('.posts-main section table',{
		perPage: 5,
		perPageSelect: false,
		columns: [{
			select: [1],
			type: 'number'
		},{
			select: [2],
			sortable: false
		}
	]
	});
	for (let i = 0; i < rows.title.length; i++) {
		let newrow = [{
			'Title':rows.title[i],
			'Score':rows.score[i],
			'Link':'<a href="'+rows.link[i]+'" target="_blank" rel="noopener noreferrer"><i class="text-blue fa-solid fa-link"></i></a>'
		}];
		posts_datatable.insert(newrow);
	}
}
/* -------------------------------------------------------------------------- */
/*                                    Users                                   */
/* -------------------------------------------------------------------------- */
function init_users() {
	makeHttpRequest('/ajax/load_users','GET','JSON','',function(response) {
		tag_list = make_auto_complete('#tag_search','Search for tags...',response.tag_list.data);
		load_user_keyword_table(response.user_keywords.data);
		load_badges_table(response.top_badges.data);
		load_user_year_chart(response.user_years);
		init_tag_form('/ajax/filtered_users');
	});
}

function load_user_keyword_table(rows) {
	if (typeof key_word_datatable !== 'undefined') {
		key_word_datatable.destroy();
	}
	key_word_datatable = new simpleDatatables.DataTable('#keyword-table',{
		perPage: 25,
		columns: [{
			select: [1,2,3],
			type: 'number'
		}]
	});
	for (let i = 0; i < rows.keyword.length; i++) {
		let newrow = [{
			'Keyword':rows.keyword[i],
			'Occurance Count':rows.occ_count[i],
			'Average Reputation':rows.avg_rep[i],
			'Total Reputation':rows.total_rep[i],
			'Average Creation Date':rows.avg_acc_age[i]
		}];
		key_word_datatable.insert(newrow);
	}
	export_datatable(key_word_datatable);
}

function load_badges_table(rows) {
	if (typeof badges_datatable !== 'undefined') {
		badges_datatable.destroy();
	}
	badges_datatable = new simpleDatatables.DataTable('#badges-table',{
		perPage: 5,
		columns: [{
			select: [1],
			type: 'number'
		}]
	});
	for (let i = 0; i < rows.names.length; i++) {
		let newrow = [{
			'Badge':rows.names[i],
			'Count':rows.count[i]
		}];
		badges_datatable.insert(newrow);
	}
}

function load_user_year_chart(response) {
	if (typeof user_line_chart !== 'undefined') {
		user_line_chart.destroy();
	}
	let user_ctx = document.getElementById('userChart');
	user_line_chart = createChart(user_ctx, 'line','Age of users by year',response.data.years,response.data.count,'');
	document.querySelector('#userChart p').innerHTML = 'Years:'+response.data.years+'Users created that year:'+response.data.count;
}

/* -------------------------------------------------------------------------- */
/*                                  Locations                                 */
/* -------------------------------------------------------------------------- */
function init_locations() {
	makeHttpRequest('/ajax/load_locations','GET','JSON','',function(response) {
		tag_list = make_auto_complete('#tag_search','Search for tags...',response.tag_list.data);
		load_location_table(response.locations.data);
		init_tag_form('/ajax/filtered_locations');
	});
}

function load_location_table(rows) {
	if (typeof location_datatable !== 'undefined') {
		location_datatable.destroy();
	}
	location_datatable = new simpleDatatables.DataTable('#location-table',{
		perPage: 25,
		columns: [{
			select: [1,2,4,5,6,7],
			type: 'number'
		}]
	});
	for (let i = 0; i < rows.location.length; i++) {
		let newrow = [{
			'Location':rows.location[i],
			'Count':rows.count[i],
			'Average Reputation':rows.avg_rep[i],
			'Total Reputation':rows.total_rep[i],
			'Average Creation Date':rows.avg_acc_age[i],
			'Questions Asked':rows.question_count[i],
			'Answered Given':rows.answer_count[i],
			'Comments Made':rows.comment_count[i]
		}];
		location_datatable.insert(newrow);
	}
}

/* -------------------------------------------------------------------------- */
/*                                   Layout                                   */
/* -------------------------------------------------------------------------- */
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
});