$gmx(document).ready(function () {
    $("#btnSubirArchivo").on("click", function () { subir_archivo(); });
});


function subir_archivo() {

    if (validarFormulario($("#frmConceptos")).valido) {
        // Aquí puedes añadir el código para manejar la subida del archivo.
        const fileInput = document.getElementById('ExtraeArchivo');
        const file = fileInput.files[0];


        console.log("$('#idTipoConcepto').val()");
        console.log($('#idTipoConcepto').val());
        // Crear un FormData object
        const formData = new FormData();
        formData.append('archivo', file);
        formData.append('idTipoConcepto', $('#idTipoConcepto').val());
        formData.append('idConcepto', $('#idConcepto').val());
        console.log("formData");
        console.log(formData);
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
                success: function (concepto) {

                    if (concepto.Obtenido) {
                        var nombres = ""
                        concepto.lista_nombres.forEach(function (nombre) {
                            console.log(nombre);
                            nombres += nombre;
                        });
                        abrirModal("Información cargada",nombres, "");

                    }

                    if (concepto.ArchivoInvalido) {
                        abrirModal("Formato desconocido", "El archivo no tiene un formato válido.", "");
                    }
                    if (concepto.ErrorLectura) {
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