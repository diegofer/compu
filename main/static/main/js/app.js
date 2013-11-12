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
			modalComponente    = $('#modal-form-componente'),

			formServicio     = modalServicio.find('form').html(),
			formPersona      = modalPersona.find('form').html(),
			formTipo         = modalTipoServicio.find('form').html(),
			formMarca        = modalMarca.find('form').html(),
			formComponente   = modalComponente.find('form').html();



		var compu = {

			initCompu: function() {
				
				this.setActionsFormServicio();	
				this.setActionsFormServicioTecnico();
				this.setActionsFormTipo();	
				this.setActionsFormComponente();				

				$('#servicio-btn').on('click',{modal:modalServicio}, this.showModal);
					$('.estado-btn').on('click', this.guardarEstado);

				$('#guardar-servicio-btn').on('click', this.guardarServicio);
				
				$('#guardar-persona-btn').on('click', this.guardarPersona);
				$('#guardar-tipo-servicio-btn').on('click', this.guardarTipoServicio);
				$('#guardar-marca-btn').on('click', this.guardarMarca);
				$('#guardar-componente-btn').on('click', this.guardarComponente);

				modalServicio.on('hidden.bs.modal', this.alHideServicio);
				modalPersona.on('hidden.bs.modal', this.alHidePersona);			
				modalTipoServicio.on('hidden.bs.modal', this.alHideTipoServicio);			
				modalMarca.on('hidden.bs.modal', this.alHideMarca);		
				modalComponente.on('hidden.bs.modal', this.alHideComponente);		
			},


			
			


			setActionsFormServicio: function() {
				$('#cliente-btn').on('click', {modal:modalPersona}, this.showModal);
				$('#tipo-btn').on('click', {modal:modalTipoServicio}, this.showModal);
				$('#marca-btn').on('click', {modal:modalMarca}, this.showModal);
				$('#componentes-btn').on('click', {modal:modalComponente}, this.showModal);

				$('#id_cliente,#id_tipo,#id_marca,#id_componentes').select2({
					formatNoMatches: function(m){return 'Oops, no se encontraron resultados!';}
				});
			},


				clearActionsFormServico: function() {
					$('#cliente-btn, #tipo-btn, #marca-btn').off();
					$('#id_cliente').select2("destroy");
					$('#id_tipo').select2("destroy");
					$('#id_marca').select2("destroy");
					$('#id_componentes').select2("destroy");
				},
						

				setActionsFormServicioTecnico: function() {
					$('#id_tecnico').select2();
					$('#guardar-servicio-tecnico-btn').on('click', this.guardarServicioTecnico);
				},


					clearActionsFormServicoTecnico: function() {
						$('#id_tecnico').select2("destroy");
						$('#guardar-servicio-tecnico-btn').off();
					},
					
			

			setActionsFormTipo: function() {
			    $('#form-tipo-servicio #id_icon').select2({
			    	formatResult: compu.iconFormat,
				    formatSelection: compu.iconFormat,
				    escapeMarkup: function(m) { return m; }
			    });
			},

				clearActionsFormTipo: function() {
					$('#form-tipo-servicio #id_icon').select2("destroy");
				},
			
			setActionsFormComponente: function() {
				$('#form-componente #id_icon').select2({
			    	formatResult: compu.iconFormat,
				    formatSelection: compu.iconFormat,
				    escapeMarkup: function(m) { return m; }
			    });
			},


				clearActionsFormComponente: function() {
					$('#form-componente #id_icon').select2("destroy");
				},
				

				iconFormat: function(state) {
					if (!state.id) return state.text; // optgroup
				    return "<i class='fa fa-fw fa-"+state.text+"'></i> "+ state.text; //state.text;
				},
			
			
			showModal: function(event) {	
				event.preventDefault();
				var selectedItems = $('#id_componentes').select2("val");
				console.log(selectedItems);
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
				compu.clearActionsFormTipo();
				$('#form-tipo-servicio').html(formTipo);
				compu.setActionsFormTipo();
			},


			alHideMarca: function() {
				$('#form-marca').html(formMarca);
			},


			alHideComponente: function() {
				compu.clearActionsFormComponente()
				$('#form-componente').html(formComponente);
				compu.setActionsFormComponente();
			},
			
			
			



			/////////	AJAX METODOS  /////////

			guardarServicio: function(event) {
				console.log($('#form-servicio').serialize());
				var $btn =  $(event.target).button('loading');

				compu.ajax({
					url  : urlGuardarServicio,
					form : '#form-servicio',
					btn  : $btn
				});
			},

				guardarEstado: function(event) {
					var data = {
						estado: event.currentTarget.id,
						servicio_id: $('#servicio-id').val(),
						csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
					};
					$.post(urlGuardarServicioEstado, data)
						.done(function(data){
							$('.icon-servicio').removeClass('en-cola en-revision reparado entregado').addClass(data.estado);
							$('#td-estado').text(data.estado);

							$('.estado-btn').removeClass().addClass('estado-btn btn btn-default');
							if (data.estado == 'en-cola') {
								$(event.currentTarget).removeClass().addClass('estado-btn btn btn-danger active');
							}
							if (data.estado == 'en-revision') {
								$(event.currentTarget).removeClass().addClass('estado-btn btn btn-warning active');
							}
							if (data.estado == 'reparado') {
								$(event.currentTarget).removeClass().addClass('estado-btn btn btn-success active');
							}
							if (data.estado == 'entregado') {
								$(event.currentTarget).removeClass().addClass('estado-btn btn btn-info active');
							}							
						});
				},


				guardarServicioTecnico: function() {
					var $btn =  $(event.target).button('loading');
					compu.ajax({
						url  : urlGuardarServicioTecnico,
						form : '#form-servicio-tecnico',
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

			guardarComponente: function() {
				var $btn =  $(event.target).button('loading');

				compu.ajax({
					url  : urlGuardarComponente,
					form : '#form-componente',
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
				            if (options.url == urlGuardarServicioTecnico) {
				            	compu.clearActionsFormServicoTecnico();
				            	compu.setActionsFormServicioTecnico();
				            	$(options.form).find('.form-group').addClass('has-error');
				            	$(options.form).find('input[name="id_servicio"]').val(data.id_servicio);

				            };
				            if (options.url == urlGuardarTipoServicio) compu.setActionsFormTipo(); 
				            if (options.url == urlGuardarComponente) compu.setActionsFormComponente();     
				        }
				        else {
				        	if (options.url == urlGuardarServicio) return window.location.href= data.url;

				        	if (options.url == urlGuardarServicioTecnico ) {
				        		var panelTecnico = $('#panel-tecnico').removeClass('panel-danger').addClass('panel-info');
				        		panelTecnico.find('.panel-heading').text('TÉCNICO');
				        		panelTecnico.find('.panel-body').html("<a href='"+data.url_tecnico+"' class='btn btn-info btn-block btn-lg'>"+data.tecnico+"</a>");
				        	}
	
				        	if (options.url == urlGuardarPersona) compu.successOk('#id_cliente', data, modalPersona);

				        	if (options.url == urlGuardarTipoServicio) compu.successOk('#id_tipo', data, modalTipoServicio);
			
				        	if (options.url == urlGuardarMarca) compu.successOk('#id_marca', data, modalMarca);			            
				        	
				        	if (options.url == urlGuardarComponente) compu.successOk('#id_componentes', data, modalComponente);			            
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
				if (selector == '#id_componentes') {
					var selectedItems = $(selector).select2("val");
					selectedItems.push(''+data.value+'');
					$(selector).select2("val", selectedItems);
				} else {
					select.val(''+data.value+'');	
        		    select.trigger('change');
        		}
								
        		modal.modal('hide');
			},
			


		};

		return compu;
	};

	var initApp = inicializar();
    initApp.initCompu();

	
    

});