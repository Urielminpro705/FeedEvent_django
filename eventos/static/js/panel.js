let currentEventIndex = 0;
let lastCurrentEventIndex = -1;

$(document).ready(function(){

    //#region //* Subir un evento

    $('#btnNewEvent').on('click',function(){
        showModal('\
            <form id="formEvent" class="cardForm"> \
                    <div class="basicColumn"> \
                        <h2>Añadir Nuevo Evento</h2>\
                        <input type="file" hidden id="impImage" name="imagen" required> \
                        <label id="lblImage" for="impImage"><i class="fa-solid fa-image"></i></label> \
                        <input type="text" id="titulo" name="titulo" class="imp" placeholder="Titulo"> \
                        <input type="text" id="desc" name="desc" class="imp" placeholder="Descripción"> \
                    </div>\
                    <div class="basicColumn"> \
                        <label for="" class="f08">Fecha del evento:</label> \
                        <input type="date" class="imp" name="cuando" id="cuando"> \
                        <input type="number" id="deport" name="deport" class="imp" placeholder="Deportivos"> \
                        <input type="number" id="cult" name="cult" class="imp" placeholder="Culturales"> \
                        <input type="number" id="solid" name="solid" class="imp" placeholder="Solidarios"> \
                            <div class="basicRow"> \
                                <button type="submit" class="basicBtn">Subir Actividad</button> \
                                <button type="button" class="basicBtn btnRemoveModal">Cancelar</button>\
                            </div> \
                    </div> \
            </form>')
    });

    // $('#modal').on('submit','#formEvent', function(e){
    //     e.preventDefault();
    //     let formData = new FormData(this);
    //     console.log(formData);
        
    //     $.ajax({ 
    //         url: 'PHP/Panel/uploadEvent.php',
    //         type: 'POST',
    //         data: formData,
    //         contentType: false,
    //         processData: false,
    //         success: function(res) {
    //             console.log(res);
    //             loadEventos(true);
    //             showModal('\
    //                 <h3>¡Se subío el evento con exito</h3>\
    //                 <button type="button" class="basicBtn btnRemoveModal">Ok</button>\
    //                 ');
    //         },
    //         error: function (jqXHR, textStatus, errorThrown) {
    //             console.log("Error en la solicitud AJAX:");
    //             console.log("Status: " + textStatus);
    //             console.log("Error lanzado: " + errorThrown);
    
    //             console.log(jqXHR.responseText);
    //             alert("Error en la conección");
    //         }
    //     })
    // });
    
    // $('#modal').on('change','#impImage',function(){
    //     let objetivo = $('#lblImage');
    //     const archivo = $(this).get(0).files[0];
    //     let vistaPrevia = objetivo;
    //     const texto = objetivo.find('.fa-solid');
    //     if (archivo) {
    //         const lector = new FileReader();
    //         lector.onload = function(event) {
    //             vistaPrevia.css('backgroundImage', 'url(' + event.target.result + ')');
    //             texto.hide();
    //         }
    //         lector.readAsDataURL(archivo);
    //     }
    // });

    function VistaPrevia(id, yo) {
        let objetivo = $('#img-option-'+id);
        const archivo = yo.get(0).files[0];
        let vistaPrevia = objetivo;
        const texto = objetivo.find('.fa-solid');
        if (archivo) {
            const lector = new FileReader();
            lector.onload = function(event) {
                vistaPrevia.css('backgroundImage', 'url(' + event.target.result + ')');
                texto.hide();
            }
            lector.readAsDataURL(archivo);
        } else {
            // No hay archivo seleccionado. Si quieres hacer algo en este caso, puedes agregar el código aquí.
        }
    }
    //#endregion
    //#region //* Cargar eventos
    // loadEventos();

    // function loadEventos(force = false){
    //     if(currentEventIndex == lastCurrentEventIndex && force == false){return;}
    //     $('#eventList').empty();
    //     $('#eventList').append('<div class="loading"></div>');
    //     switch (currentEventIndex) {
    //         case 0:
    //             $.get('PHP/Panel/importMyEvents.php',function(res){
    //                 $('#eventList').empty();
    //                 $('#eventList').append(res);
    //             })    
    //         break;
    //         case 1:
    //             $.get('PHP/Panel/importMyCurrentEvents.php',function(res){
    //                 $('#eventList').empty();
    //                 $('#eventList').append(res);
    //             })
    //         break;
    //         case 2:
    //             $.get('PHP/Panel/importMyLastEvents.php',function(res){
    //                 $('#eventList').empty();
    //                 $('#eventList').append(res);
    //             })
    //         break;
    //     }
    //     console.log("SE: ",currentEventIndex);
    //     lastCurrentEventIndex = currentEventIndex;
    // }

    //#endregion
    //#region //* Cambiar tipo de evento
    $('.optionsRow').on('click','.btnNoBg',function(){
        let type = $(this).text();
        let ancho = $(this).css('width');
        $('.optionsRow .btnNoBg').css('color','var(--placeholder)')
        $(this).css('color','var(--tag1)')
        switch (type) {
            case 'Todos':
                $('.optionsSel').css({
                    'left':'0%',
                    'transform':'translateX(0%)',
                    'width':ancho
                });
                currentEventIndex = 0;
            break;
            case 'Eventos Actuales':
                $('.optionsSel').css({
                    'left':'22%',
                    'transform':'translateX(0%)',
                    'width':ancho
                });
                currentEventIndex = 1;
            break;
            case 'Eventos Pasados':
                $('.optionsSel').css({
                    'left':'100%',
                    'transform':'translateX(-100%)',
                    'width':ancho
                });
                currentEventIndex = 2;
            break;
        }
        loadEventos();
    });
    //#endregion
    //#region //* Borrar Evento
    $('#eventList').on('click','.btnEventRemove',function(){
        let eventId = this.dataset.id;
        let titulo = $(this).prev().text();
        showModal('\
            <h3>Desea borrar el evento "'+titulo+'"?</h3>\
            <div class="basicRow">\
                <button class="basicBtn btnRemEvent" data-id="'+eventId+'">Aceptar</button>\
                <button class="basicBtn btnRemoveModal">Cancelar</button>\
            </div>\
        ');
    })

    $('#modal').on('click','.btnRemEvent',function(){
        let eventId = this.dataset.id;

        $.post('Php/Panel/removeEvent.php',{id: eventId},function(res){
            $('#modal h3').text(res);
            $('#modal .btnRemoveModal').text('Ok');
            loadEventos(true);
            $('#modal .btnRemEvent').hide();
        })
    })
    //#endregion

    function showModal(content){
        $('#contModal').fadeIn();
        $('#modal').addClass('animate__animated animate__fadeInRight');
        $('#modal').empty();
        $('#modal').append(content);
    }

    $('#modal').on('click','.btnRemoveModal',function(){
        $('#contModal').fadeOut(200);
    })
});