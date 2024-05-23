$gmx(document).ready(function(){
    $("#Mes").change(obtener_select_concepto);
    $("#btnAgregarAlCalendario").click(agregar_fecha);
    configuraDatepickers("FechaInicio", "FechaFin", "");
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
            if(data.lenght > 0){
                
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