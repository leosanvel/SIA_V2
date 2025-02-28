$gmx(document).ready(function(){
    inicializar_anio();
    obtener_quincenas();
    $("#btnGenerarReporte").click(generar_reporte);
    $("#Movimiento").change(function(){
        sel_alta_o_baja();
        obtenerInformacionPrevia();
    });
    $("#Periodo").change(function(){
        obtener_quincenas();
        obtenerInformacionPrevia();
    });
    $("#Quincena").change(function(){
        obtenerInformacionPrevia();
    });
    $("#TipoEmpleado").change(function(){
        obtenerInformacionPrevia();
    });

    $(".filtro-col").on("keyup", function(){
        BuscarEnTabla($(this));
    })
});

function inicializar_anio(){
    var hoy = new Date();
    var anio = hoy.getFullYear();
    $("#Periodo").val(anio);
}

function obtener_quincenas(){
    AnioFiscal = $("#Periodo").val();
    if($("#Periodo").val != ""){
        $.ajax({
            type: "POST",
            url: "/rh/reportes/por-movimientos/obtener-quincenas",
            data: {
                AnioFiscal: AnioFiscal
            },
            success: function(data){
                if(data.length > 0){
                    $("EQuincena").text("");
                    $("#Quincena").find('option').not(':first').remove();
                    data.forEach(function(Quincena){
                        $("#Quincena").append(new Option(Quincena.Descripcion, Quincena.idQuincena));
                    });
                }else{
                    $("EQuincena").text("No hay quincenas disponibles.");
                }
            }
        });
    }
}

function obtenerInformacionPrevia(){
    Periodo = $("#Periodo").val();
    Quincena = $("#Quincena").val();
    Movimiento = $("#Movimiento").val();
    TipoEmpleado = $("#TipoEmpleado").val();

    if(Periodo != "0" && Quincena != "0" && Movimiento != "0" && TipoEmpleado != "0"){
        $.ajax({
            type: "POST",
            url: "/rh/reportes/por-movimientos/obtener-informacion-movimientos",
            data: $("#formularioPorMovimientos, #idPersona").serialize(),
            success: function(data){
                if(data.length > 0){
                    console.log(data);
                    $("#EResultadoInformacionPrevia").text("");
                    // Muestra la tabla existente
                    $("#TablaResultadosMovimientos").show();
                    // Limpiar la tabla existente
                    $("#TablaResultadosMovimientos tbody").empty();
                    // Iterar sobre los incidencias y agregar filas a la tabla
                    var cont = 1;
                    data.forEach(function(Movimiento){
                        // Agregar información a cada fila de la tabla
                        var FechaEfecto = convertirFechaParaVisualizacion(Movimiento.FechaEfecto);
                        text = `
                            <tr>
                                <td>
                                    <input type="text" id="NumEmpleado${cont}" class="form-control" value="${Movimiento.NumEmpleado}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="RFC${cont}" class="form-control" value="${Movimiento.RFC}" style="width: 170px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="CURP${cont}" class="form-control" value="${Movimiento.CURP}" style="width: 230px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="Nombre${cont}" class="form-control" value="${Movimiento.Nombre}" style="width: 370px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="NumMovimiento${cont}" class="form-control" value="${Movimiento.NumMovimiento}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="Movimiento${cont}" class="form-control" value="${Movimiento.Movimiento}" style="width: 50px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="Plaza${cont}" class="form-control" value="${Movimiento.Plaza}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="NumPlaza${cont}" class="form-control" value="${Movimiento.NumPlaza}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="Nivel${cont}" class="form-control" value="${Movimiento.NivelSalarial}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="CCOrigen${cont}" class="form-control" value="${Movimiento.CCOrigen}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="TipoPlaza${cont}" class="form-control" value="${Movimiento.TipoPlaza}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="Puesto${cont}" class="form-control" value="${Movimiento.Puesto}" style="width: 300px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="FechaEfecto${cont}" class="form-control" value="${FechaEfecto}" style="width: 130px;" readonly>
                                </td>
                                <td>
                                    <input type="text" id="CCPropuesto${cont}" class="form-control" value="${Movimiento.CCPropuesto}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <textarea rows="2" id="CentroCosto${cont}" class="form-control" style="resize: none;width: 300px;" readonly>${Movimiento.CentroCosto}</textarea>
                                </td>
                                <td>
                                    <textarea rows="2" id="Causabaja${cont}" class="form-control" style="resize: none;width: 300px;" readonly>${Movimiento.CausaBaja}</textarea>
                                </td>
                                <td>
                                    <input type="text" id="Grupo${cont}" class="form-control" value="${Movimiento.Grupo}" style="width: 75px;" readonly>
                                </td>
                                <td>
                                    <textarea rows="2" id="Observaciones${cont}" class="form-control" style="resize: none;width: 150px;" readonly>${Movimiento.Observaciones}</textarea>
                                </td>
                            <tr>
                        `;
                        $("#TablaResultadosMovimientos tbody").append(text);
                    });
                }else{
                    $("#TablaResultadosMovimientos tbody").empty();
                    $("#TablaResultadosMovimientos").hide();
                    $("#EResultadoInformacionPrevia").text("No se encontraron coincidencias");
                }
            }
        });
    }
}

function BuscarEnTabla(columna){
    //var IndiceColumna = columna.data("col");
    //var Filtro = columna.val().toUpperCase();

    $("#TablaResultadosMovimientos tbody tr").each(function(){
        var Fila = $(this);
        var MostrarFila = true;
        //var Celda = $(this).find("td").eq(IndiceColumna).find("input");

        $(".filtro-col").each(function(){
            var Columna = $(this);
            var IndiceColumna = Columna.data("col");
            var Filtro = Columna.val().toUpperCase().trim();

            if(Filtro !== ""){
                var Celda = Fila.find("td").eq(IndiceColumna).find("input");
                var ValorCelda = Celda.length > 0
                    ? Celda.val().toUpperCase()
                    : Fila.find("td").eq(IndiceColumna).text().toUpperCase();

                if(ValorCelda.indexOf(Filtro) === -1){
                    MostrarFila = false;
                }
            }
        });
        Fila.toggle(MostrarFila);
        // if(Celda.length > 0){
        //     var ValorCelda = Celda.val().toUpperCase();
        //     $(this).toggle(ValorCelda.indexOf(Filtro) > -1);
        // }
    });
}

function generar_reporte(){
    if(validarFormulario($("#formularioPorMovimientos")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/reportes/generar_reporte_por_movimiento",
            data: $("#formularioPorMovimientos, #idPersona").serialize(),
            success: function(data){
                if(data.respuesta){
                    var urlDescarga = data.url_descarga;
                    $("#btnDescargarReporte").show();
                    $("#btnDescargarReporte").wrap('<a href="' + urlDescarga + '" download></a>');
                    abrirModal("Reporte generado", `El reporte ha sido creado correctamente`, "");
                }
                else{
                    abrirModal("Reporte no generado", `No existen movimientos`, "");
                    $("#btnDescargarReporte").hide();
                    $('#btnDescargarReporte').unwrap();
                }
            }
        });
    }
}

function sel_alta_o_baja(){
    if($("#Movimiento").val() == "1" || $("#Movimiento").val() == "2"){
        $("#NumEmpleado").show();
        $("#NumEmpleado").val("");
    }else{
        $("#NumEmpleado").hide();
        $("#NumEmpleado").val("");
    }
}