from flask import Blueprint, session
from flask_login import current_user

general = Blueprint('general', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/scripts')


@general.route('/general/cargar-menu', methods=['POST'])
def carga_menu():
    if current_user.is_authenticated and current_user.Activo == 1:
        return (generar_menu())
    else:
        return ("")

def generar_menu():
    menu_html = ''  # Inicializamos el string del menú

    # Diccionario para almacenar menús agrupados por nombre
    menus = {}
    # Recorre las páginas del usuario almacenadas en la sesión
    if 'paginas_usuario' in session:
        paginas_usuario = session['paginas_usuario']
        for pagina in paginas_usuario:
            menu = pagina['Menu']
            submenu = pagina['SubMenu']
            nombre = pagina['Pagina']
            url = pagina['URL']
            # Agrupa las páginas por menú
            if menu not in menus:
                menus[menu] = {}
            if submenu not in menus[menu]:
                menus[menu][submenu] = []
            menus[menu][submenu].append({'nombre': nombre, 'url': url})

    # Genera el HTML del menú agrupado por menús y submenús
    for menu, submenus in menus.items():
        menu_html += f'<li class="dropdown">'  # Abre el dropdown del menú
        menu_html += f'<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">{menu}<span class="caret"></span></a>'  # Genera el botón del menú
        menu_html += '<ul class="dropdown-menu" role="menu">'  # Abre la lista de opciones del menú

        # Recorre los submenús dentro del menú
        for submenu, paginas in submenus.items():
            menu_html += f'<li class="dropdown-header"><h6>{submenu}</h6></li>'  # Agrega el título del submenú
            for pagina in paginas:
                menu_html += f'<li><a href="{pagina["url"]}">{pagina["nombre"]}</a></li>'  # Agrega las páginas del submenú

        menu_html += '</ul></li>'  # Cierra la lista de opciones del menú
    return menu_html