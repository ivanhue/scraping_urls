from datetime import datetime
import os

# Fecha que sera utilizada para asignar nombres a los archivos creados durante la ejecución.
FECHA = datetime.today().strftime('%Y_%m_%d%H_%M_%S')

# Folder donde se guarda todos los registros (errores e información adicional, rendimiento).
FOLDER = "logs/"+FECHA+"/"
if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)
    
# Cadenas de texto obligatorias que SÍ debe tener.
OBLIGATORIOS = ['uam']

# Al menos uno de estas cadenas debe ser contenida en la página web extraida.
INCLUIDODS = [
    '.izt',
    'uami',
    'iztapalapa'
]

# Lista de cadenas que NO deben tener en las páginas web extraidas.
EXCLUIDOS = [
    'whatsapp',
    'facebook',
    'instagram',
    'twitter',
]

# 10_000 < MAX_CANTIDAD_TEXTO < 50_000
MAX_CANTIDAD_TEXTO = 50_000 # Máxima cantidad de texto que puede tener un documento.
# 100 < MIN_CANTIDAD_TEXTO < 500
MIN_CANTIDAD_TEXTO = 200    # Minima cantidad de texto que debe tener un documento.

# 5 < MAX-PAGES < 8_000
MAX_PAGES = 5 # Maxima cantida de páginas que van a ser visitadas.

# Paginas web que se van agregar la base de datos YA EXISTENTE.
NUEVAS_PAGINAS = [
    "https://cbi.izt.uam.mx/coddaa/index.php/fisica-pe",
    'https://cbi.izt.uam.mx/coddaa/index.php/compu-desc', 
    'https://cbi.izt.uam.mx/coddaa/index.php/fisica-da', 
    'https://cbi.izt.uam.mx/coddaa/index.php/descripcion', 
    'https://cbi.izt.uam.mx/coddaa/index.php/iq-desc', 
    'https://cbi.izt.uam.mx/coddaa/index.php/fisica-asp', 
    'https://www.cseuami.org/index.php/proceso', 
    'https://cbi.izt.uam.mx/coddaa/index.php/ceremonias/egresados-enero-2023', 
    'https://cbi.izt.uam.mx/coddaa/index.php/ih-desc', 
    'https://cbi.izt.uam.mx/coddaa/index.php/ceremonias/entrega-de-reconocimientos-al-alumnado-regular',
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/energia-y-medio-ambiente', 
    'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2023', 
    'https://cbi.izt.uam.mx/coddaa/index.php/fisica-pe#plan-de-estudios', 
    'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef', 
    'https://cbi.izt.uam.mx/coddaa/index.php/ceremonias', 
    'https://iquizayan.uam.mx:8443/sae/izt/aewbf001.omuestraframes?mod=1', 
    'https://cbi.izt.uam.mx/coddaa/index.php/vinculacion/movilidad-estudiantil', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/pquim', 
    'https://cbi.izt.uam.mx/coddaa/index.php/ie-desc', 
    'https://cbi.izt.uam.mx/coddaa/', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/pib', 
    'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2020', 
    'https://cbi.izt.uam.mx/coddaa/index.php/home/quienes-somos', 
    'https://cbi.izt.uam.mx/coddaa/index.php/fisica-mt', 
    'https://cbi.izt.uam.mx/coddaa/index.php/terminales-fisica', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/fisica', 
    'https://cbi.izt.uam.mx/coddaa/index.php/vinculacion/programa-de-vinculacion-profesional', 
    'https://cbi.izt.uam.mx/coddaa/index.php/alumnos/legislacion-universitaria', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/fisica-medica', 
    'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2021', 
    'http://www.izt.uam.mx/', 
    'https://cbi.izt.uam.mx/coddaa/index.php/home/directorio', 
    'https://cbi.izt.uam.mx/coddaa/index.php/ene-desc', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/ultimas-noticias', 
    'https://cbi.izt.uam.mx/coddaa/index.php/alumnos/tutorias', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/matematicas-aplicadas-e-industriales', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/matematicas', 
    'https://cbi.izt.uam.mx/coddaa/index.php/nuevo-ingreso', 
    'https://cbi.izt.uam.mx/coddaa/index.php/vinculacion/emprendimiento', 
    'https://cbi.izt.uam.mx/coddaa/index.php/eventos', 'https://cbi.izt.uam.mx/coddaa/index.php/fisica-pe', 'https://cbi.izt.uam.mx/coddaa/index.php/fisica-pe#mapa-curricular', 'https://cbi.izt.uam.mx/coddaa/index.php/programas-fisica', 'https://cbi.izt.uam.mx/coddaa/index.php', 'https://cbi.izt.uam.mx/coddaa/index.php/catm-desc', 'https://cbi.izt.uam.mx/coddaa/index.php/fisica-habilidades', 'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2022', 'https://cbi.izt.uam.mx/coddaa/index.php/quim-desc', 'https://cbi.izt.uam.mx/coddaa/index.php/mate-desc', 'https://cbi.izt.uam.mx/coddaa/index.php/fisica-desc', 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/ingenieria-quimica', 'http://ixtamati.uam.mx:8080/sae/izt/PAWBC005.oCONSULTA?CLAVE_CL=26&VERSION_CL=7', 'https://cbi.izt.uam.mx/coddaa/index.php/alumnos/tramites', 
    'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/ciencias-y-tecnologias-de-la-informacion'
]
# Paginas web que se van agregar a una nueva base de datos.
INICIAL_PAGES = [
    "https://www.celex.izt.uam.mx/instructivocelex.pdf",
    "https://www.celex.izt.uam.mx/celex/",
    "https://cbi.izt.uam.mx/coddaa/index.php/compu-pemc",
    # "http://www.iztapalapa.uam.mx/",
    # "http://www.izt.uam.mx/index.php/licenciaturas/",
    # "https://www.cseuami.org/",
    # "https://www.cseuami.org/index.php/cambio-carrera",
    # "http://www.izt.uam.mx/index.php/division-csh/",
    # "https://cbs.izt.uam.mx/",
    # "https://cbi.izt.uam.mx/",
    # "https://pcyti.izt.uam.mx/",
    # 'https://cbi.izt.uam.mx/coddaa/index.php/compu-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/descripcion', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/iq-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/images/guia-rec-pass.pdf', 
    # 'https://cbi.izt.uam.mx/coddaa/images/avisos/Lamina3.pdf', 
    # 'https://www.cseuami.org/index.php/proceso', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/ceremonias/egresados-enero-2023', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/ih-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/ceremonias/entrega-de-reconocimientos-al-alumnado-regular', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/energia-y-medio-ambiente', 
    # 'https://cbi.izt.uam.mx/coddaa/images/SitiosInteres/preguntas-frecuentes.pdf', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2023', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/ceremonias', 
    # 'https://iquizayan.uam.mx:8443/sae/izt/aewbf001.omuestraframes?mod=1', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/vinculacion/movilidad-estudiantil', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/pquim', 
    # 'https://cbi.izt.uam.mx/coddaa/images/avisos/cosib.pdf', 
    # 'https://cbi.izt.uam.mx/coddaa/images/UAM-calendario-escolar-2022-2023-y-2023-2024vf.pdf', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/ie-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/pib', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2020', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/home/quienes-somos', 
    # 'https://www.izt.uam.mx/index.php/acciones-contra-la-violencia-de-genero/', 
    # 'https://cbi.izt.uam.mx/consejo_divisional/', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/fisica', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/vinculacion/programa-de-vinculacion-profesional', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/alumnos/legislacion-universitaria', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/fisica-medica', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2021', 
    # 'https://cbi.izt.uam.mx/coddaa/images/avisos/La_UAM-I_y_su_compromiso_social.pdf', 
    # 'http://www.izt.uam.mx/', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/home/directorio', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/ene-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/ultimas-noticias', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/alumnos/tutorias', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/matematicas-aplicadas-e-industriales', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/matematicas', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/nuevo-ingreso', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/vinculacion/emprendimiento', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/eventos', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php#rt-head-anchor', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/catm-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/eventos/carlos-graef-2022', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/quim-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/mate-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/fisica-desc', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php?option=com_content&view=article&id=180', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/ingenieria-quimica', 
    # 'https://cbi.izt.uam.mx/coddaa/images/SitiosInteres/preguntas-becas-especie.pdf', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/alumnos/tramites', 
    # 'https://cbi.izt.uam.mx/coddaa/index.php/posgrado/ciencias-y-tecnologias-de-la-informacion',
    # 'https://www.cseuami.org/index.php/ingreso-posgrado', 
    # 'https://www.cseuami.org/index.php/calendario-de-procesos-escolares', 
    # 'http://www.cseuami.org/documentos/licenciatura/instructivos/ins_rei_pos_23p.pdf', 
    # 'http://www.cseuami.org/index.php?option=com_content&view=article&id=164', 
    # 'https://www.cseuami.org/index.php/tramites-escolares', 
    # 'https://www.cseuami.org/index.php/proceso', 
    # 'http://csh.izt.uam.mx/', 
    # 'https://www.cseuami.org/index.php', 
    # 'https://www.cseuami.org/index.php/legislacion/reglamentos', 
    # 'https://www.cseuami.org/index.php/tramite-de-grado-de-maestria', 
    # 'http://www.cseuami.org/index.php/proceso', 
    # 'https://cbs.izt.uam.mx/', 
    # 'https://www.cseuami.org/index.php/cal-esc', 
    # 'https://www.cseuami.org/index.php/home/presentacion', 
    # 'https://www.cseuami.org/index.php/home/ubicacion', 
    # 'http://ixtamati.uam.mx:8080/sae/izt/PAWBC004', 
    # 'https://www.cseuami.org/index.php/tramite-diploma-especializacion',
    # 'http://amoxcalli.izt.uam.mx/concurso_logo/', 
    # 'http://www.cseuami.org/index.php/programas-posgrado', 
    # 'https://www.cseuami.org/documentos/calendario_2022.pdf', 
    # 'http://www.cseuami.org/index.php?option=com_content&view=article&id=165', 
    # 'https://www.cseuami.org/index.php/home/directorio/dir-cbi', 
    # 'https://www.cseuami.org/index.php/credencial-uami', 
    # 'https://www.cseuami.org/index.php/legislacion/instructivos-de-servicios', 
    # 'https://www.cseuami.org/#rt-head-anchor', 
    # 'https://www.cseuami.org/documentos/licenciatura/instructivos/fechas_importantes.pdf', 
    # 'http://amoxcalli.izt.uam.mx/', 
    # 'http://www.celex.izt.uam.mx/celex/index.shtml', 
    # 'https://www.cseuami.org/index.php/programas-posgrado', 
    # 'https://www.cseuami.org/index.php/egreso', 
    # 'https://www.cseuami.org/index.php/tramites-escolares-posgrado', 
    # 'https://www.cseuami.org/index.php/tramite-grado-doctorado', 
    # 'http://www.cseuami.org/documentos/licenciatura/instructivos/ins_insc_pos_23p.pdf', 
    # 'http://www.izt.uam.mx/', 
    # 'https://www.cseuami.org/index.php/estadisticas-posgrado', 
    # 'https://www.cseuami.org/index.php/calendario-escolar', 
    # 'http://www.cseuami.org/index.php/programas', 
    # 'https://www.cseuami.org/index.php/home/directorio/dir-cse',
    # 'https://www.cseuami.org/index.php/titulacion/ccel', 
    # 'https://www.cseuami.org/index.php/home/preguntas', 
    # 'https://www.cseuami.org/index.php/programas', 
    # 'http://escolaresbot.izt.uam.mx/', 
    # 'https://www.cseuami.org/index.php/home/directorio/dir-cbs', 
    # 'https://www.cseuami.org/index.php/cursos-posgrado', 
    # 'https://www.cseuami.org/index.php/est-lic', 
    # 'https://www.cseuami.org/index.php/home/directorio/dir-csh', 
    # 'https://www.cseuami.org/index.php/optativas',
    # 'https://www.cseuami.org/index.php/legislacion/lineamientos', 
    # 'https://www.cseuami.org/documentos/licenciatura/instructivos/calendario_rec_rei_2.pdf'
]

# BASE_DE_DATOS = "path/base/datos" 
BASE_DE_DATOS = "data/textos_2023_07_3116_31_07.json" # Base  de datos a modificar.

