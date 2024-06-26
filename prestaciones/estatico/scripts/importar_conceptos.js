$gmx(document).ready(function () {
    $("#btnSubirArchivo").on("click", function () { subir_archivo(); });


    // Cerrar Mymodal
    $('#btnCierreModalImportar').on('click', function (e) {
        var comportamiento = $('#ModalImportar').attr('data-comportamiento');
        if (comportamiento === 'recargar') {
            // Recargar la página
            window.scrollTo(0, 0);
            window.location.reload();
        }
        if (comportamiento === 'modificarEmpleado') {
            // Recargar la página
            window.location.href = "/rh/gestion-empleados/modificar-empleado";
        }
        if (comportamiento === 'inicio') {
            // Recargar la página
            window.location.href = "/principal/sia";
        }
        if (comportamiento === 'cerrar_modales') {
            // cerrar todas las ventanas modales
            $('.modal').modal('hide');
        }

    });
});


function subir_archivo() {

    if (validarFormulario($("#frmConceptos")).valido) {
        // Aquí puedes añadir el código para manejar la subida del archivo.
        const fileInput = document.getElementById('ExtraeArchivo');
        const file = fileInput.files[0];

        // Crear un FormData object
        const formData = new FormData();
        formData.append('archivo', file);
        formData.append('idTipoConcepto', $('#Concepto option:selected').data('tipo'));
        formData.append('idConcepto', $('#Concepto').val());


        if (file) {
            $.ajax({
                async: false,
                type: "POST",
                url: "/prestaciones/extraer-concepto-de-archivo",
                data: formData,
                processData: false,
                contentType: false,
                success: function (resp) {

                    if (resp.Obtenido) {
                        var lista = false
                        var lista_guardados = false
                        var listaHTML = 'Los siguientes RFC no fueron encontrados. Favor de verificarlos manualmente:';
                        listaHTML += '<ul>';

                        resp.resultados.forEach(function (concepto) {
                            if (concepto.errorRFC) {
                                listaHTML += '<li>' + concepto.errorRFC + '</li>'
                                lista = true
                            }else{
                                lista_guardados = true
                            }
                        });
                        listaHTML += '</ul>'

                        listaHTML += '</tbody></table>';

                        var tablaHTML = '<table class="table table-striped">';
                        tablaHTML += '<thead><tr>' +
                            '<th>Nombre</th>' +
                            '<th>Apellidos</th>' +
                            '<th>RFC</th>' +
                            '<th>No. Contrato</th>' +
                            '<th>Monto</th>' +
                            '</tr></thead><tbody>';

                        resp.resultados.forEach(function (concepto) {
                            if (!concepto.errorRFC) {
                                tablaHTML += '<tr>' +
                                    '<td>' + concepto.Nombre + '</td>' +
                                    '<td>' + concepto.Apellidos + '</td>' +
                                    '<td>' + concepto.RFC + '</td>' +
                                    '<td>' + concepto.NumeroContrato + '</td>' +
                                    '<td>' + concepto.Monto + '</td>' +
                                    '</tr>';
                            }
                        });
                        tablaHTML += '</tbody></table>';
                        var mensaje = '';
                        if (lista == true) {
                            mensaje += listaHTML;
                        }
                        if (lista_guardados == true) {
                            mensaje += tablaHTML;
                        }else{
                            mensaje += "No se cargaron conceptos. ";
                        }
                        // Modificar el contenido del modal
                        document.getElementById('tituloModalImportar').textContent = "Información cargada";
                        document.getElementById('contenidoModalImportar').innerHTML = mensaje;
                        $('#ModalImportar').attr('data-comportamiento', "recargar");

                        // Abrir el modal
                        $('#ModalImportar').modal('show');

                    }

                    if (resp.ArchivoInvalido) {
                        abrirModal("Formato desconocido", "El archivo no tiene un formato válido.", "");
                    }
                    if (resp.ErrorLectura) {
                        abrirModal("Error de lectura", "El archivo no contiene la información o formato requerido", "");
                    }

                }


            })

        } else {
            abrirModal("Archivo no seleccionado", "Por favor seleccione un archivo.", "")
            console.log('No se seleccionó ningún archivo.');
            // Manejar el caso donde no se seleccionó archivo

        }
    }
}

