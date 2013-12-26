$( document ).ready( function(){

	

	var template = _.template( $('.cliente-tpl').html() ),
		$searchForm = $('#search-form');



	$searchForm.find('input').on('keypress', function() {
		if (event.keyCode === 13) { 
            event.preventDefault();
        }
	})

	$searchForm.find('input').on('keyup', function() {
		var datos = {
			key: $searchForm.find('.search-query').val(),
		};

		$.get('/search_cliente/', datos)
			
			.always(function(data) {
				var $menu = $('<ul class="dropdown-menu" style="width:250px; max-height:350px; overflow-y:auto;"> </ul>');
				
				if (data.length == 0) {
					$menu.html('<li class="dropdown-header">Oops, No se encontraron resultados..!</li>');
				} else {					
					$.each(data, function(i, cte) {
						var cliente = {
							pk       : cte.pk,
							fullName : truncText(cte.fields.nombre+' '+cte.fields.apellido, 27),
							cedula   : cte.fields.cedula
						}

						$menu.append( template(cliente) );
					});
				}

				$searchForm.find('.dropdown-menu').remove();
				$searchForm.append($menu).addClass('open');
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