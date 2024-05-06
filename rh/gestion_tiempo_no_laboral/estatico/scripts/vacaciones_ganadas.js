$gmx(document).ready(function(){
    $("#btnGuardaDiasGan").click(guardar_vacacionesganadas);
    $("#btnBuscaPeriodos").click(obtener_periodos);

    $(document).on('click', "input:checkbox", un_solo_checkbox);

    // $(document).on('click', "input:checkbox", function(){
    //     console.log("si entra");
    //     var $box = $(this);
    //     console.log($box);
    //     if($box.is(":checked")){
    //         console.log($box.checked);
    //         var group = "input:checkbox[name='" + $box.attr("name") + "']";
    //         console.log($box.attr("name"));
    //         $(group).prop("checked", false);
    //         $box.prop("checked", true);
    //     }else{
    //         $box.prop("checked", false);
    //     }
    // });

    $("#Fecha").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true
    });
});

function guardar_vacacionesganadas(event){
    event.preventDefault();
    var validaEmpleado = true;
    var existeNumeroEmpleado = $("#idPersona").length > 0;
    //console.log($("#idPersona").val());
    if(!existeNumeroEmpleado || ($("#idPersona").val()) === ""){
        var validaEmpleado = false;
        $("#NumeroEmpleadoSeleccionado").addClass("form-control-error");
        $("ENumEmp").text("Seleccione un empleado");
    }
    if(validarFormulario($("#formularioVacacionesGanadas")).valido && validaEmpleado){
        var FechaFormateada = convertirFechaParaEnvio($("#Fecha").val());
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-tiempo-no-laboral/guardar-dias-persona",
            data: {
                "idPeriodo": 3,
                "idPersona": $("#idPersona").val(),
                "DiasGanados": $("#DiasGanados").val(),
                "Fecha": $("#Fecha").val(),
                "Activo": $("#ActVacacionesGanadas").val() - 1
            },
            success: function(data){
                if(data.guardado){
                    abrirModal("Información guardada", "Los datos de Vacaciones ganadas se han guardado correctamente.", "recargar");
                }
            }
        });
    }
}

function obtener_periodos(){
    if($("#NumeroEmpleadoSeleccionado").val() != ""){
        $("#lblDiasGanados").toggle();
        $("#DiasGanados").toggle();
        $("#lblFecha").toggle();
        $("#Fecha").toggle();
        $("#tabPeriodos").toggle();

        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-*tiempo-no-laboral/obtener-dias-persona",
            data: {
                "idPersona": $("#idPersona").val()
            },
            success: function(data){
                if(data){
                    var cont = 0;
                    data.forEach(function(DiasPersona){
                        var text = `
                        <tr>
                            <td><input type="checkbox" name="type" id="check${cont}" class="only-one"></td>
                            <td><input type="text" class="form-control" id="Periodo${cont}" value=${DiasPersona.idPeriodo} readonly></td>
                        </tr>
                        `;
                        cont++;
                        $("#tabPeriodos tbody").append(text);
                    });
                }
            }
        });
    }
}

function un_solo_checkbox(){
    
    var $box = $(this);
    if($box.is(":checked")){
        var group = "input:checkbox[name='" + $box.attr("name") + "']";
        $(group).prop("checked", false);
        $box.prop("checked", true);
    }else{
        $box.prop("checked", false);
    }
}

function verifica_seleccion(check){
    if(!check.checked){
        check.checked = 1;
    }
}