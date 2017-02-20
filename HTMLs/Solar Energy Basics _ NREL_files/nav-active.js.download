$(function(){

	//Side Navigation Higlighting
	$('ul.nav').find('li').each(function(i){

		var link = $(this).children('a').attr('href');
		var pathName = window.location.pathname;
		var href = pathName.indexOf('index.html') !== -1 ? pathName.substring(0, pathName.lastIndexOf('/')) + '/' : pathName;

		if(link === pathName){

			$(this).addClass('active');
			$(this).children('ul:first').removeClass('hide');

		}
	});

	//Top Navigation Higlighting
	$('ul.dropdown-menu').find('li').each(function(i){

		var link = $(this).children('a').attr('href');
		var pathName = window.location.pathname;
		var href = pathName.indexOf('index.html') !== -1 ? pathName.substring(0, pathName.lastIndexOf('/')) + '/' : pathName;

		if(href.indexOf(link) !== -1){

			$(this).parents("li").addClass("active");

		}
	});
})
