$(document).ready(function() {
    let nav_btn = $("#navProfile")
    let cont_profile = $(".cont-menu-profile")
    let isNavOpen = false

    function switchNav() {
        if (isNavOpen){
            $("nav").removeClass("dark-nav")
            cont_profile.removeClass("navProfile-open")
            $('#logoFade').css('opacity','0')
            isNavOpen = false
        } else {
            let text = $('#navProfile').children().eq(2).text();
            if(text == "Iniciar Sesión"){window.location = "/usuarios/"; return}
            $("nav").addClass("dark-nav")
            cont_profile.addClass("navProfile-open")
            $('#logoFade').css('opacity','1')
            isNavOpen = true
        }
    }   

    nav_btn.click(function() {
        switchNav()
    })
})