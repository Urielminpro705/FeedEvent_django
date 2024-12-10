let currentEventIndex = 0;
let lastCurrentEventIndex = -1;
$(document).ready(function(){

    let tokenInput = $("input[name='csrfmiddlewaretoken']")
    const csrfToken = tokenInput.val();
    tokenInput.remove();
    let id_evento_editar = 0

    $('#btnNewEvent').on('click',function(){
        showModal(`
            <form id="formEvent" class="cardForm" enctype="multipart/form-data"> 
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}"> 
                <div class="basicColumn"> 
                    <h2>Añadir Nuevo Evento</h2>
                    <input type="file" hidden id="impImage" name="imagen"> 
                    <label id="lblImage" for="impImage"><i class="fa-solid fa-image"></i></label> 
                    <input type="text" id="titulo" name="titulo" class="imp" placeholder="Titulo", required> 
                    <textarea id="desc" name="desc" class="imp" placeholder="Descripción" required></textarea>
                </div>
                <div class="basicColumn"> 
                    <label for="" class="f08">Fecha del evento:</label> 
                    <input type="date" class="imp" name="cuando" id="cuando" required> 
                    <label for="horaInicio" class="f08">Hora de inicio:</label> 
                    <input type="time" class="imp" name="horaInicio" id="horaInicio" required> 
                    <label for="horaFin" class="f08">Hora de finalizacion:</label> 
                    <input type="time" class="imp" name="horaFin" id="horaFin" required> 
                    <textarea class="imp" name="requisitos" id="requisitos" placeholder="Requisitos"></textarea>
                    <input type="number" id="deport" name="deport" class="imp" placeholder="Deportivos" min="0" max="30"> 
                    <input type="number" id="cult" name="cult" class="imp" placeholder="Culturales" min="0" max="30"> 
                    <input type="number" id="solid" name="solid" class="imp" placeholder="Solidarios" min="0" max="30"> 
                        <div class="basicRow"> 
                            <button type="submit" class="basicBtn">Subir Actividad</button> 
                            <button type="button" class="basicBtn btnRemoveModal">Cancelar</button>
                        </div> 
                </div> 
            </form>`)
    });

    // Vista previa de la imagen
    $("#modal").on("change", "#impImage",function() {
        let objetivo = $('#lblImage');
        const file = $(this).get(0).files[0];
        const preview = objetivo;
        const texto = objetivo.find('.fa-solid');
        if(file){
            const lector = new FileReader();
            lector.onload = function(event) {
                preview.css('backgroundImage', 'url(' + event.target.result + ')');
                texto.hide();
            }
            lector.readAsDataURL(file);
        }
    })

    // Publicar evento sin recargar pagina
    $('#modal').on('submit','#formEvent', function(e){
        e.preventDefault();
        let formData = new FormData(this);
        console.log(formData);
        $.ajax({
            url: "/eventos/agregar/",
            method: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function(res) {
                console.log(res);
                showModal('\
                    <h3>¡Se subío el evento con exito</h3>\
                    <button type="button" class="basicBtn btnRemoveModal">Ok</button>\
                    ');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error en la solicitud AJAX:");
                console.log("Status: " + textStatus);
                console.log("Error lanzado: " + errorThrown);
    
                console.log(jqXHR.responseText);
                alert("Error en la conección");
            }
        });
    });

    //#endregion
    //#region //* Cargar eventos
    function loadEventos(){
        switch(currentEventIndex){
            case 0:
                $("#oldEventList").show()
                $("#pendingEventList").show()
                break;
            case 1:
                $("#oldEventList").hide()
                $("#pendingEventList").show()
                break;
            case 2:
                $("#oldEventList").show()
                $("#pendingEventList").hide()
                break;
        }
    }

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
        let eventoId = this.dataset.id;
        let titulo = $(this).prev().text();
        showModal(`
            <h3>Desea borrar el evento ${titulo}?</h3>
            <div class="basicRow">
                <a class="basicBtn" href="/eventos/eliminar/${eventoId}">Aceptar</a>
                <button class="basicBtn btnRemoveModal">Cancelar</button>
            </div>
        `);
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
        location.reload();
    })


    //#region //* Actualizar evento
    $(".btnEventEditar").on("click", function(){
        var imagen = $(this).data("imagen")
        imagen  = "/media/" + imagen
        var descr = $(this).data("descr")
        id_evento_editar = $(this).data("id")
        showModal(`
            <form id="formUpdate" class="cardForm" enctype="multipart/form-data"> 
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}"> 
                <div class="basicColumn"> 
                    <h2>Editar evento</h2>
                    <input type="file" hidden id="impImage" name="imagen"> 
                    <label id="lblImage" for="impImage" style="background-image: url(${imagen})"></label> 
                </div>
                <div class="basicColumn"> 
                    <textarea id="desc" name="desc" class="imp" placeholder="Descripción" required>${descr}</textarea>
                    <div class="basicRow"> 
                        <button type="submit" class="basicBtn">Actualizar actividad</button> 
                        <button type="button" class="basicBtn btnRemoveModal">Cancelar</button>
                    </div> 
                </div>
            </form>
        `)
    })

    $('#modal').on('submit','#formUpdate', function(e){
        e.preventDefault();
        let formData = new FormData(this);
        console.log(formData);
        $.ajax({
            url: "/eventos/editar/" + id_evento_editar,
            method: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function(res) {
                console.log(res);
                showModal('\
                    <h3>¡Se editó el evento con exito</h3>\
                    <button type="button" class="basicBtn btnRemoveModal">Ok</button>\
                    ');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error en la solicitud AJAX:");
                console.log("Status: " + textStatus);
                console.log("Error lanzado: " + errorThrown);
    
                console.log(jqXHR.responseText);
                alert("Error en la conección");
            }
        });
    });

    //#endregion
});