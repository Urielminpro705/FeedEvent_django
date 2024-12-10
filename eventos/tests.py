from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from usuarios.models import Usuario
from django.contrib.auth.models import User
from eventos.models import Evento
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model


class PruebasRegistroUsuario(TestCase):

    def setUp(self):
        # Datos iniciales para pruebas
        self.datos_validos = {
            'nombre': 'usuarioprueba',
            'correo': 'usuarioprueba@example.com',
            'password': 'contrasenaSegura123',
            'password2': 'contrasenaSegura123',
            'carrera': 'Ingeniería en Desarrollo de Software',
        }
        self.datos_invalidos = {
            'nombre': '',
            'correo': '',
            'password': '',
            'password2': '',
            'carrera': '',
        }

    def test_registro_usuario_exitoso(self):
        # Caso: Registro exitoso.
        # Verificamos que un usuario se registre correctamente con datos validos.

        respuesta = self.client.post(reverse('usuarios:register'), data=self.datos_validos)
        self.assertEqual(respuesta.status_code, 302)  # Redirección tras registro exitoso
        self.assertTrue(Usuario.objects.filter(correo='usuarioprueba@example.com').exists())

    def test_registro_usuario_fallido(self):
        # Caso: Registro fallido por datos invalidos.
        # Verifica que el registro falle por datos invalidos.

        respuesta = self.client.post(reverse('usuarios:register'), data=self.datos_invalidos)
        self.assertEqual(respuesta.status_code, 200) 
        self.assertContains(respuesta, 'El campo "Nombre" es obligatorio', html=True)
        self.assertEqual(Usuario.objects.count(), 0)  # Ningún usuario debe haber sido creado

class PruebasInicioSesionUsuario(TestCase):

    def setUp(self):
        # Crear un usuario para las pruebas
        self.datos_usuario = {
            'username': 'usuarioprueba', 
            'email': 'usuarioprueba@gmail.com',
            'password': 'contrasena123',
        }
        self.usuario = User.objects.create_user(
            username=self.datos_usuario['username'],
            email=self.datos_usuario['email'],
            password=self.datos_usuario['password']
        )
        self.url_inicio_sesion = reverse('usuarios:login')
        self.url_perfil = reverse('usuarios:profile')

    def test_inicio_sesion_exitoso(self):
        # Caso: Inicio de sesión exitoso.
        # Verificamos que un usuario registrado pueda iniciar sesion correctamente.

        respuesta = self.client.post(self.url_inicio_sesion, {
            'username': self.datos_usuario['username'],  # Nombre de usuario
            'password': self.datos_usuario['password'],
        })

        self.assertEqual(respuesta.status_code, 302)  # Redireccion tras inicio exitoso
        self.assertRedirects(respuesta, '/usuarios/?error=1')  

        # Realizamos el inicio de sesión 
        self.client.login(username=self.datos_usuario['username'], password=self.datos_usuario['password'])

        # Verificamos que el usuario se haya autenticado correctamente
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_inicio_sesion_fallido(self):
        # Caso: Fallo en inicio de sesion.
        # Verifica que un usuario no pueda iniciar sesión con datos incorrectoss.

        respuesta = self.client.post(self.url_inicio_sesion, {
            'username': self.datos_usuario['username'],  # Nombre de usuario
            'password': 'contrasenaIncorrecta',  # Contraseña incorrecta
        })
        self.assertEqual(respuesta.status_code, 302)  # Redireccion tras fallar
        self.assertRedirects(respuesta, '/usuarios/?error=1') 
        self.assertFalse('_auth_user_id' in self.client.session)  # El usuario no debe estar autenticado
        


class PruebasCreacionEventos(TestCase):

    def setUp(self):
        # Obtemos el usuario configurado en el proyecto
        User = get_user_model()

        # Creamos un superusuario para las pruebas
        self.usuario_admin = User.objects.create_superuser(
            username="adminprueba",
            email="adminprueba@example.com",
            password="adminpassword",
        )
        # Autenticamos al usuario
        self.client.login(username="adminprueba", password="adminpassword")

        self.url_crear_evento = reverse("eventos:agregarEvento")

        self.datos_validos_evento = {
            'titulo': "Evento de Prueba",
            'descr': "Descripción del evento de prueba",
            'cuando': "2024-12-31",
            'horaInicio': "10:00:00",
            'horaFin': "12:00:00",
            'solidarios': 5,
            'culturales': 3,
            'deportivos': 2,
            'requisitos': "Requisito de prueba",
            'fechaCreacion': timezone.now(),
            'Usuario': self.usuario_admin.id,
        }

        # Datos invalidoss'
        self.datos_invalidos_evento = {
            'titulo': "", 
            'descr': "Descripción del evento de prueba",
            'cuando': "2024-12-31",
            'horaInicio': "10:00:00",
            'horaFin': "12:00:00",
            'solidarios': -1,  
            'culturales': 3,
            'deportivos': 2,
            'requisitos': "Requisito de prueba",
            'fechaCreacion': timezone.now(),
            'Usuario': self.usuario_admin.id,
        }

def test_creacion_evento_fallido(self):
    # Caso: Creamos el evento fallido por datos invalidos.
    # Verificamos que el evento no se cree.

    # Verificamos que el usuario este autenticado
    self.assertTrue(self.client.session['_auth_user_id'])

    respuesta = self.client.post(self.url_crear_evento, data=self.datos_invalidos_evento)

    # Verificamos que la respuesta sea un error 200, ya que la página se recarga para mostrar los errores
    self.assertEqual(respuesta.status_code, 200)

    # Verificamos que el formulario ha mostrado un error en titulo
    self.assertContains(respuesta, 'Este campo es obligatorio.', html=True)

    # Verificamos que se ha mostrado un error para el cammpo de creditos solidarios
    self.assertContains(respuesta, 'Asegúrese de que este valor sea mayor o igual a 0.', html=True)

    # Verificamos que el evento no se haya creado en la base de datos
    self.assertEqual(Evento.objects.count(), 0)
    
    

    class PruebasFiltrosEventos(TestCase):

        def setUp(self):
            # Crear un usuario para asociar los eventos
            self.usuario = Usuario.objects.create(
                nombre="usuarioprueba", correo="usuario@example.com", password="password", carrera="Ingeniería"
            )

            # Crear eventos con diferentes categorías
            self.evento1 = Evento.objects.create(
                titulo="Evento Deportivo 1",
                descr="Descripción evento 1",
                requisitos="Requisitos 1",
                cuando="2024-12-15",
                solidarios=0,
                culturales=0,
                deportivos=10,
                fechaCreacion=timezone.now(),
                Usuario=self.usuario,
                horaInicio="10:00:00",
                horaFin="12:00:00",
            )
            self.evento2 = Evento.objects.create(
                titulo="Evento Cultural 1",
                descr="Descripción evento 2",
                requisitos="Requisitos 2",
                cuando="2024-12-16",
                solidarios=0,
                culturales=10,
                deportivos=0,
                fechaCreacion=timezone.now(),
                Usuario=self.usuario,
                horaInicio="12:00:00",
                horaFin="14:00:00",
            )
            self.evento3 = Evento.objects.create(
                titulo="Evento Solidario 1",
                descr="Descripción evento 3",
                requisitos="Requisitos 3",
                cuando="2024-12-17",
                solidarios=10,
                culturales=0,
                deportivos=0,
                fechaCreacion=timezone.now(),
                Usuario=self.usuario,
                horaInicio="14:00:00",
                horaFin="16:00:00",
            )
            
        def test_busqueda_filtro_exitoso(self):
            # Caso: Búsqueda y filtro exitoso, deben aparecer solo los eventos de la categoría "Deportivo".
            
            url = reverse('eventos:busqueda') + "?deportivos=5"  # Filtro para mostrar solo eventos deportivos
            
            # Realizar la solicitud con los filtros
            respuesta = self.client.get(url)
            
            # Verificamos que la respuesta sea exitosa
            self.assertEqual(respuesta.status_code, 200)
            
            # Verificamos que solo se muestre el evento deportivo
            self.assertContains(respuesta, "Evento Deportivo 1")
            self.assertNotContains(respuesta, "Evento Cultural 1")
            self.assertNotContains(respuesta, "Evento Solidario 1")
            
            # Verificar que la cantidad de eventos mostrados sea 1
            self.assertEqual(len(respuesta.context['eventos']), 1)
            
            
            
    class PruebasFiltrosEventos(TestCase):

        def setUp(self):
            # Crear un usuario para asociar los eventos
            self.usuario = Usuario.objects.create(
                nombre="usuarioprueba", correo="usuario@example.com", password="password", carrera="Ingeniería"
            )

            # Crear eventos con diferentes categorías
            self.evento1 = Evento.objects.create(
                titulo="Evento Deportivo 1",
                descr="Descripción evento 1",
                requisitos="Requisitos 1",
                cuando="2024-12-15",
                solidarios=0,
                culturales=0,
                deportivos=10,
                fechaCreacion=timezone.now(),
                Usuario=self.usuario,
                horaInicio="10:00:00",
                horaFin="12:00:00",
            )
            self.evento2 = Evento.objects.create(
                titulo="Evento Cultural 1",
                descr="Descripción evento 2",
                requisitos="Requisitos 2",
                cuando="2024-12-16",
                solidarios=0,
                culturales=10,
                deportivos=0,
                fechaCreacion=timezone.now(),
                Usuario=self.usuario,
                horaInicio="12:00:00",
                horaFin="14:00:00",
            )
            self.evento3 = Evento.objects.create(
                titulo="Evento Solidario 1",
                descr="Descripción evento 3",
                requisitos="Requisitos 3",
                cuando="2024-12-17",
                solidarios=10,
                culturales=0,
                deportivos=0,
                fechaCreacion=timezone.now(),
                Usuario=self.usuario,
                horaInicio="14:00:00",
                horaFin="16:00:00",
            )
            
        def test_busqueda_filtro_exitoso(self):
            # Caso: Busqueda y filtro exitoso
            
            url = reverse('eventos:busqueda') + "?deportivos=5"  # Filtro
            
            # Realizar la solicitud con los filtros
            respuesta = self.client.get(url)
            
            # Verificamos que la respuesta sea exitosa
            self.assertEqual(respuesta.status_code, 200)
            
            # Verificamos que solo se muestre el evento deportivo
            self.assertContains(respuesta, "Evento Deportivo 1")
            self.assertNotContains(respuesta, "Evento Cultural 1")
            self.assertNotContains(respuesta, "Evento Solidario 1")
            
            # Verificar que la cantidad de eventos mostrados sea 1
            self.assertEqual(len(respuesta.context['eventos']), 1)
            
            
        
        def test_busqueda_sin_resultados(self):
        # Caso: Filtros que no coinciden con ningun evento
        
            url = reverse('eventos:busqueda') + "?deportivos=100"  # Filtro para mostrar solo eventos con más de 100 creditos deportivos
            
            # Realizamos la solicitud con los filtros
            respuesta = self.client.get(url)
            
            # Verificamos que la respuesta sea exitosa
            self.assertEqual(respuesta.status_code, 200)
            
            # Verificamos que no se muestren eventos
            self.assertNotContains(respuesta, "Evento Deportivo 1")
            self.assertNotContains(respuesta, "Evento Cultural 1")
            self.assertNotContains(respuesta, "Evento Solidario 1")
            
            self.assertContains(respuesta, "No se encontraron eventos que coincidan con los criterios de bsqueda.")
            
            # Verificar que no haya eventos
            self.assertEqual(len(respuesta.context['eventos']), 0)
            