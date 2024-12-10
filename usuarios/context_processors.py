from .models import Usuario

def global_vars(request):
    feed_id = request.session.get('feedID', 0)
    if (feed_id == None):
        user = Usuario()
        user.nombre = "Iniciar Sesión"
    else:
        user = Usuario.objects.filter(id=feed_id).first()

    return {
        'feedID' : feed_id,
        'CURRENT_USER' : user
    }