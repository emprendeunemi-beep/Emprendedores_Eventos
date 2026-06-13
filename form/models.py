from django.db import models


class VinculacionChoices(models.TextChoices):
    ESTUDIANTE = 'estudiante', 'Estudiante de UNEMI'
    RETIRADO = 'retirado', 'Retirado UNEMI'
    GRADUADO = 'graduado', 'Graduado(a) de UNEMI'
    DOCENTE = 'docente', 'Docente de UNEMI'
    ADMINISTRATIVO = 'administrativo', 'Personal administrativo de UNEMI'
    EXTERNO = 'externo', 'Externo'
    OTRO = 'otro', 'Otro'


class SexoChoices(models.TextChoices):
    MASCULINO = 'masculino', 'Masculino'
    FEMENINO = 'femenino', 'Femenino'
    NO_RESPONDE = 'no_responde', 'Prefiero no responder'


class CategoriaEmprendimientoChoices(models.TextChoices):
    GASTRONOMIA = 'gastronomia', 'Gastronomía'
    COMERCIO = 'comercio', 'Comercio'
    SERVICIOS = 'servicios', 'Servicios'
    TECNOLOGIA = 'tecnologia', 'Tecnología'
    ARTESANIAS = 'artesanias', 'Artesanías'
    AGRICULTURA = 'agricultura', 'Agricultura'
    BELLEZA = 'belleza', 'Belleza y bienestar'
    EDUCACION = 'educacion', 'Educación'
    TEXTIL = 'textil', 'Textil y confección'
    TURISMO = 'turismo', 'Turismo'
    OTRO = 'otro', 'Otro'


class TiempoFuncionamientoChoices(models.TextChoices):
    IDEA = 'idea', 'Idea de negocio'
    MENOS_6M = 'menos_6m', 'Menos de 6 meses'
    DE_6M_1A = '6m_1a', 'De 6 meses a 1 año'
    DE_1A_3A = '1a_3a', 'De 1 a 3 años'
    MAS_3A = 'mas_3a', 'Más de 3 años'


class NumeroColaboradoresChoices(models.TextChoices):
    NINGUNO = 'ninguno', 'Ninguno (Solo yo)'
    UNO_DOS = '1_2', '1 a 2 personas'
    TRES_CINCO = '3_5', '3 a 5 personas'
    SEIS_NUEVE = '6_9', '6 a 9 personas'
    MAS_DIEZ = 'mas_10', 'Más de 10 personas'


class PermisosChoices(models.TextChoices):
    SI = 'si', 'Sí'
    NO = 'no', 'No'
    EN_TRAMITE = 'en_tramite', 'En trámite'


class CapacitacionChoices(models.TextChoices):
    MARKETING = 'marketing', 'Marketing digital'
    VENTAS = 'ventas', 'Ventas'
    FINANZAS = 'finanzas', 'Finanzas para emprendedores'
    COSTOS = 'costos', 'Costos y fijación de precios'
    IA = 'ia', 'Inteligencia artificial aplicada a negocios'
    ATENCION_CLIENTE = 'atencion_cliente', 'Atención al cliente'
    ECOMMERCE = 'ecommerce', 'Comercio electrónico'
    BRANDING = 'branding', 'Branding'
    MODELOS_NEGOCIO = 'modelos_negocio', 'Modelos de negocio'
    FOTOGRAFIA = 'fotografia', 'Fotografía para productos'
    OTRO = 'otro', 'Otro'


class RegistroEmprendedor(models.Model):
    # ── Sección 1: Información general ──────────────────────────────────────
    cedula = models.CharField(max_length=20, unique=True, verbose_name='Número de cédula o documento de identidad')
    nombres_apellidos = models.CharField(max_length=200, verbose_name='Nombres y apellidos completos')
    edad = models.PositiveSmallIntegerField(verbose_name='Edad')
    sexo = models.CharField(max_length=20, choices=SexoChoices.choices, verbose_name='Sexo')
    whatsapp = models.CharField(max_length=20, verbose_name='Número de WhatsApp')

    # ── Sección 2: Vinculación con UNEMI ─────────────────────────────────────
    vinculacion = models.CharField(
        max_length=20,
        choices=VinculacionChoices.choices,
        verbose_name='Vínculo con UNEMI',
    )
    correo_institucional = models.EmailField(
        blank=True, null=True,
        verbose_name='Correo institucional UNEMI',
        help_text='Requerido para estudiantes, docentes y personal administrativo',
    )
    correo_personal = models.EmailField(
        blank=True, null=True,
        verbose_name='Correo electrónico personal',
    )
    carrera_actual = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name='Carrera que cursa actualmente',
        help_text='Solo para estudiantes',
    )
    semestre_actual = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name='Semestre actual',
        help_text='Solo para estudiantes',
    )
    carrera_graduado = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name='Carrera de la que se graduó',
        help_text='Solo para graduados',
    )

    # ── Sección 3: Ubicación ─────────────────────────────────────────────────
    provincia = models.CharField(max_length=100, verbose_name='Provincia de residencia')
    canton = models.CharField(max_length=100, verbose_name='Cantón o ciudad de residencia')

    # ── Sección 4: Información del emprendimiento ────────────────────────────
    nombre_emprendimiento = models.CharField(max_length=200, verbose_name='Nombre del emprendimiento o negocio')
    descripcion_productos = models.TextField(verbose_name='Descripción de productos o servicio principal')
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaEmprendimientoChoices.choices,
        verbose_name='Categoría principal del emprendimiento',
    )
    categoria_otro = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name='Especifique la categoría (si eligió Otro)',
    )
    tiempo_funcionamiento = models.CharField(
        max_length=20,
        choices=TiempoFuncionamientoChoices.choices,
        verbose_name='Tiempo de funcionamiento del emprendimiento',
    )
    numero_colaboradores = models.CharField(
        max_length=10,
        choices=NumeroColaboradoresChoices.choices,
        verbose_name='Número de colaboradores o empleados',
    )
    direccion = models.CharField(max_length=300, verbose_name='Dirección del emprendimiento')
    redes_sociales = models.TextField(verbose_name='Redes sociales del emprendimiento')

    # ── Sección 5: Formalización ─────────────────────────────────────────────
    tiene_ruc = models.BooleanField(verbose_name='¿Cuenta con RUC o RIMPE?')
    numero_ruc = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name='Número de RUC o RIMPE',
    )
    archivo_ruc = models.FileField(
        upload_to='ruc/', blank=True, null=True,
        verbose_name='RUC o RIMPE adjunto',
    )
    permisos_funcionamiento = models.CharField(
        max_length=20,
        choices=PermisosChoices.choices,
        verbose_name='¿Cuenta con permisos de funcionamiento?',
    )
    archivo_permiso = models.FileField(
        upload_to='permisos/', blank=True, null=True,
        verbose_name='Permiso de funcionamiento adjunto',
    )

    # ── Sección 6: Intereses de capacitación ────────────────────────────────
    # Almacenamos como JSON array (Django 3.1+)
    capacitacion_intereses = models.JSONField(
        default=list,
        verbose_name='Temas de capacitación de interés',
        help_text='Lista con uno o más valores de CapacitacionChoices',
    )
    capacitacion_otro = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name='Otro tema de capacitación (detallar)',
    )

    # ── Sección 7: Información complementaria ───────────────────────────────
    participo_anteriormente = models.BooleanField(
        null=True,
        verbose_name='¿Ha participado en actividades de la Gestión de Emprendimiento UNEMI?',
    )
    comentarios = models.TextField(
        blank=True, null=True,
        verbose_name='Comentarios, sugerencias o expectativas',
    )

    # ── Metadatos ────────────────────────────────────────────────────────────
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Registro de Emprendedor'
        verbose_name_plural = 'Registros de Emprendedores'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.nombres_apellidos} — {self.nombre_emprendimiento}'