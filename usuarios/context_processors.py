from .models import Usuario

def global_vars(request):
    feed_id = request.session.get('feedID', 0)
    user = Usuario.objects.filter(id=feed_id).first()
    return {
        'feedID' : feed_id,
        'CURRENT_USER' : user
    }