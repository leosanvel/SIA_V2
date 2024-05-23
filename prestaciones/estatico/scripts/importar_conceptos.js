$gmx(document).ready(function () {


    cargar_conceptos_extraeArchivo();

});

function cargar_conceptos_extraeArchivo() {

    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/filtrar-conceptos-extrae-archivo",
        // data: $("#frmBuscarConceptoEmpleado, #idPersona").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
                $("#tablaResultadosConceptos tbody").empty();
                $("#tablaResultadosConceptos").hide();
            } else {
                $("#tablaResultadosConceptos").show();
                $("#tablaResultadosConceptos tbody").empty();
                var cont = 1;
                data.forEach(function (concepto) {
                    text = `
                    <tr>
                        <td>
                            <input type="text" class="form-control" id="idTipoConcepto${cont}" value="${concepto.idTipoConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto${cont}" value="${concepto.idConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto${cont}" value="${concepto.Concepto}" readonly style="width: 330px"></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Abreviatura${cont}" value="${concepto.Abreviatura}" readonly></input>
                        </td>
                        
                        <td>
                            <input type="text" class="form-control" id="Monto${cont}" value="${concepto.Monto}" readonly></input>
                        </td>
                        
                        <td>
                            <input type="text" class="form-control" id="Porcentaje${cont}" value="${concepto.Porcentaje}" readonly style="width: 120px"></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="ClaveSAT${cont}" value="${concepto.ClaveSAT}" readonly style="width: 120px"></input>
                        </td>
                        `;


                    text = text + `
                    <td>
                        <div class="form-group hidden-xs" bis_skin_checked="1">
                            <label for="ExtraeArchivo${cont}">Extraer información<span class="form-text">*</span>:</label>
                            <input type="file" id="ExtraeArchivo${cont}" name="ExtraeArchivo${cont}" class="obligatorio">
                            <small id="EExtraeArchivo${cont}" class="etiquetaError form-text form-text-error"></small>
                        </div>
                    </td>
                    <td>
                        <div>
                            <button type="button" class="btn btn-primary" id="SubirArchivo${cont}" onclick="subir_archivo(${cont})">Subir archivo</button>
                        </div>
                    </td>
                        </tr>
                    `;
                    cont++;
                    $("#tablaResultadosConceptos tbody").append(text);
                });
            }
        }
    })

}

function subir_archivo(cont) {
    // Aquí puedes añadir el código para manejar la subida del archivo.
    const fileInput = document.getElementById('ExtraeArchivo' + cont);
    const file = fileInput.files[0];


    console.log("$('#idTipoConcepto' + cont).val()");
    console.log($('#idTipoConcepto' + cont).val());
    // Crear un FormData object
    const formData = new FormData();
    formData.append('archivo', file);
    formData.append('idTipoConcepto', $('#idTipoConcepto' + cont).val());
    formData.append('idConcepto', $('#idConcepto' + cont).val());
    console.log("formData");
    console.log(formData);
    if (file) {
        // Procesar el archivo (por ejemplo, enviarlo a un servidor)
        console.log(`Subiendo archivo ${file.name} con id de botón SubirArchivo${cont}`);

        $.ajax({
            async: false,
            type: "POST",
            url: "/prestaciones/extraer-concepto-de-archivo",
            data: formData,
            processData: false,
            contentType: false,
            success: function (concepto) {

                if (concepto.Obtenido) {
                    
                    abrirModal("Información cargada", 
                    `
                    Concepto: ${concepto.concepto} <br> <br>
                    Porcentaje: ${concepto.porcentaje}<br><br>
                    Monto: ${concepto.monto}
                    `, "");
                    
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