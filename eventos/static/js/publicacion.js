$(document).ready(function(){
    let tokenInput = $("input[name='csrfmiddlewaretoken']")
    const csrfToken = tokenInput.val();
    tokenInput.remove();

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

    $("#btn-registro").on("click", function (){
        showModal(`
            <h3>¿Desea registrarse al evento?</h3>
            <div class="basicRow">
                <button class="basicBtn" id="btn-confirmar-registro">Registrarse</button>
                <button class="basicBtn btnRemoveModal">Cancelar</button>
            </div>
        `);
    })

    $("#modal").on("click","#btn-confirmar-registro", function (){
        id_usuario = $("#btn-registro").data("id")
        console.log(csrfToken)
        $.ajax({
            url: "/registros/registro/" + id_usuario,
            method: "POST",
            data: {
                "id_usuario": id_usuario,
                "csrfmiddlewaretoken": csrfToken
            },
            success: function(res) {
                console.log(res)
                location.reload();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error en la solicitud AJAX:");
                console.log("Status: " + textStatus);
                console.log("Error lanzado: " + errorThrown);
    
                console.log(jqXHR.responseText);
                alert("Error en la conección");
                location.reload();
            }
        })
    })
})