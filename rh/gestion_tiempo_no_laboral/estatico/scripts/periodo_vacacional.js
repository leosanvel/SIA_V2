$gmx(document).ready(function(){
    cargarPeriodoVacacional();
    $("#btnGuardaPeriodoVacacional").click(guardar_periodo_vacacional);

    $("#FechaInicio, #FechaFin").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,
        beforeShow: function(input, inst){
            var fechaLimite = this.id === "FechaInicio" ? $("#FechaFin").datepicker("getDate") : $("#FechaInicio").datepicker("getDate");
            if(this.id === "FechaInicio"){
                if(fechaLimite){
                    $(this).datepicker("option", "maxDate", fechaLimite);
                }else{
                    $(this).datepicker("option", "maxDate", null);
                }
            }else{
                if(fechaLimite){
                    $(this).datepicker("option", "minDate", fechaLimite);
                }else{
                    $(this).datepicker("option", "minDate", null);
                }
            }
        },
        onSelect: function(dataText){
            var fechaFinal = $("#FechaFin").datepicker("getDate");
            var fechaIncial = $("#FechaInicio").datepicker("getDate");

            if((fechaFinal && fechaIncial) && (fechaIncial > fechaFinal)){
                abrirModal("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.", "");
                $(this).val("");
            }
        }
    });
});

function cargarPeriodoVacacional(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/cargar-periodo-vacacional",
        success: function(data){
            $("#TabPeriodoVacacional").show();
            $("#TabPeriodoVacacional tbody").empty();
            data.forEach(function(PeriodoVacacional){

                var FechaInicioFormateada = convertirFechaParaVisualizacion(PeriodoVacacional.FechaInicio);
                var FechaFinFormateada = convertirFechaParaVisualizacion(PeriodoVacacional.FechaFin);
                text = `
                <tr>
                    <td>
                        <div class="form-group datepicker-group"  style="z-index: 10; width: 175px">
                            <input type="text" id="FechaInicio${PeriodoVacacional.idPeriodoVacacional}" class="form-control fecha" value="${FechaInicioFormateada}" readonly>
                            <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                            <small id="EFechaInicio${PeriodoVacacional.idPeriodoVacacional}" class="etiquetaError form-text form-text-error"></small>
                        </div>
                    </td>
                    <td>
                        <div class="form-group datepicker-group"  style="z-index: 10; width: 175px">
                            <input type="text" id="FechaFin${PeriodoVacacional.idPeriodoVacacional}" class="form-control fecha" value="${FechaFinFormateada}" readonly>
                            <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                            <small id="EFechaInicio${PeriodoVacacional.idPeriodoVacacional}" class="etiquetaError form-text form-text-error"></small>
                        </div>
                    </td>
                    <td>
                        <div class="form-group" style="z-index: 10; width: 75px">
                            <select id="Periodo${PeriodoVacacional.idPeriodoVacacional}" name="Periodo${PeriodoVacacional.idPeriodoVacacional}" class="form-control" disabled>
                                <option value="1">PP</option>
                                <option value="2">SP</option>
                                <option value="3">VG</option>
                            </select>
                            <script>
                                $("#Periodo${PeriodoVacacional.idPeriodoVacacional}").val(${PeriodoVacacional.idPeriodo});
                            </script>
                        </div>
                    </td>
                    <td><textarea rows="3" class="form-control" id="Descripcion${PeriodoVacacional.idPeriodoVacacional}" style="resize: none; width: 450px;" readonly>${PeriodoVacacional.Descripcion}</textarea></td> 
                    <td><button type="button" class="btn btn-primary" id="Generar${PeriodoVacacional.idPeriodoVacacional}" onclick="generar(${PeriodoVacacional.idPeriodoVacacional})">Generar</button></td>
                </tr>
                `
                $("#TabPeriodoVacacional tbody").append(text);
            });
        }
    });
}

function generar(idPeriodoVacacional){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/guardar-dias-persona",
        data: {
            "idPeriodoVacacional": idPeriodoVacacional,
            "DiasGanados": 10,
        },
        success: function(data){
            if(data.guardado){
                abrirModal("Vacaciones generadas de forma correcta", "El perido vacacional se ha generado de manera correcta", "recargar");
            }
        }
    });
}

function guardar_periodo_vacacional(event){
    event.preventDefault();
    if(validarFormulario($("#formularioPeriodoVacacional")).valido){

        var FechaInicio_string = $("#FechaInicio").val();
        var FechaFin_string = $("#FechaFin").val();

        var FechaInicio_format = convertirFechaParaEnvio(FechaInicio_string);
        var FechaFin_format = convertirFechaParaEnvio(FechaFin_string);

        $("#formularioPeriodoVacacional input[name='fechaInicioFormateada']").remove();
        $("#formularioPeriodoVacacional input[name='fechaFinFormateada']").remove();

        $("#formularioPeriodoVacacional").append('<input type="hidden" name="fechaInicioFormateada" value="' + FechaInicio_format + '">');
        $("#formularioPeriodoVacacional").append('<input type="hidden" name="fechaFinFormateada" value="' + FechaFin_format + '">');

        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-tiempo-no-laboral/guardar-periodo-vacacional",
            data: $("#formularioPeriodoVacacional").serialize(),
            success: function(data){
                if(data.guardado){
                    abrirModal("Información guardada", "El periodo vacacional se guardo correctamente.", "recargar");
                }
            }
        });
    }
}