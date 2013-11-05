// $(function() {
//   $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
// });

$( document ).ready( function(){

	// var item = $('.nav-servicios a[href^="' + location.pathname + '"]').addClass('active');
	// console.log(item);
	function inicializar() {

		formServicio = $('#modal-form-servicio');
		formPersona  = $('#modal-form-persona');

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
				//formServicio.on('hidden.bs.modal', this.alHideServicio);
				formPersona.on('hidden.bs.modal', this.alHidePersona);
			},


			alClickServicio: function() {
				formServicio.modal('show');
			},


			alClickCliente: function() {
				formServicio.modal('hide');
				formPersona.modal('show');
			},

			alHideServicio: function() {
				//formPersona.modal('show');
			},

			alHidePersona: function() {
				formServicio.modal('show');
			},		

		};

		return compu;
	};

	var initApp = inicializar();
    initApp.initCompu();

	
    

});