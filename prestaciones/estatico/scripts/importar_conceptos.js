$gmx(document).ready(function () {
    $("#btnSubirArchivo").on("click", function () { subir_archivo(); });
});


function subir_archivo() {

    if (validarFormulario($("#frmConceptos")).valido) {
        // Aquí puedes añadir el código para manejar la subida del archivo.
        const fileInput = document.getElementById('ExtraeArchivo');
        const file = fileInput.files[0];

        // Crear un FormData object
        const formData = new FormData();
        formData.append('archivo', file);
        formData.append('idTipoConcepto', $('#idTipoConcepto').val());
        formData.append('idConcepto', $('#idConcepto').val());

        if (file) {
            // Procesar el archivo (por ejemplo, enviarlo a un servidor)
            console.log(`Subiendo archivo ${file.name} con id de botón SubirArchivo`);

            $.ajax({
                async: false,
                type: "POST",
                url: "/prestaciones/extraer-concepto-de-archivo",
                data: formData,
                processData: false,
                contentType: false,
                success: function (resp) {

                    if (resp.Obtenido) {

                        var tablaHTML = '<table class="table table-striped">';
                        tablaHTML += '<thead><tr>' +
                            '<th>Ramo</th>' +
                            '<th>PAGSUBPAG</th>' +
                            '<th>Numero ISSSTE</th>' +
                            '<th>RFC</th>' +
                            '<th>Nombre</th>' +
                            '<th>Clave Cobro</th>' +
                            '<th>TPOD</th>' +
                            '<th>Pzo Qna</th>' +
                            '<th>Periodo 1</th>' +
                            '<th>Periodo 2</th>' +
                            '<th>Concepto</th>' +
                            '<th>Importe</th>' +
                            '<th>Numero Prestamo</th>' +
                            '</tr></thead><tbody>';

                        resp.lista_empleados.forEach(function (empleado) {
                            tablaHTML += '<tr>' +
                            '<td>' + empleado.Ramo + '</td>' +
                            '<td>' + empleado.PAGSUBPAG + '</td>' +
                            '<td>' + empleado.NumeroISSSTE + '</td>' +
                            '<td>' + empleado.RFC + '</td>' +
                            '<td>' + empleado.Nombre + '</td>' +
                            '<td>' + empleado.ClaveCobro + '</td>' +
                            '<td>' + empleado.TPOD + '</td>' +
                            '<td>' + empleado.PzoQna + '</td>' +
                            '<td>' + empleado.Periodo1 + '</td>' +
                            '<td>' + empleado.Periodo2 + '</td>' +
                            '<td>' + empleado.Concepto + '</td>' +
                            '<td>' + empleado.Importe + '</td>' +
                            '<td>' + empleado.NumeroPrestamo + '</td>' +
                            '</tr>';
                        });
                        tablaHTML += '</tbody></table>';
                        abrirModal("Información cargada", tablaHTML, "");

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