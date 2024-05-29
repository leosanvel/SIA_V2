$gmx(document).ready(function(){
    $("#Mes").change(obtener_select_concepto);
    $("#btnAgregarAlCalendario").click(agregar_fecha);
    $("#btnGenerarCalendario").click(generar_calendario);
    configuraDatepickers("FechaInicio", "FechaFin", "");
    obtener_fecha();
});

function obtener_select_concepto(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/nomina/obtener-select-concepto",
        data: {
            "idMes": $("#Mes").val()
        },
        success: function(data){
            if(data){
                $("#Concepto").html(data);
            }
        }
    });
}

function agregar_fecha(event){
    event.preventDefault();

    if(validarFormulario($("#formularioCalendarioPagos")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/agregar-fecha-calendario",
            data: $("#formularioCalendarioPagos").serialize(),
            success: function(data){
                if(data.guardado){
                    abrirModal("Fecha agregada", "La fecha ha sido agregada correctamente.", "recargar")
                }
                if(data.actualizado){
                    abrirModal("Fecha actualizada", "La fecha ha sido actualizada correctamente.", "recargar")
                }
            }
        });
    }
}

function obtener_fecha(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/nomina/obtener-fechas-calendario",
        success: function(data){
            if(data.Fechas.length > 0){

                var Meses = '';
                data.Meses.forEach(function(mes){
                    Meses += `<option value="${mes.idMes}">${mes.Mes}</option>`;
                });

                var QuincenasCalendario = '';
                data.QuincenasCalendario.forEach(function(quincena){
                    QuincenasCalendario += `<option value="${quincena.idQuincenaCalendario}">${quincena.QuincenaCalendario}</option>`
                });

                var Actividades = '';
                data.Actividades.forEach(function(actividad){
                    Actividades += `<option value="${actividad.idActividadCalendario}">${actividad.ActividadCalendario}</option>`
                })

                $("#tablaFechasCalendario").show();
                $("#tablaFechasCalendario tbody").empty();
                var cont = 1;
                data.Fechas.forEach(function(fecha){
                    var FechaInicio = convertirFechaParaVisualizacion(fecha.FechaInicio);
                    var FechaFin = convertirFechaParaVisualizacion(fecha.FechaFin);
                    text = `
                        <tr>
                            <td>
                                <input type="text" id="Periodo${cont}" class="form-control" value="${fecha.Periodo}" readonly>
                            </td>
                            <td>
                                <select id="Mes${cont}" name="Mes${cont}" class="obligatorio form-control" disabled>
                                    ${Meses}
                                </select>
                            </td>
                            <td>
                                <select id="QuincenaCalendario${cont}" name="QuincenaCalendario${cont}" class="obligatorio form-control" readonly disabled>
                                    ${QuincenasCalendario}
                                </select>
                            </td>
                            <td>
                                <select id="ActividadCalendario${cont}" name="ActividadCalendario${cont}" class="obligatorio form-control" readonly disabled>
                                    ${Actividades}
                                </select>
                            </td>
                            <td>
                                <input type="text" id="FechaInicio${cont}" class="form-control" value="${FechaInicio}" readonly>
                            </td>
                            <td>
                                <input type="text" id="FechaFin${cont}" class="form-control" value="${FechaFin}" readonly>
                            </td>
                        </tr>
                    `;
                    $("#tablaFechasCalendario tbody").append(text);
                    $(`#Mes${cont}`).val(fecha.idMes);
                    $(`#QuincenaCalendario${cont}`).val(fecha.idQuincenaCalendario);
                    $(`#ActividadCalendario${cont}`).val(fecha.idActividadCalendario);
                    cont++;
                });
            }
        }
    })
}

function generar_calendario(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/nomina/generar-calendario-pagos",
        success: function(data){
            if(data){

            }
        }
    })
}

function configuraDatepickers(idInicio, idFin, data, FechaInicio, FechaFin) {
    $(`#${idInicio}${data}, #${idFin}${data}`).datepicker({
        // $(`#fechaInicioFormateada${data}, #fechaFinFormateada${data}`).datepicker({
        changeYear: true,
        changeMonth: true,
        beforeShow: function (input, inst) {
            var fechaLimite = this.id === `${idInicio}${data}` ? $(`#${idFin}${data}`).datepicker("getDate") : $(`#${idInicio}${data}`).datepicker("getDate");
            if (this.id === `${idInicio}${data}`) {
                if (fechaLimite) {
                    $(this).datepicker("option", "maxDate", fechaLimite);
                    console.log(typeof (fechaLimite));
                } else {
                    //$(this).datepicker("option", "maxDate", FechaFin);
                }
            } else {
                if (fechaLimite) {
                    $(this).datepicker("option", "minDate", fechaLimite);
                }
                else {
                    //$(this).datepicker("option", "minDate", FechaInicio);
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