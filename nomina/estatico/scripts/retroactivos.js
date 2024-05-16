$gmx(document).ready(function(){
    $("#TipoProceso").change(masivo_individual);
    $("#btnGuardarRetroactivos").click(guardar_retroactivos);
});

function masivo_individual(event){
    event.preventDefault();
    var TipoProceso = $("#TipoProceso").val();
    if(TipoProceso === "2"){
        $("#NumEmpGrupo").hide();
        $("#idPersona").val("");
        $("#tablaEmpleadoSeleccionado").hide();
    }else if (TipoProceso === "1") {
        $("#NumEmpGrupo").show();
        if ($("#idPersona").val()) {
            $("#tablaEmpleadoSeleccionado").show();
        }
    }
}

function guardar_retroactivos(){
    var validaEmpleado = true;
    if ($("#TipoProceso").val() == 1) {
        var existeNumeroEmpleado = $("#idPersona").length > 0;
        if (!existeNumeroEmpleado || $("#idPersona").val() === "") {
            var validaEmpleado = false;
            // campo.removeClass("form-control-error");
            $("#NumeroEmpleadoSeleccionado").addClass("form-control-error");
            $("#ENumEmp").text("Seleccione un empleado");
        }
    } else {
        $("#idPersona").val("");
    }

    if(validarFormulario($("#formularioRetroactivos")).valido && validaEmpleado){
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/guardar-retroactivos",
            data: $("#formularioRetroactivos, #idPersona").serialize(),
            success: function(data){
                if(data.guardado){
                    abrirModal("Días retroactivos creados", "Los días retroactivos fueron creados de manera correcta.", "recargar");
                }else{
                    abrirModal("Días retroactivos no creados", "Los días retroactivos no pudieron crearse.", "recargar");
                }
            }
        });
    }
}

function buscar_retroactivos(event){
    if(validarFormulario($("#formularioBuscarRetroactivos")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/buscar-retroactivos",
            data: {
                "idPersona": $("#idPersona").val(),
            },
            success: function(data){
                if(data.length > 0){
                    $("#EResultado").text("");
                    $("#tablaResultadosRetroactivos").show();
                    $("#tablaResultadosRetroactivos tbody").empty();
                    var cont = 1;
                    data.forEach(function(retroactivo){
                        text = `
                        <tr>
                            <td>
                                <input type="text" class="form-control" id="Quincena${cont}" value="${retroactivo.idQuincena}" style="width: 300px;" readonly>
                            </td>
                            <td>
                                <input type="text" class="form-control" id="DiasRetroactivos${cont}" value="${retroactivo.Dias}" style="width: 100px;" readonly>
                            </td>
                            <td>
                                <textarea id="Descripcion${cont}" name="Descripcion${cont}" class="form-control" rows="3" style="width: 400px; resize: none" readonly>${retroactivo.Descripcion}</textarea>
                            </td>
                        </tr>
                        `;
                        $("#tablaResultadosRetroactivos tbody").append(text);
                    });
                }
            }
        })
    }
}

function funcionSeleccionar(){
    buscar_retroactivos();
}