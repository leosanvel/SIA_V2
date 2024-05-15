$gmx(document).ready(function () {

   $("#btnGuardaDiasPersona").click(function (event) {
        event.preventDefault();
        if (validarFormulario($("#formularioCreaDiasPersona")).valido) {
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-tiempo-no-laboral/guardar-dias-persona",
                data: $("#formularioCreaDiasPersona, #idPersona").serialize(),
                success: function (data) {
                    if (data.idPersona) {
                        abrirModal("Información guardada", "Los días se agregaron con éxito", "recargar");
                    }
                }
            });
        }
    });

    cargarDiasPersona();
});

function cargarDiasPersona(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/buscar-dias-persona",
        success: function(data){
            if(data.length > 0){
                $("#EResultado").text("");
                $("#tablaResultadosDiasPersona").show();
                // Limpiar la tabla existente
                $("#tablaResultadosDiasPersona tbody").empty();
                cont = 1;
                data.forEach(function(diaPersona){
                    var FechaFormateada = convertirFechaParaVisualizacion(diaPersona.Fecha);
                    var Fechadate = new Date(diaPersona.Fecha).getTime();
                    var tiempoTranscurrido = Date.now();
                    var Hoy = new Date(tiempoTranscurrido);
                    var diff = Hoy - Fechadate;
                    var dias = diff/(1000*60*60*24);
                    console.log(diaPersona.Activo);
                    text = `
                    <tr>
                        <td>
                            <input type="text" class="form-control" id="NumEmpleado${cont}" value="${diaPersona.Nombre}" readonly style="width: 500px;"></td>
                        <td>
                        <select id="Periodo${cont}" name="Periodo${cont}" class="form-control" disabled style="width: 75px;">
                            <option value="1">PP</option>
                            <option value="2">SP</option>
                            <option value="3">VG</option>
                        </select>
                        <script>
                            $("#Periodo${cont}").val(${diaPersona.idPeriodo});
                        </script>
                    </td>
                    <td><input type="text" class="form-control" id="DiasGanados${cont}" value="${diaPersona.DiasGanados}" readonly style="width: 75px;"></td>
                    <td>
                        <div class="form-group datepicker-group"  style="z-index: 7; width: 175px">
                            <input type="text" id="Fecha${cont}" class="form-control fecha" value="${FechaFormateada}" readonly>
                            <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                            <small id="EFechaInicio${cont}" class="etiquetaError form-text form-text-error"></small>
                        </div>
                    </td>
                    <td>
                        <select id="ActDiasPersona${cont}" name="ActDiasPersona${cont}" class="obligatorio form-control" value="${diaPersona.Activo}" disabled style="width: 120px;">
                            <option value="0">Inactivo</option>
                            <option value="1">Activo</option>
                        </select>
                        <script>
                            document.ready = document.getElementById("ActDiasPersona${cont}").value = "${diaPersona.Activo}"
                        </script>
                    </td>
                    <td><button id="eliminar${cont}" type="button" class="btn btn-primary" onclick="eliminar_dias(${cont})" disabled>Eliminar días</td>
                    <td><button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar${cont}" onclick="editar_aceptar('${cont}')">Editar</button></td>
                    <td><button type="button" class="btn btn-primary oculta-empleado" id="Cancelar${cont}" onclick="cancelar('${cont}', '${diaPersona.Activo}')" style="display: none;">Cancelar</button></td>
                    </tr>
                    `
                    $("#tablaResultadosDiasPersona tbody").append(text);
                    if(dias >= 180){
                        $("#eliminar" + cont).attr("disabled", false);
                    }
                    cont++;0
                });
            }else{
                $("#tablaResultadosDiasPersona tbody").empty();
                $("#tablaResultadosDiasPersona").hide;
                $("#MensajeTablaDiasPersona").text("Por el momento no existen días persona registrados.");
            }
        }
    });
}

function editar_aceptar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        $("#ActDiasPersona" + data).attr("disabled", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_diaspersona(data);
    }
}

function cancelar(data1, data2) {
    $("#ActDiasPersona" + data1).attr("disabled", true);

    $("#ActDiasPersona" + data1).val(data2);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_diaspersona(dato){
    var datos = new FormData();
    datos.append("idPersona", $("#NumEmpleado" + dato).val());
    datos.append("idPeriodo", $("#Periodo" + dato).val());
    datos.append("DiasGanados", $("#DiasGanados" + dato).val());
    datos.append("Fecha", $("#Fecha" + dato).val());
    datos.append("Activo", $("#ActDiasPersona" + dato).val());
    //datos = JSON.stringify(datos);

    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/guardar-dias-persona",
        data: datos,
        enctype: 'multipart/form-data',
        contentType: false,
        processData: false,
        success: function(data){
            if(data.guardado){
                abrirModal("Información guardada", "Los datos de Dias Persona se guardaron correctamente.", "recargar");
            }
        }
    })
}

function eliminar_dias(id){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/eliminar-dias",
        data: {
            id: id,
        },
        success: function(data){
            if(data.eliminado){
                abrirModal("Días Eliminados" ,"Se borraron los días exitosamente", "recargar");
            }
        }
    });
}

function configuraDatepickers(idInicio, idFin, data) {
    $(`#${idInicio}${data}, #${idFin}${data}`).datepicker({
    // $(`#fechaInicioFormateada${data}, #fechaFinFormateada${data}`).datepicker({
        changeYear: true,
        changeMonth: true,
        beforeShow: function (input, inst) {
            var fechaLimite = this.id === `${idInicio}${data}` ? $(`#${idFin}${data}`).datepicker("getDate") : $(`#${idInicio}${data}`).datepicker("getDate");
            if (this.id === `${idInicio}${data}`) {
                if (fechaLimite) {
                    $(this).datepicker("option", "maxDate", fechaLimite);
                } else {
                    $(this).datepicker("option", "maxDate", null);
                }
            } else {
                if (fechaLimite) {
                    $(this).datepicker("option", "minDate", fechaLimite);
                }
                else {
                    $(this).datepicker("option", "minDate", null);
                }
            }
        },
        onSelect: function (dateText) {
            var fechaFinal = $(`#${idFin}${data}`).datepicker("getDate");
            var fechaInicial = $(`#${idInicio}${data}`).datepicker("getDate");

            if ((fechaFinal && fechaInicial) && (fechaInicial > fechaFinal)) {
                abrirModal("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.", "");
                $(this).val("");
            }
        }
    });
}