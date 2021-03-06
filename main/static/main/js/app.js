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
            formComponente   = modalComponente.find('form').html(),

            wd  = window || document;



        var compu = {

            initCompu: function() {
                
                this.setActionsFormServicio();  
                this.setActionsFormTipo();  
                this.setActionsFormComponente();                

                $('#servicio-btn').on('click',{modal:modalServicio}, this.showModal);

                $('#guardar-servicio-btn').on('click', this.guardarServicio);
                $('#edit-servicio-btn').on('click', {modal:modalServicio}, this.showModal);
                
                $('#guardar-persona-btn').on('click', this.guardarPersona);
                $('#guardar-tipo-servicio-btn').on('click', this.guardarTipoServicio);
                $('#guardar-marca-btn').on('click', this.guardarMarca);
                $('#guardar-componente-btn').on('click', this.guardarComponente);

                $('#update-btn').on('click', this.update);

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

                $('#id_plazo').datetimepicker({
                    language: 'es',
                    showMeridian: true, //muestra am y pm pero si se cambia el language no funciona, se arregla add ["AM", "PM"] en el archivo localizado
                    format: 'dd-mm-yyyy HH P',
                    startDate: new Date(),
                    autoclose: true,
                    daysOfWeekDisabled: [0],
                    minView: 1,
                    //maxView: 3,
                    todayHighlight: true,
                });
            },


                clearActionsFormServico: function() {
                    $('#cliente-btn, #tipo-btn, #marca-btn').off();
                    $('#id_cliente').select2("destroy");
                    $('#id_tipo').select2("destroy");
                    $('#id_marca').select2("destroy");
                    $('#id_componentes').select2("destroy");
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
                    return "<i class='fa fa-fw fa-"+state.id+"'></i> "+ state.text; //state.text;
                },
            
            
            showModal: function(event) {    
                event.preventDefault();
                if (event.data.reset) {   // si reset es true entonces reseteo el form y su id, por ahora no estoy usando esto
                    var form = event.data.modal.find('form');
                    compu.clearForm(form);
                };
                
                var selectedItems = $('#id_componentes').select2("val");
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
            

            /////////   PRINT METODOS  /////////


            update: function(event) {

                modalUpdate = $('#modal-update').modal({backdrop: 'static'});

                okBtn = modalUpdate.find('.ok-btn').one('click', function(){
                    
                    return wd.location.reload(true);
                });

                okBtn.button('loading');

                url = $(event.currentTarget).data('url')
                
                $.get(url)
                    .fail(function() {
                        alert( "error" );
                    })
                    .always(function(data){
                        var $content = modalUpdate.find('.content')
                        var $msg = $content.find('.msg');

                        if (!(data['success'])) { 
                            modalUpdate.find('.logo i').removeClass().addClass('fa fa-frown-o');
                            modalUpdate.find('.logo h5').text('imposible');
                            $msg.html(data.msg);
                            okBtn.button('reset'); 

                            setTimeout(function(){console.log('hola despues de 10 segundos')}, 10000);
                            console.log('hola soy despues del settimeout');
                            
                        } else {
                            modalUpdate.find('.logo i').removeClass().addClass('fa fa-smile-o');
                            modalUpdate.find('.logo h5').text('actualizado');   
                            $msg.html(data.msg);

                            setTimeout(function(){
                                okBtn.button('reset');
                                $msg.html('Servidor listo, Dale OK');
                            }, 30000);

                            var $progress = $content.find('.progress').removeClass('hidden').addClass('show');
                            var $bar = $content.find('.progress-bar');
                            var unidad = $bar.width();

                            var intervalo = setInterval(function(){
                                var width = $bar.width() + 3;
                                
                                $bar.width($bar.width() + unidad);
                                
                                if (okBtn.text() == "OK") {
                                    $progress.removeClass('active'); 
                                    $bar.width('100%');
                                    clearInterval(intervalo);   
                                }
                            },1000);
                        }
                    });
            },
            

            /////////   AJAX METODOS  /////////

            guardarServicio: function(event) {
                console.log($('#form-servicio').serialize());
                var $btn =  $(event.target).button('loading');

                compu.ajax({
                    url  : urlGuardarServicio,
                    form : '#form-servicio',
                    btn  : $btn
                });
            },



                fadeElement: function() {
                    $(document).bind('DOMNodeInserted', function(e) {
                        var element = e.target;
                        setTimeout(function() {
                            $(element).fadeOut(1000, function() {
                                $(this).remove();
                            });
                        }, 2000);
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
                            if (options.url == urlGuardarTipoServicio) compu.setActionsFormTipo(); 
                            if (options.url == urlGuardarComponente) compu.setActionsFormComponente();     
                        }
                        else {
                            if (options.url == urlGuardarServicio) return window.location.href= data.url;
                                
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



            ///////////////  UTILES  ////////////////

            clearForm: function(form) {
                console.log(form);
                form.find('*').each(function(index,element){
                    //console.log(Element.tagName.toLowerCase());
                    switch(element.tagName.toLowerCase()) {
                        case 'input':
                            if (element.name == 'csrfmiddlewaretoken') break;
                            else if ( $(element).hasClass('datetimeinput') ) {
                                element.value = "";
                                //$(element).datetimepicker('update');
                            }
                            else {
                                element.value = "";
                            }
                            break;
                        case 'textarea':
                            element.value = "";
                            //console.log(element.value);
                            break;
                        case 'select':
                            //console.log(element.options[element.selectedIndex].text);
                            //element.selectedIndex = 1;
                            $(element).select2("val", "");
                            break;


                    }

                });
                
              /*var elements = form.elements; 
                
              form.reset();

              for(i=0; i<elements.length; i++) {
                  
                field_type = elements[i].type.toLowerCase();
                
                switch(field_type) {
                
                    case "text": 
                    case "password": 
                    case "textarea":
                        case "hidden":  
                        
                        elements[i].value = ""; 
                        break;
                    
                    case "radio":
                    case "checkbox":
                        if (elements[i].checked) {
                            elements[i].checked = false; 
                        }
                        break;

                    case "select-one":
                    case "select-multi":
                                elements[i].selectedIndex = -1;
                        break;

                    default: 
                        break;
                }
                }*/
            }
            


        };

        return compu;
    };

    var initApp = inicializar();
    initApp.initCompu();

    
    

});