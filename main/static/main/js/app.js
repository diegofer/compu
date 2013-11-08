// $(function() {
//   $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
// });

$( document ).ready( function(){

	// var item = $('.nav-servicios a[href^="' + location.pathname + '"]').addClass('active');
	// console.log(item);
	function inicializar() {

		var modalServicio      = $('#modal-form-servicio'),
			modalPersona       = $('#modal-form-persona'),
		    modalTipoServicio  = $('#modal-form-tipo-servicio'),
			modalMarca         = $('#modal-form-marca'),

			formServicio     = modalServicio.find('form').html(),
			formPersona      = modalPersona.find('form').html(),
			formTipo         = modalTipoServicio.find('form').html(),
			formMarca        = modalMarca.find('form').html();



		var compu = {

			initCompu: function() {
				this.setActionsFormServicio();	
				this.setActionsFormTipo();					

				$('#servicio-btn').on('click',{modal:modalServicio}, this.showModal);

				$('#guardar-servicio-btn').on('click', this.guardarServicio);
				$('#guardar-persona-btn').on('click', this.guardarPersona);
				$('#guardar-tipo-servicio-btn').on('click', this.guardarTipoServicio);
				$('#guardar-marca-btn').on('click', this.guardarMarca);

				modalServicio.on('hidden.bs.modal', this.alHideServicio);
				modalPersona.on('hidden.bs.modal', this.alHidePersona);			
				modalTipoServicio.on('hidden.bs.modal', this.alHideTipoServicio);			
				modalMarca.on('hidden.bs.modal', this.alHideMarca);		
			},


			setActionsFormServicio: function() {
				$('#cliente-btn').on('click', {modal:modalPersona}, this.showModal);
				$('#tipo-btn').on('click', {modal:modalTipoServicio}, this.showModal);
				$('#marca-btn').on('click', {modal:modalMarca}, this.showModal);

				$('#id_cliente,#id_tipo,#id_marca').select2({
					formatNoMatches: function(m){return 'Oops, no se encontraron resultados!';}
				});
			},


				clearActionsFormServico: function() {
					$('#cliente-btn, #tipo-btn, #marca-btn').off();
					$('#id_cliente').select2("destroy");
					$('#id_tipo').select2("destroy");
					$('#id_marca').select2("destroy");
				},
				
			

			setActionsFormTipo: function() {
				function format(state) {
				    if (!state.id) return state.text; // optgroup
				    return "<i class='fa fa-fw fa-"+state.text+"'></i> "+ state.text; //state.text;
				}

			    $('#id_icon').select2({
			    	formatResult: format,
				    formatSelection: format,
				    escapeMarkup: function(m) { return m; }
			    });
			},

				clearActionsFormTipo: function() {
					$('#id_icon').select2("destroy");
				},
			
			
			showModal: function(event) {	
				
				event.preventDefault();
				console.log('estoy mostrando una modal');
				event.data.modal.modal('show');		
			},


			alHideServicio: function() {
				compu.clearActionsFormServico();
				$('#form-servicio').html(formServicio);
				compu.setActionsFormServicio();
			},

			alHidePersona: function() {
				$('#form-persona ').html(formPersona);
			},	


			alHideTipoServicio: function() {
				clearActionsFormTipo();
				$('#form-tipo-servicio').html(formTipo);
				compu.setActionsFormTipo();
			},


			alHideMarca: function() {
				$('#form-marca').html(formMarca);
			},
			
			



			/////////	AJAX METODOS  /////////

			guardarServicio: function(event) {
				var $btn =  $(event.target).button('loading');

				compu.ajax({
					url  : urlGuardarServicio,
					form : '#form-servicio',
					btn  : $btn
				});
			},


			guardarPersona: function() {
				var $btn =  $(event.target).button('loading');

				$(event.target).button('loading');
				compu.ajax({
					url  : urlGuardarPersona,
					form : '#form-persona',
					btn  : $btn
				});
			},


			guardarTipoServicio: function() {
				var $btn =  $(event.target).button('loading');

				compu.ajax({
					url  : urlGuardarTipoServicio,
					form : '#form-tipo-servicio',
					btn  : $btn
				});
			},


			guardarMarca: function() {
				var $btn =  $(event.target).button('loading');

				compu.ajax({
					url  : urlGuardarMarca,
					form : '#form-marca',
					btn  : $btn
				});
			},
				


			ajax: function(options) {
				
				$.ajax({
				    url: options.url,
				    type: "POST",
				    data: $(options.form).serialize(),

				    success: function(data) {
				        if (!(data['success'])) {
				            $(options.form).replaceWith(data['form_html']); // OJO replace mata los listener y referencias...
				            
				            if (options.url == urlGuardarServicio) compu.setActionsFormServicio();
				            if (options.url == urlGuardarTipoServicio) compu.setActionsFormTipo();      
				        }
				        else {
				        	if (options.url == urlGuardarServicio) location.reload();
	
				        	if (options.url == urlGuardarPersona) compu.successOk('#id_cliente', data, modalPersona);

				        	if (options.url == urlGuardarTipoServicio) compu.successOk('#id_tipo', data, modalTipoServicio);
			
				        	if (options.url == urlGuardarMarca) compu.successOk('#id_marca', data, modalMarca);			            
				        }

				        options.btn.button('reset');
				    },
				    error: function () {
				    	console.log('tengo errores');
				        $(options.form).find('.error-message').show()
				    }
				});
			},


			successOk: function(selector, data, modal) {
				var select = $('#form-servicio '+selector).append('<option value="'+ data['value']+'">'+data['nombre']+'</opotion>');
        		select.val(''+data.value+'');	
        		select.trigger('change');		
        		modal.modal('hide');
			},
			


		};

		return compu;
	};

	var initApp = inicializar();
    initApp.initCompu();

	
    

});