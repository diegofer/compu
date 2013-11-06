// $(function() {
//   $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
// });

$( document ).ready( function(){

	// var item = $('.nav-servicios a[href^="' + location.pathname + '"]').addClass('active');
	// console.log(item);
	function inicializar() {

		formServicioModal = $('#modal-form-servicio');
		formPersonaModal  = $('#modal-form-persona');

		var compu = {

			initCompu: function() {
				this.setChosen();						
				this.setEvents();
			},
				

			setChosen: function() {
				$('#id_cliente').chosen({
			        no_results_text: "Oops, no se encontraron resultados!",
			        width: "100%"
			    });
			},
			

			setEvents: function(arg) {
				$('#servicio-btn').on('click', this.alClickServicio);
				$('#cliente-btn').on('click', this.alClickCliente);

				$('#guardar-servicio-btn').on('click', this.guardarServicio);
				$('#guardar-persona-btn').on('click', this.guardarPersona);

				formPersonaModal.on('hidden.bs.modal', this.alHidePersona);
			},

			clearEvents: function() {
				$('#servicio-btn').off('click', this.alClickServicio);
				$('#cliente-btn').off('click', this.alClickCliente);

				$('#guardar-servicio-btn').off('click', this.guardarServicio);
				$('#guardar-persona-btn').off('click', this.guardarPersona);

				formPersonaModal.off('hidden.bs.modal', this.alHidePersona);
			},
			
		


			alClickServicio: function(event) {	
				formServicioModal.modal('show');
				event.preventDefault();
			},


			alClickCliente: function() {
				console.log('click en agregar cliente');
				formServicioModal.modal('hide');
				formPersonaModal.modal('show');
			},

			alHideServicio: function() {
				//formPersonaModal.modal('show');
			},

			alHidePersona: function() {
				formServicioModal.modal('show');
			},	

			/////////	AJAX METODOS  /////////

			guardarServicio: function() {
				// compu.ajax({
				// 	url: urlGuardarServicio,
				// 	form: '#form-servicio',
				// });

				var select = $('#form-servicio #id_cliente')
        			.append('<option value="79">hola soy yo</opotion>');
        		select.val("79");
        		select.trigger("chosen:updated");
			},


			guardarPersona: function() {
				compu.ajax({
					url: urlGuardarPersona,
					form: '#form-persona'
				});
			},
				


			ajax: function(options) {
				
				$.ajax({
				    url: options.url,
				    type: "POST",
				    data: $(options.form).serialize(),

				    success: function(data) {
				        if (!(data['success'])) {
				            $(options.form).replaceWith(data['form_html']);
				            //$(event.target).button('reset');
				          	compu.clearEvents();
				            compu.setEvents();
				        }
				        else {
				        	if (options.url == urlGuardarServicio) {
				        		location.reload();
				        	}
				        	if (options.url == urlGuardarPersona) {
				        		formPersonaModal.modal('hide');  // cierro el formulario persona
				        		var select = $('#form-servicio #id_cliente')
				        			.append('<option value="'+ data['persona_id']+'">'+data['persona']+'</opotion>');
				        		select.val(''+data.persona_id+'');
				        		select.trigger("chosen:updated");
				        	}

				            
				        }
				    },
				    error: function () {
				    	console.log('tengo errores');
				        $(options.form).find('.error-message').show()
				    }
				});
			},
			
					

		};

		return compu;
	};

	var initApp = inicializar();
    initApp.initCompu();

	
    

});