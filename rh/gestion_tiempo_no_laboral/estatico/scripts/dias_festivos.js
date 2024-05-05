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
                                <td>${FechaFormateada}</td>
                                <td>${festividad.Descripcion}</td>
                                <td>${FechaCreacionFormateada}</td>
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
