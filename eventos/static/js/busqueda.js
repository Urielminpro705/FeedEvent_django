$(document).ready(function() {
    let filter_btn = $(".filter-btn")
    let isOpenPanelFilter = false
    let filtros = ["", 0, 0, 0]
    let numeroFiltros = false

    function openAndClose() {
        if (isOpenPanelFilter) {
            filter_btn.removeClass("filter-btn-activated")
            setTimeout(function (){
                $(".cont-search-input").removeClass("cont-search-input-activated")
                $("#filter-btn-x-icon").css("display","none")
                $("#filter-btn-filter-icon").css("display","block")
            },200)
            $(".cont-filters").removeClass("cont-filters-activated")
            isOpenPanelFilter = false
            if ($(".filterTag").length != numeroFiltros) {
                busqueda()
            }
        } else {
            filter_btn.addClass("filter-btn-activated")
            $(".cont-search-input").addClass("cont-search-input-activated")
            $("#filter-btn-x-icon").css("display","block")
            $("#filter-btn-filter-icon").css("display","none")
            setTimeout(function (){
                $(".cont-filters").addClass("cont-filters-activated")
            },200)
            isOpenPanelFilter = true
            numeroFiltros = $(".filterTag").length
        }
    }

    function busqueda(){
        var texto = $("#search-input").val()
        var url = new URL("/eventos/busqueda/", window.location.origin)
        url.searchParams.append("titulo", texto)
        url.searchParams.append("deportivos", filtros[1])
        url.searchParams.append("solidarios", filtros[2])
        url.searchParams.append("culturales", filtros[3])
        window.location.href = url.toString()
    }

    function obtenerValoresUrl(){
        var urlParams = new URLSearchParams(window.location.search)
        filtros[0] = urlParams.get("titulo") || ""
        filtros[1] = urlParams.get("deportivos") === '1' ? 1 : 0;
        filtros[2] = urlParams.get("solidarios") === '1' ? 1 : 0;
        filtros[3] = urlParams.get("culturales") === '1' ? 1 : 0;
    }

    function activarFiltros(filtro){
        var txt = filtro.text()
        var id = filtro.data('id')
        filtros[id] = 1
        $('.cont-filters-on').append(`
            <div class="filter-card tag${id}" data-id="${id}"><p>${txt}</p>
                <button class="filter-x-btn">
                    <i class="fa-solid fa-x"></i>
                </button>
            </div>
        `);
        filtro.remove()
    }

    function recuperarFiltros(){
        obtenerValoresUrl()
        $(".filterTag").each(function(index, tag){
            var id = $(tag).data('id')
            if (filtros[id] == 1) {
                activarFiltros($(tag))
            }
        })
        $("#search-input").val(filtros[0])
    }

    recuperarFiltros()

    filter_btn.click(function() {
        openAndClose()
    })

    $(".filterTag").click(function () {
        activarFiltros($(this))
    })

    $(".filter-card").on("click",".filter-x-btn", function(){
        var card = $(this).closest(".filter-card"); 
        var id = card.data("id")
        var txt = card.text()
        $(".cont-filters-content").append(`
            <button class="filterTag bgTag${id}" data-id="${id}">${txt}</button>
        `)
        filtros[id] = 0
        card.remove()
        busqueda()
    })

    $("#searchEvents").click(function (){
        busqueda()
    })

    $("#search-input").on('keypress', function(event) {
        // Enter es 13
        if (event.keyCode === 13) {
            busqueda()
        }
    });
})