$gmx(document).ready(function () {


    $("#FechaEfecto").datepicker({ dateFormat: 'dd/mm/yy', changeYear: true, changeMonth: true });

    $("#btnDarDeBaja").click(function (event) {abrirAdModal()});

    $("#btnDarBajaModal").click(function(event) {dar_baja()});

    $("#btnBuscaBajaEmpleado").click(function (event) {busca_baja_empleado()});

});

function abrirAdModal(){
    if (validarFormulario($("#frmResultadoPuesto")).valido){
        $("#MensajeAdModal").html("Se va a dar de baja al empleado " + $("#NombreEmpleado").text() + " " + $("#ApellidosEmpleado").text() + "." + " ¿Seguro quiere dar de baja?");
        $("#BajaEmpleadoModal").modal("show");
    }
}

function busca_baja_empleado() {
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


                    $("#Puesto").val(datos.Puesto);
                    $("#idPuesto").val(datos.idPuesto);

                    $("#TipoEmpleado").val(datos.TipoEmpleado);
                    var optionsHTML = `<option value='0'> -- Seleccione -- </option>`;
                    datos.CausasBaja.forEach(function (causa) {
                        if (causa.idCausaBaja == datos.empleadoPuesto.idCausaBaja) {
                            optionsHTML += `<option selected value='${causa.idCausaBaja}'> ${causa.CausaBaja} </option>`;
                        } else {
                            optionsHTML += `<option value='${causa.idCausaBaja}'> ${causa.CausaBaja} </option>`;
                        }
                    });

                    $("#CausaBaja").html(optionsHTML);
                    $("#TipoAlta").val(datos.TipoAlta);

                    if (datos.TipoEmpleado == "Plaza federal") {
                        $("#contenedorCheckbox").show();
                    }


                    if (datos.empleadoPuesto.ConservaVacaciones == 1) {
                        $("#checkboxConservarVacaciones").prop("checked", true);
                    } else {
                        $("#checkboxConservarVacaciones").prop("checked", false);
                    }

                    if (datos.empleadoPuesto.FechaEfecto != null) {
                        var FechaEfecto = convertirFechaParaVisualizacion(datos.empleadoPuesto.FechaEfecto);
                    } else {
                        var FechaEfecto = ""
                    }

                    $("#Observaciones").val(datos.empleadoPuesto.Observaciones);
                    $("#FechaEfecto").val(FechaEfecto);
                }
            }
        });
    }
}

function dar_baja() {
    if (validarFormulario($("#frmResultadoPuesto")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/dar-baja-empleado",
            data: $("#frmResultadoPuesto, #idPersona").serialize(),
            success: function (datos) {
                if (datos.NoEncontrado) {
                    abrirModal("Error", "Ha ocurrido un problema", "");
                }
                if (datos.DadoBaja) {
                    abrirModal("Éxito", "El empleado ha sido dado de baja correctamente", "recargar");
                } else if (datos.Guardado) {
                    abrirModal("Éxito", "La información se guardó correctamente", "recargar");
                }
            }
        });
    }

}

function funcionSeleccionar() {
    busca_baja_empleado();
}