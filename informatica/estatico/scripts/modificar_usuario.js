$(document).ready(function() {
    
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
            var isChecked = e.target.checked;
            var descendants = this.parentElement.querySelectorAll('input[type="checkbox"]');
            descendants.forEach(function (descendant) {
                descendant.checked = isChecked;
            });
        });
    });

    $("#btnBuscaUsuario").click(buscar_concepto);
});

function buscar_concepto() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/informatica/gestion-usuarios/buscar-usuario",
        data: $("#BuscarUsuario").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
            } else {
                $("#tablaResultadoUsuarios").show();
                $("#tablaResultadoUsuarios tbody").empty();
                var cont = 1;
                data.forEach(function (usuario) {
                    text = `
                    <tr>
                        
                        <td>
                            <input type="text" class="form-control" id="TipoConcepto" value="${usuario.Usuario}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto" value="${usuario.Contrasenia}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto" value="${usuario.PrimerIngreso}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Abreviatura" value="${usuario.idPersona}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Porcentaje" value="${usuario.Activo}" readonly></input>
                        </td>

                    </tr>
                    `;
                    cont++;
                    $("#tablaResultadoUsuarios tbody").append(text);
                });
            }
        }
    })

}