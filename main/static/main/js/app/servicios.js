$( document ).ready( function(){

	var template    = _.template( $('.item-servicio-tpl').html() ),
		url         = '/search_servicio/',
		$searchForm = $('#search-form');


	$searchForm.find('input').on('keypress', function() {
		if (event.keyCode === 13) { 
            event.preventDefault();
        }
	})

	$searchForm.find('input').on('keyup', function(event) {

		if (!/^([0-9])*$/.test(event.target.value)) {
			$searchForm.find('.dropdown-menu').remove();
			$searchForm.find('.form-group').addClass('has-error');
			return;
		}
		if (event.target.value == '') {
			$searchForm.find('.form-group').removeClass('has-error');
			$searchForm.find('.dropdown-menu').remove();		
			return;
		}

		$searchForm.find('.form-group').removeClass('has-error');
      		

		var datos = {
			key: $searchForm.find('.search-query').val(),
		};

		$.get(url, datos)
			
			.always(function(data) {
				var $menu = $('<ul class="dropdown-menu" style="width:250px; max-height:350px; overflow-y:auto;"> </ul>');
				
				if (data.length == 0) {
					$menu.html('<li class="dropdown-header">Oops, No se encontraron resultados..!</li>');
				} else {					
					$.each(data, function(i, serv) {
						var servicio = {
							pk       : serv.pk,
							estado   : serv.fields.estado
						}
						console.log(serv);

						$menu.append( template(serv) );
					});
					$menu.find('li:last').remove();  // remover el ultimo divider
				}

				$searchForm.find('.dropdown-menu').remove();
				$searchForm.find('.input-group').append($menu).addClass('open');
			});
	});


	function truncText (text, maxLength, ellipseText){
        ellipseText = ellipseText || '&hellip;';
       
        if (text.length < maxLength) 
            return text;
 
        //Find the last piece of string that contain a series of not A-Za-z0-9_ followed by A-Za-z0-9_ starting from maxLength
        var m = text.substr(0, maxLength).match(/([^A-Za-z0-9_]*)[A-Za-z0-9_]*$/);
        if(!m) return ellipseText;
        
        //Position of last output character
        var lastCharPosition = maxLength-m[0].length;
        
        //If it is a space or "[" or "(" or "{" then stop one before. 
        if(/[\s\(\[\{]/.test(text[lastCharPosition])) lastCharPosition--;
        
        //Make sure we do not just return a letter..
        return (lastCharPosition ? text.substr(0, lastCharPosition+1) : '') + ellipseText;
    }


});