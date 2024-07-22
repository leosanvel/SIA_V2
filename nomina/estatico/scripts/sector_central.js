$gmx(document).ready(function(){
    $("#btnBuscar").click(buscar_sector_central);
    $("#btnSubirArchivo").on("click", function () { subir_archivo(); });

});

function subir_archivo() {
    if (validarFormulario($("#formulario_cargar_archivo")).valido) {
        // Aquí puedes añadir el código para manejar la subida del archivo.

        const fileInput = document.getElementById('ArchivoZE');
        const file = fileInput.files[0];

        // Crear un FormData object
        const formData = new FormData();
        formData.append('archivo', file);
        window.document.getElementById("ArchivoZE").value = "";
        if (file) {
            $.ajax({
                async: false,
                type: "POST",
                url: "/nomina/extraer-archivoze",
                data: formData,
                processData: false,
                contentType: false,
                success: function (resp) {
                    if (resp.Resultado == 1) {
                        
                        var tablaHTML = '<table class="table table-striped">';
                        tablaHTML += '<thead><tr>' +
                            '<th>Año fiscal</th>' +
                            '<th>Zona Económica</th>' +
                            '<th>Nivel</th>' +
                            '<th>Sueldo base</th>' +
                            '<th>Compensación Garantizada</th>' +
                            '</tr></thead><tbody>';
                        /*
                            resp.Informacion.forEach(function (registro) {
                            tablaHTML += '<tr>' +
                                '<td>' + registro.idAnioFiscal + '</td>' +
                                '<td>' + registro.idZonaEconomica + '</td>' +
                                '<td>' + registro.idNivel + '</td>' +
                                '<td>' + registro.SueldoBase + '</td>' +
                                '<td>' + registro.CompensacionGarantizada + '</td>' +
                                '</tr>';                            
                        });
                        */
                        tablaHTML += '</tbody></table>';
                        /*   
                        document.getElementById('tituloModalImportar').textContent = "Información cargada";
                        document.getElementById('contenidoModalImportar').innerHTML = tablaHTML;
                        $('#ModalImportar').attr('data-comportamiento', "recargar");
                        $('#ModalImportar').modal('show');
                       */ 
                        
                        abrirModal("Tabulador ZE", "La información se cargo correctamente", "");
                    }
                    else{
                        abrirModal("Carga fallida", resp.Informacion, "");
                    }
                }
            })
        } else {
            abrirModal("Archivo no seleccionado", "Por favor seleccione un archivo.", "");
        }
    }
}

function Limpiar(Accion){
    switch (Accion) {
        case 'A':
            window.document.getElementById("ArchivoZE").value = "";
        break;
        case 'M':
            window.document.getElementById("AnioFiscal").value = "0";
            $("#tblSector tbody").empty();
            $("#tblSector").hide();            
        break;
        default:
          //Declaraciones ejecutadas cuando ninguno de los valores coincide con el valor de la expresión
        break;
    }
}

function buscar_sector_central(){
    if(validarFormulario($("#formulario_modificar_tabulador")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/buscar-sector-central",
            data: $("#formulario_modificar_tabulador").serialize(),
            success: function(data){
                if (data.respuesta == 0) {    
                    var text = "";
                    var codigo = "";
                    $("#tblSector").show();       
                    $("#tblSector tbody").empty();
                    data.lista.forEach(function(dlista) {
                        codigo = dlista.idAnioFiscal + "" + dlista.idZonaEconomica + "" + dlista.idNivel
                        text = text + `
                        <tr>
                            <td>
                                ${dlista.idAnioFiscal}
                            </td>  
                            <td>
                                ${dlista.idZonaEconomica}
                            </td>
                            <td>
                                ${dlista.idNivel}
                            </td>
                            <td>
                                <input class="form-control" id="SB${codigo}" name="SB${codigo}" type="text" value="${dlista.SueldoBase}" readonly>                                
                            </td>
                            <td>
                                <input class="form-control" id="CG${codigo}" name="CG${codigo}" type="text" value="${dlista.CompensacionGarantizada}" readonly>                             
                            </td>
                            <td>
                                <button class="btn btn-primary btn-sm" id="btnEditarGuardar${codigo}" name="btnEditarGuardar${codigo}" type="button" onclick="Activar('${codigo}','${dlista.idAnioFiscal}','${dlista.idZonaEconomica}','${dlista.idNivel}')" >Editar</button>                             
                            </td>
                        </tr>
                        `});
                    $("#tblSector tbody").append(text);                                     
                }
                else{
                    $("#tblSector").show();  
                    $("#tblSector tbody").empty();
                    text = "";                
                    text = text + "<tr>";
                    text = text + "<td colspan='6'><label>"+data.informacion+"</label></td>";
                    text = text + "</tr>";
                    $("#tblSector tbody").append(text);
                }
            }
        });
    }
}

function Activar(codigo,anio,ze,nivel){
    if ($("#btnEditarGuardar" + codigo).text() == "Editar") {
        $("#SB" + codigo).attr("readonly", false);
        $("#CG" + codigo).attr("readonly", false);
        $("#SB" + codigo).focus();
        $("#btnEditarGuardar" + codigo).text("Guardar");
        //$("#Cancelar" + data).toggle();
    }
    else {
        guardar_tabulador(codigo,anio,ze,nivel);
    }
}

function guardar_tabulador(codigo,anio,ze,nivel){
    $.ajax({
        async: false,
        type: "POST",
        url: "/nomina/guardar-tabulador",
        data: {
            "idAnioFiscal": anio,
            "idZonaEconomica": ze,
            "idNivel": nivel,
            "SueldoBase": $("#SB" + codigo).val(),
            "CompensacionGarantizada": $("#CG" + codigo).val(),
        },
        success: function (data) {
            if (data.respuesta == 0){
                abrirModal("Tabulador", "Los cambios se realizaron correctamente.", "");
                $("#SB" + codigo).attr("readonly", true);
                $("#CG" + codigo).attr("readonly", true);
                $("#btnEditarGuardar" + codigo).text("Editar");
            }
            //cancelar(data.idJustificante);
        }
    });   
}