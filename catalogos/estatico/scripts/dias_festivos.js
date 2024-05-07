$gmx(document).ready(function(){
    inicializacion();
    hablitar_calendario();
});

function hablitar_calendario(){
    $('input[id^=FechaDiaFestivo]').datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,
        disabled: true,
    });
}

function inicializacion(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/Catalogos/cargar_diasfestivos",
        success: function(data){
            $("#TabDiasFestivos").show();
            $("#TabDiasFestivos tbody").empty();
            data.forEach(function(DiaFestivo){
                var FechaFormateada = convertirFechaParaVisualizacion(DiaFestivo.fecha);
                text = `
                <tr>
                    <td><input type="text" class="form-control" id="idDiaFestivo${DiaFestivo.idDiaFestivo}" value="${DiaFestivo.idDiaFestivo}" readonly></td>
                    <td>
                        <div class="form-group datepicker-group" style="z-index: 1;">
                            <input type="text" class="form-control fecha" id="FechaDiaFestivo${DiaFestivo.idDiaFestivo}" value="${FechaFormateada}" readonly>
                            <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                            <small id="EFecha${DiaFestivo.idDiaFestivo}" class="etiquetaError form-text form-text-error"></small>
                        </div>
                    </td>
                    <td><input type="text" class="form-control" id="DescripcionDiaFestivo${DiaFestivo.idDiaFestivo}" value="${DiaFestivo.descripcion}" readonly></td>
                    <td><button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar${DiaFestivo.idDiaFestivo}" onclick="editar_aceptar('${DiaFestivo.idDiaFestivo}')">Editar</button></td>
                    <td><button type="button" class="btn btn-primary oculta-empleado" id="Cancelar${DiaFestivo.idDiaFestivo}" onclick="cancelar('${DiaFestivo.idDiaFestivo}', '${FechaFormateada}', '${DiaFestivo.descripcion}')" style="display: none;">Cancelar</button></td>
                </tr>
                `
                $("#TabDiasFestivos tbody").append(text);
            });
        }
    });
}

function editar_aceptar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        $("#FechaDiaFestivo" + data).attr("readonly", false);
        $("#FechaDiaFestivo" + data).datepicker("option", "disabled", false);
        $("#DescripcionDiaFestivo" + data).attr("readonly", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_diafestivo(data);
    }
}

function cancelar(data1, data2, data3){
    $("#FechaDiaFestivo" + data1).attr("readonly", true);
    $("#FechaDiaFestivo" + data1).datepicker("option", "disabled", true);
    $("#DescripcionDiaFestivo" + data1).attr("readonly", true);

    $("#FechaDiaFestivo" + data1).val(data2);
    $("#DescripcionDiaFestivo" + data1).val(data3);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_diasfestivos(dato){
    datos = {};
    datos["idDiaFestivo"] = dato;
    var Fecha_string = $("#FechaDiaFestivo" + dato).val();
    datos["fecha"] = convertirFechaParaEnvio(Fecha_string);
    datos["descripcion"] = $("#DescripcionDiaFestivo" + dato).val();
    datos = JSON.stringify(datos);

    $.ajax({
        async: false,
        type: "POST",
        url: "/Catalogos/guardar_diasfestivos",
        data: datos,
        success: function(data){
            if(data.guardado){
                abrirModal("Información guardada", "Los datos de Días Festivos se guardaron correctamente.", "recargar");
            }
        }
    });
}