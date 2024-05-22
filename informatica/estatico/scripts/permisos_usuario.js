$(document).ready(function () {

    cargar_arbol_paginas();

    var folders = document.querySelectorAll('.folder');
    folders.forEach(function (folder) {
        folder.addEventListener('click', function (event) {

            if (!event.target.matches('li')) return; // Si el clic no fue en un label, no hacer nada
            var checkbox = this.querySelector('input[type="checkbox"]');
            var isOpen = this.classList.toggle('expanded');
            event.stopPropagation(); // Detener la propagación del evento
        });
    });

    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('click', function (e) {

            el = $(this);
            var isChecked = el.data('checked');

            if (isChecked === undefined) {
                var isChecked = 1;
            }
            switch (isChecked) {
                case 0:
                    el.data('checked', 1);
                    el.prop('checked', false);
                    el.prop('indeterminate', true);

                    break;

                case 1:
                    el.data('checked', 2);
                    el.prop('checked', true);
                    el.prop('indeterminate', false);


                    break;

                default:
                    el.data('checked', 0);
                    el.prop('checked', false);
                    el.prop('indeterminate', false);


            }


            var descendants = this.parentElement.querySelectorAll('input[type="checkbox"]');

            descendants.forEach(function (descendant) {
                descendant.dataset.checked = el.data('checked');

                switch (isChecked) {

                    case 0:
                        descendant.checked = false;
                        descendant.indeterminate = false;

                        break;

                    case 1:
                        descendant.checked = false;
                        descendant.indeterminate = true;

                        break;

                    default:
                        descendant.checked = true;
                        descendant.indeterminate = false;
                }

            });

        });
    });

    $("#checkbox1").prop('checked',true)
    $("#checkbox1").on("click", function (event) {event.preventDefault(); });
    $("#checkbox2").prop('indeterminate',true)
    $("#checkbox2").on("click", function (event) { event.preventDefault(); });
    $("#checkbox3").prop('checked',false)
    $("#checkbox3").on("click", function (event) { event.preventDefault(); });
});

function cargar_arbol_paginas() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/informatica/gestion-usuarios/carga-arbol-paginas",
        success: function (paginas_usuario) {
            if (paginas_usuario.Error) {
                abrirModal("Error", "Ocurrión un problema. Lo sentimos.", "")
            } else {
                // Objeto para almacenar las páginas agrupadas por menú y submenú
                var menuTree = {};

                // Agrupar páginas por menú y submenú
                paginas_usuario.forEach(function (pagina) {

                    var menu = pagina.Menu;
                    var submenu = pagina.SubMenu;

                    if (!menuTree[menu]) {
                        menuTree[menu] = {};
                    }

                    if (!menuTree[menu][submenu]) {
                        menuTree[menu][submenu] = [];
                    }

                    menuTree[menu][submenu].push(pagina.Pagina);
                });

                // Generar el árbol de menú
                var menuContainer = $('#menu-container');
                menuContainer.empty();
                generateMenu(menuContainer, menuTree);
            }
        }
    })

}
function generateMenu(parentElement, menuItems, parentId = '', level = 0) {
    var ul = $('<ul>');
    $.each(menuItems, function (menu, submenus) {
        var menuId = parentId + 'menu-' + menu;
        console.log("menuId");
        console.log("-"+menu+"-");
        
        if(menu.trim() !== ''){
            // var li = $('<li>', { class: 'folder' + (level === 0 ? ' expanded' : '') });
            // var li = $('<li>', { class: 'folder' + ' expanded' });
            var li = $('<li>', { class: 'folder'});
            var checkbox = $('<input>', { type: 'checkbox', id: menuId });
            var label = $('<label>', { for: menuId, text: menu });
            li.append(checkbox, label);
        }else{
            var li = $('<li>');
        }


        var hasSubmenus = typeof submenus === 'object' && !Array.isArray(submenus);
        if (hasSubmenus) {
            var subMenuNames = Object.keys(submenus);

            if ( subMenuNames[0].trim() !== '') {
            }else{
            }
            li.append(generateMenu($('<ul>'), submenus, menuId + '-', level + 1));
        } else if (Array.isArray(submenus)) {
            var subUl = $('<ul>');
            submenus.forEach(function (page, index) {
                
                var pageId = menuId + '-' + index;
                var pageLi = $('<li>');
                var pageCheckbox = $('<input>', { type: 'checkbox', id: pageId });
                var pageLabel = $('<label>', { for: pageId, text: page });

                pageLi.append(pageCheckbox, pageLabel);
                subUl.append(pageLi);
            });

           
            li.append(subUl);

        }

        ul.append(li);
    });

    parentElement.append(ul);
    return parentElement;
}