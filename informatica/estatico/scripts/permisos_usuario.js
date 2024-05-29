$(document).ready(function () {

    cargar_paginas_arbol();

});

function cargar_paginas_arbol() {
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
                    var menuId = pagina.idMenu;
                    var menuName = pagina.Menu;
                    var submenuId = pagina.idSubMenu;
                    var submenuName = pagina.SubMenu;
                    var paginaId = pagina.idPagina;
                    var paginaName = pagina.Pagina;

                    if (!menuTree[menuId]) {
                        menuTree[menuId] = {
                            id: menuId,
                            name: menuName,
                            submenus: {}
                        };
                    }

                    if (!menuTree[menuId].submenus[submenuId]) {
                        menuTree[menuId].submenus[submenuId] = {
                            id: submenuId,
                            name: submenuName,
                            pages: []
                        };
                    }

                    menuTree[menuId].submenus[submenuId].pages.push({
                        id: paginaId,
                        name: paginaName
                    });
                });


                var menuContainer = $('#menu-container');
                menuContainer.empty();
                generarArbolCheck(menuContainer, menuTree);
            }
        }
    })
}

function generarArbolCheck(parentElement, menuItems, parentId = '', level = 0) {
    var ul = $('<ul>');
    $.each(menuItems, function (menuId, menu) {
        var menuElementId = parentId + 'menu-' + menuId;

        var li = $('<li>', { class: 'folder' });
        var checkbox = $('<input>', { type: 'checkbox', id: menuElementId });
        var label = $('<label>', { for: menuElementId, text: menu.name });
        var hiddenInput = $('<input>', { type: 'hidden', value: menu.id, class: 'menu-id' });
        li.append(checkbox, label, hiddenInput);

        var submenus = menu.submenus;
        var hasSubmenus = typeof submenus === 'object' && !Array.isArray(submenus);
        if (hasSubmenus) {
            li.append(generarSubMenu(submenus, menuElementId, level + 1));
        }

        ul.append(li);
    });

    parentElement.append(ul);

    var folders = document.querySelectorAll('.folder');
    folders.forEach(function (folder) {
        folder.addEventListener('click', function (event) {
            if (!event.target.matches('li')) return;
            var checkbox = this.querySelector('input[type="checkbox"]');
            var isOpen = this.classList.toggle('expanded');
            event.stopPropagation();
        });
    });

    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('click', function (e) {
            el = $(this);
            var isChecked = el.data('checked');

            if (isChecked === undefined) {
                isChecked = 1;
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

            updateParentCheckboxes(this);


        });
    });

    //Deshabilitar checkboxes para el LABEL
    $("#checkbox1").prop('checked', true)
    $("#checkbox1").on("click", function (event) { event.preventDefault(); });
    $("#checkbox2").prop('indeterminate', true)
    $("#checkbox2").on("click", function (event) { event.preventDefault(); });
    $("#checkbox3").prop('checked', false)
    $("#checkbox3").on("click", function (event) { event.preventDefault(); });

    return parentElement;
}

function generarSubMenu(submenus, parentId, level) {
    var ul = $('<ul>');
    $.each(submenus, function (submenuId, submenu) {
        var submenuElementId = parentId + '-submenu-' + submenuId;
        if (submenu.name.trim() !== '') {
            var li = $('<li>', { class: 'folder' });
            var checkbox = $('<input>', { type: 'checkbox', id: submenuElementId });
            var label = $('<label>', { for: submenuElementId, text: submenu.name });
            var hiddenInput = $('<input>', { type: 'hidden', value: submenu.id, class: 'submenu-id' });
            li.append(checkbox, label, hiddenInput);
        } else {
            var li = $('<li>');
        }
        var pages = submenu.pages;
        var subUl = $('<ul>');
        pages.forEach(function (page) {
            var pageElementId = submenuElementId + '-page-' + page.id;
            var pageLi = $('<li>');
            var pageCheckbox = $('<input>', { type: 'checkbox', id: pageElementId });
            var pageLabel = $('<label>', { for: pageElementId, text: page.name });
            var pageHiddenInput = $('<input>', { type: 'hidden', value: page.id, class: 'page-id' });

            pageLi.append(pageCheckbox, pageLabel, pageHiddenInput);
            subUl.append(pageLi);
        });

        li.append(subUl);
        ul.append(li);
    });

    return ul;
}

function leerEstadosCheckbox() {
    var states = [];

    $('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var li = checkbox.closest('li');
        var state = {
            idMenu: li.parents('ul').prev('input.menu-id').val(),
            idSubMenu: li.parents('ul').prev('input.submenu-id').val(),
            idPagina: li.find('input.page-id').val(),
            estado: checkbox.prop('indeterminate') ? 'lectura' : (checkbox.prop('checked') ? 'escritura' : 'inactiva')
        };

        // solo guarda cuando hay ID y haya sido seleccionado (menu, submenu, or page)
        if (state.estado != 'inactiva') {
            if (state.idMenu && state.idSubMenu && state.idPagina) {
                states.push(state);
            }
        }
    });

    return states;
}

function actualizarEstadoCheckboxes(consecutivo) {
    var nombre_usuario = $("#Usuario" + consecutivo).val();
    $.ajax({
        type: "POST",
        data: { nombre_usuario: nombre_usuario },
        url: "/informatica/gestion-usuarios/carga-paginas-usuario",
        success: function (lista_paginas) {

            if (lista_paginas.error) {
                abrirModal("Error", "Error", "")
            }
            else {
                lista_paginas.forEach(function (pagina) {
                    var idMenu = pagina.idMenu;
                    var idSubMenu = pagina.idSubMenu;
                    var idPagina = pagina.idPagina;
                    var estadoPagina = pagina.estado;

                    var checkboxId = `menu-${idMenu}-submenu-${idSubMenu}-page-${idPagina}`;

                    if ($(`#${checkboxId}`).length) {
                        console.log("----");
                        if (estadoPagina === 1) {
                            $(`#${checkboxId}`).prop('indeterminate', false);
                            $(`#${checkboxId}`).prop('checked', true);
                        } else if (estadoPagina === 0) {
                            $(`#${checkboxId}`).prop('checked', false);
                            $(`#${checkboxId}`).prop('indeterminate', true);
                        } else {
                            $(`#${checkboxId}`).prop('checked', false);
                            $(`#${checkboxId}`).prop('indeterminate', false);
                        }
                        updateParentCheckboxes($(`#${checkboxId}`));
                    }
                });
            }
        }
    })
}

function updateParentCheckboxes(childCheckbox) {
    var parentCheckbox = $(childCheckbox).closest('li').parents('li').children('input[type="checkbox"]');

    parentCheckbox.each(function() {
        var parent = $(this);
        var allSiblings = parent.closest('li').find('ul > li > input[type="checkbox"]');
        var allChecked = true;
        var allUnchecked = true;
        var anyIndeterminate = false;

        allSiblings.each(function () {
            if (this.checked) {
                allUnchecked = false;
            } else {
                allChecked = false;
            }
            if (this.indeterminate) {
                anyIndeterminate = true;
            }
        });

        if (allChecked) {
            parent.prop('checked', true);
            parent.prop('indeterminate', false);
            parent.data('checked', 2);
        } else if (allUnchecked && !anyIndeterminate) {
            parent.prop('checked', false);
            parent.prop('indeterminate', false);
            parent.data('checked', 0);
        } else {
            parent.prop('checked', false);
            parent.prop('indeterminate', true);
            parent.data('checked', 1);
        }

        // Propagar el cambio a niveles superiores
        updateParentCheckboxes(parent);
    });
}