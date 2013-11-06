// $(function() {
//   $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
// });

$( document ).ready( function(){

	// var item = $('.nav-servicios a[href^="' + location.pathname + '"]').addClass('active');
	// console.log(item);
	function inicializar() {

		modalServicio      = $('#modal-form-servicio');
		modalPersona       = $('#modal-form-persona');
		modalTipoServicio  = $('#modal-form-tipo-servicio');
		modalMarca         = $('#modal-form-marca');

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
				$('#tipo-btn').on('click', this.alClickTipo);
				$('#marca-btn').on('click', this.alClickMarca);


				$('#guardar-servicio-btn').on('click', this.guardarServicio);
				$('#guardar-persona-btn').on('click', this.guardarPersona);
				$('#guardar-tipo-servicio-btn').on('click', this.guardarTipoServicio);
				$('#guardar-marca-btn').on('click', this.guardarMarca);

				modalServicio.on('hidden.bs.modal', this.alHideServicio);
				modalPersona.on('hidden.bs.modal', this.alHidePersona);			
				modalTipoServicio.on('hidden.bs.modal', this.alHideTipoServicio);			
				modalMarca.on('hidden.bs.modal', this.alHideMarca);			
			},

			clearEvents: function() {
				$('#servicio-btn').off('click', this.alClickServicio);
				$('#cliente-btn').off('click', this.alClickCliente);
				$('#tipo-btn').off('click', this.alClickTipo);
				$('#marca-btn').off('click', this.alClickMarca);

				$('#guardar-servicio-btn').off('click', this.guardarServicio);
				$('#guardar-persona-btn').off('click', this.guardarPersona);
				$('#guardar-tipo-servicio-btn').off('click', this.guardarTipoServicio);
				$('#guardar-marca-btn').off('click', this.guardarMarca);

				modalServicio.on('hidden.bs.modal', this.alHideServicio);
				modalPersona.off('hidden.bs.modal', this.alHidePersona);
				modalTipoServicio.off('hidden.bs.modal', this.alHideTipoServicio);			
				modalMarca.off('hidden.bs.modal', this.alHideMarca);
			},
			
		


			alClickServicio: function(event) {	
				event.preventDefault();
				modalServicio.modal('show');		
			},


			alClickCliente: function() {
				modalServicio.modal('hide');
				modalPersona.modal('show');
			},


			alClickTipo: function() {
				modalServicio.modal('hide');
				modalTipoServicio.modal('show');
			},

			alClickMarca: function() {
				modalServicio.modal('hide');
				modalMarca.modal('show');
			},
			

			alHideServicio: function() {
				$('#form-servicio ')[0].reset();
				$('#id_cliente').trigger("chosen:updated");
			},

			alHidePersona: function() {
				$('#form-persona ')[0].reset();
				modalServicio.modal('show');
			},	


			alHideTipoServicio: function() {
				$('#form-tipo-servicio')[0].reset();
				modalServicio.modal('show');
			},


			alHideMarca: function(arg) {
				$('#form-marca ')[0].reset();
				modalServicio.modal('show');
			},
			
			



			/////////	AJAX METODOS  /////////

			guardarServicio: function() {
				compu.ajax({
					url: urlGuardarServicio,
					form: '#form-servicio',
				});
			},


			guardarPersona: function() {
				compu.ajax({
					url: urlGuardarPersona,
					form: '#form-persona'
				});
			},


			guardarTipoServicio: function() {
				compu.ajax({
					url: urlGuardarTipoServicio,
					form: '#form-tipo-servicio'
				});
			},


			guardarMarca: function() {
				compu.ajax({
					url: urlGuardarMarca,
					form: '#form-marca'
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
				        	};
				        	if (options.url == urlGuardarPersona) {
				        		modalPersona.modal('hide');  // cierro el formulario persona
				        		var select = $('#form-servicio #id_cliente')
				        			.append('<option value="'+ data['value']+'">'+data['nombre']+'</opotion>');
				        		select.val(''+data.value+'');
				        		select.trigger("chosen:updated");
				        	};
				        	if (options.url == urlGuardarTipoServicio) {
				        		modalTipoServicio.modal('hide');
				        		var select = $('#form-servicio #id_tipo')
				        			.append('<option value="'+ data['value']+'">'+data['nombre']+'</opotion>');
				        		select.val(''+data.value+'');
				        	};
				        	if (options.url == urlGuardarMarca) {
				        		modalMarca.modal('hide');
				        		var select = $('#form-servicio #id_marca')
				        			.append('<option value="'+ data['value']+'">'+data['nombre']+'</opotion>');
				        		select.val(''+data.value+'');
				        	};

				            
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