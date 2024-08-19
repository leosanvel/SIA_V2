$gmx(document).ready(function () {

    $("#btnGuardaDiafestivo").click(function (event) {
        event.preventDefault();
        var validaEmpleado = true;
        if (validarFormulario($("#formularioCreaDiaFestivo")).valido) {
            var Fecha_string = $("#Fecha").val();
            var Fecha_format = convertirFechaParaEnvio(Fecha_string);  
            $("#formularioCreaDiaFestivo input[name='Fecha_format']").remove();      
            $("#formularioCreaDiaFestivo").append('<input type="hidden" name="Fecha_format" value="' + Fecha_format + '">');        
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-tiempo-no-laboral/guardar-dia-festivo",
                data: $("#formularioCreaDiaFestivo").serialize(),
                success: function (data) {
                    if (data.Fecha) {
                        abrirModal("Información guardada", "El Día Festivo se creó con éxito", "recargar");
                    }
                }
            });
        }
    });

    cargarFestividades();

    $("#Fecha").datepicker({
        changeYear: true,
        changeMonth: true,
        beforeShow: function(input, inst) {
            setTimeout(function () {
                inst.dpDiv.css({
                    top: (inst.input.offset().top + inst.input.outerHeight()) + 'px',
                    left: inst.input.offset().left + 'px'
                });
            }, 0);
        },
        onClose: function (dateText) {
            var FechaBusqueda = $("#Fecha").val();
            var Fecha_formateada = convertirFechaParaEnvio(FechaBusqueda);

            $("#formularioCreaDiaFestivo input[name='Fecha_formateada']").remove();
            $("#formularioCreaDiaFestivo").append('<input type="hidden" name="Fecha_formateada" value="' + Fecha_formateada + '">');        
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-tiempo-no-laboral/buscar-dia-festivo",
                data: $("#formularioCreaDiaFestivo").serialize(),
                success: function (data) {
                    console.log(data.Encontrado);
                    if (data.Encontrado ==! false) {
                        $("#Descripcion").val(data.Descripcion);
                        abrirModal("Fecha encontrada", 'La fecha ya está registrada. A continuación modificarás su descripción', "");
                    }
                }
            });
        }
    });
    

});

function cargarFestividades() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/consulta-dias-festivos",
        success: function (data) {
            if (data.length > 0) {
                $("#EResultadoFestividades").text("");
                $("#tablaResultadosFestividad").show();
                // Limpiar la tabla existente
                $("#tablaResultadosFestividad tbody").empty();
                // Iterar sobre los justificantes y agregar filas a la tabla
                data.forEach(function (festividad) {
                    // Formatear las fechas
                    var FechaFormateada = convertirFechaParaVisualizacion(festividad.Fecha);
                    var FechaCreacionFormateada = convertirFechaParaVisualizacion(festividad.FechaCreacion);
                    // Agregar filas a la tabla con fechas formateadas
                    $("#tablaResultadosFestividad tbody").append(`
                            <tr>
                                <td>${festividad.idDiaFestivo}</td>
                                <td>
                                    <div class="form-group datepicker-group" style="z-index: 10;">
                                        <input type="text" id="Fecha${festividad.idDiaFestivo}"
                                        class="form-control" value="${FechaFormateada}" readonly>
                                        <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                                        <small id="EFecha" class="etiquetaError form-text form-text-error"></small>
                                    </div>
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="Descripcion${festividad.idDiaFestivo}" value="${festividad.Descripcion}" style="width: 300px;" readonly>
                                </td>
                                <td>
                                    <div style="display: block;">
                                        <button type="button" class="btn btn-primary" id="Eliminar${festividad.idDiaFestivo}" onclick="eliminar(${festividad.idDiaFestivo})">Eliminar</button>
                                    </div>
                                </td>
                                <td>
                                    <div style="display: block;">
                                        <button type="button" class="btn btn-primary" id="Editar_Aceptar${festividad.idDiaFestivo}" onclick="editar_aceptar(${festividad.idDiaFestivo})">Editar</button>
                                    </div>
                                </td>
                                <td>
                                <div style="display: block;">
                                    <button type="button" class="btn btn-secondary" id="Cancelar${festividad.idDiaFestivo}" onclick="cancelar('${festividad.idDiaFestivo}')" style="display: none">Cancelar</button>
                                </div>
                            </td>
                            </tr>
                        `);
                });
            } else {
                $("#tablaResultadosFestividad tbody").empty();
                $("#tablaResultadosFestividad").hide;
                $("#MensajeTablaFestividad").text("Por el momento no existen fechas registradas.");
            }
    
        }
    });
}

function editar_aceptar(idDiaFestivo){
    if($("#Editar_Aceptar" + idDiaFestivo).text() == "Editar"){
        $("#Fecha" + idDiaFestivo).prop("readonly", false);
        $("#Fecha" + idDiaFestivo).datepicker("option", "disabled", false);
        $("#Descripcion" + idDiaFestivo).prop("readonly", false);
        configuraDatepickers("Fecha", idDiaFestivo);

        $("#Editar_Aceptar" + idDiaFestivo).text("Aceptar");
        $("#Cancelar" + idDiaFestivo).show();
    }else{
        guardar_modificar_dia_festivo(idDiaFestivo);
    }
}

function cancelar(idDiaFestivo){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/cancelar-dia-festivo",
        data: {
            idDiaFestivo: idDiaFestivo
        },
        success: function(DiaFestivo){
            Fecha = convertirFechaParaVisualizacion(DiaFestivo.Fecha);

            $("#Fecha" + idDiaFestivo).attr("readonly", true);
            $("#Fecha" + idDiaFestivo).datepicker("option", "disabled", true);
            $("#Descripcion" + idDiaFestivo).attr("readonly", true);

            $("#Fecha" + idDiaFestivo).val(Fecha);
            $("#Descripcion" + idDiaFestivo).val(DiaFestivo.Descripcion);

            $("#Editar_Aceptar" + idDiaFestivo).text("Editar");
            $("#Cancelar" + idDiaFestivo).hide();
        }
    });
}

function eliminar(idDiaFestivo){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/eliminar-dia-festivo",
        data: {
            idDiaFestivo: idDiaFestivo
        },
        success: function(data){
            if(data.eliminado){
                abrirModal("Día festivo eliminado", "El día festivo se ha eliminado de manera correcta", "recargar");
            }
        }
    });
}

function configuraDatepickers(idFecha, data){
    $(`#${idFecha}${data}`).datepicker({
        dateFormat: "dd/mm/yy",
        changeYear: true,
        changeMonth: true
    });
}