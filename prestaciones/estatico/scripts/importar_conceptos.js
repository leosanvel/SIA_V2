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

                        var tablaHTML = '<table class="table table-striped">';
                        tablaHTML += '<thead><tr>' +
                            '<th>Nombre</th>' +
                            '<th>Tipo Concepto</th>' +
                            '<th>idConcepto</th>' +
                            '<th>Concepto</th>' +
                            '<th>Porcentaje</th>' +
                            '<th>Monto</th>' 
                            '</tr></thead><tbody>';

                        resp.resultados.forEach(function (concepto) {
                            tablaHTML += '<tr>' +
                            '<td>' + concepto.Nombre + '</td>' +
                            '<td>' + concepto.idTipoConcepto + '</td>' +
                            '<td>' + concepto.idConcepto + '</td>' +
                            '<td>' + concepto.Concepto + '</td>' +
                            '<td>' + concepto.Porcentaje + '</td>' +
                            '<td>' + concepto.Monto + '</td>' 
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