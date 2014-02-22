$(document).ready(function(){
	var $panelTecnicoForm    = $('#panel-tecnico-form'),
		$cerrarFormBtn       = $panelTecnicoForm.find('.cerrar'),
		$panelTecnicoExist   = $('#panel-tecnico-exist'),
		panelTecnicoExistTpl = _.template( $('.panel-tecnico-exist-tpl').html() )
		wd  = window || document;
	

	$('.estado-btn').on('click', guardarEstado);
	$('#print-servicio-btn').on('click', printServicio);

	
	if ($panelTecnicoExist.length) { 
		$panelTecnicoForm.hide();
		setEvents();
	}

	function setEvents() {
		$('#panel-tecnico-exist').hover(alHoverIn, alHoverOut);
	}   
	
		function alHoverIn(){
			$(this).find('.editar').removeClass('hidden').addClass('show');
			$('#panel-tecnico-exist .editar').one('click', editarTecnico);
		}

		function alHoverOut(){
			$(this).find('.editar').removeClass('show').addClass('hidden');
		}


	

	function editarTecnico() {
		$('#panel-tecnico-exist').slideUp();
		$panelTecnicoForm.slideDown(); 
		$cerrarFormBtn.removeClass('hidden');
		$cerrarFormBtn.one('click', cerrarPanelTecnicoForm); 
	}

	function cerrarPanelTecnicoForm() {
		$panelTecnicoForm.slideUp();
		$('#panel-tecnico-exist').slideDown();
	}

	/////////////////  AJAX //////////////////

	setActionsFormServicioTecnico();

	function setActionsFormServicioTecnico() {
        $panelTecnicoForm.find('#id_tecnico').select2();
        $panelTecnicoForm.find('#guardar-servicio-tecnico-btn').on('click', guardarServicioTecnico);
    }

    function guardarServicioTecnico() {
    	var $btn =  $(event.target).button('loading');
    	var value = $panelTecnicoForm.find('#id_tecnico').val();

    	if ( value == null || value.length == 0 || /^\s+$/.test(value) ) {
    		$panelTecnicoForm.find('.form-group').addClass('has-error');
    		return;
    	}
    	
    	var data = $('#form-servicio-tecnico').serialize();
    	post = $.post(urlGuardarServicioTecnico, data );

    	post.always(function(data){
    	 	$('#panel-tecnico-exist').remove();
        	$panelTecnicoForm.after( panelTecnicoExistTpl(data) );
        	$panelTecnicoForm.slideUp();
        	$btn.button('reset');
        	setEvents();
        	servicio.tecnico = data.tecnico;
        });
    }

	function guardarEstado (event) {

	    if (!servicio.tecnico) {
	        var $modalAlert = $('#modal-alert'); 
	        $modalAlert.find('.msg').html('Asigne primero un Técnico...');
	        $modalAlert.modal('show');
	        return;
	    }
	    
	    var estadoBtn = $('#conten-estado .estado-btn').addClass('disabled'),
	        btnActual = $(event.currentTarget),
	        
	        data = {
	            estado: event.currentTarget.id,
	            servicio_id: $('#servicio-id').val(),
	            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
	        };
	        console.log(data.estado);

	    $.post(urlGuardarServicioEstado, data)
	        .fail(function() {
	            alert( "error" );
	        })
	        .always(function(data){
	            if (data.success) wd.location.reload(true);
	            else alert('no se puedo actualizar el estado, intentalo nuevamente');                     
	        });                        
	}


	/////////////////  AJAX //////////////////

	function printServicio (event) {
		event.preventDefault();
		window.print();
		window.focus();
		window.close();
	}

});