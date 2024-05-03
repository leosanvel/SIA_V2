$gmx(document).ready(function () {


    $("#FechaEfecto").datepicker({ dateFormat: 'dd/mm/yy', changeYear: true, changeMonth: true });

    $("#btnDarDeBaja").click(function (event) {dar_baja()});

    $("#btnBuscaBajaEmpleado").click(function (event) {busca_baja_empleado()
    });

});

function busca_baja_empleado(){
    var idPersona = $("#idPersona").val()
    if (idPersona) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/obtener-puestos-empleado",
            data: {
                "idPersona": $("#idPersona").val()
            },
            success: function (datos) {
                if (datos.NoEncontrado) {
                    abrirModal("Error", "El empleado no tiene asignado un puesto", "");
                    $("#ResultadoPuesto input").val("");
                    $("#ResultadoPuesto select").val("0");
                    $("#ResultadoPuesto").hide();
                }
                else {
                    $("#ResultadoPuesto input").val("");
                    $("#ResultadoPuesto select").val("0");

                    $("#ResultadoPuesto").show();

                    if (datos.empleadoPuesto.FechaInicio != null) {
                        var FechaInicio = convertirFechaParaVisualizacion(datos.empleadoPuesto.FechaInicio);
                    } else {
                        var FechaInicio = "-"
                    }
                    if (datos.empleadoPuesto.FechaTermino != null) {
                        var FechaFin = convertirFechaParaVisualizacion(datos.empleadoPuesto.FechaTermino);
                    } else {
                        var FechaFin = "-"
                    }

                    $("#Puesto").val(datos.Puesto);
                    $("#idPuesto").val(datos.idPuesto);
                    $("#fechaInicio").val(FechaInicio);
                    $("#FecTerm").val(FechaFin);
                    $("#TipoEmpleado").val(datos.TipoEmpleado);
                    var optionsHTML = `<option value='0'> -- Seleccione -- </option>`;
                    datos.CausasBaja.forEach(function (causa) {
                        optionsHTML += `<option value='${causa.idCausaBaja}'> ${causa.CausaBaja} </option>`;
                    });
                    $("#CausaBaja").html(optionsHTML);
                    $("#TipoAlta").val(datos.TipoAlta);

                    if (datos.TipoEmpleado == "Plaza federal"){
                        $("#contenedorCheckbox").show();
                    }

                }
            }
        });
    }
}

function dar_baja(){
    if (validarFormulario($("#frmResultadoPuesto")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/dar-baja-empleado",
            data: $("#frmResultadoPuesto, #idPersona").serialize(),
            success: function (datos) {
                if (datos.NoEncontrado) {
                    abrirModal("Error", "Ha ocurrido un problema", "");
                }else{
                    abrirModal("Éxito", "El empleado ha sido dado de baja correctamente", "recargar");
                }
            }
        });
    }
    
}