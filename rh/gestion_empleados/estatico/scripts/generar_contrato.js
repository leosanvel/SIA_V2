$gmx(document).ready(function(){
    var TodosSeleccionados = false;
    //$("#btnGenerarContrato").click(generar_contrato);
    $("#btnConfirmarContrato").click(obtenerDatosContrato);
    $("#btnGuardarContrato").click(Guardar);
    $("#btnGenerarContrato").click(ProcesandoGenerarContrato);

    $("#btnBusqueda").click(cargarEmpleadosHonorarios);

    $("#btnGenerarContratosMasivos").click(function(){
        enviarListaEmpleados();
    });

    $("#btnSeleccionarTodo").click(function(){
        TodosSeleccionados = SeleccionarTodosCheckbox(TodosSeleccionados);
    });

    $("#FechaInicioBusqueda").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true
    });

    $("#FechaFinBusqueda").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true
    });
});

function generar_contrato(){
    //event.preventDefault();
    window.document.getElementById("btnGenerarContrato").disabled = "";
    $.ajax({
        async: false,
        type: "POST",
        url: "/RH/generarContrato",
        data: $("#idPersona, #formularioModificarContrato").serialize(),
        success: function(data){
            window.document.getElementById("ImgModal").style.display = "none";
            if(data.generado){
                abrirModal("Contrato Generado", "Contrato generado de forma correcta", "");
            }
            
            var urlDescarga = data.url_descarga;
            $("#btnDescargaContrato").show();
            $("#btnDescargaContrato").wrap('<a href="' + urlDescarga + '"download></a>');
        }
    });
}

function cargarEmpleadosHonorarios(){
    texto_busqueda = $("#Busqueda").val();
    FechaInicio = $("#FechaInicioBusqueda").val();
    FechaFin = $("#FechaFinBusqueda").val();
    if(texto_busqueda != "" || FechaInicio != "" || FechaFin != ""){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/generar-contratos-masivo/busqueda-empleados",
            data: {
                "Busqueda": texto_busqueda,
                "FechaInicio": FechaInicio,
                "FechaFin": FechaFin
            },
            success: function(data){
                if(data){
                    if(data.lista_empleados.length > 0){
                        $("#EResultado").text("");
                        $("#tablaEmpleadosHonorariosActivos").show();
                        // Limpiar la tabla existente
                        $("#tablaEmpleadosHonorariosActivos tbody").empty();

                        data.lista_empleados.forEach(function(Empleado){
                            FechaInicio = convertirFechaParaVisualizacion(Empleado.FechaInicio);
                            FechaFin = convertirFechaParaVisualizacion(Empleado.FechaFin);
                            ColumnaDescarga = "";
                            if(Empleado.ContratoGenerado){
                                ColumnaDescarga = `<button type="button" id="DescargaContrato${Empleado.idPersona}"><span class="bootstrap-icons" aria-hidden="true"><i class="bi bi-file-earmark-pdf"></i></span></button>`;
                            }
                            text = `
                                <tr>
                                    <td>
                                        <input type="checkbox" id="check${Empleado.idPersona}" class="checkbox-empleado" style="width: 50px;">
                                    </td>
                                    <td>
                                        <button type="button" id="btnEditarContrato${Empleado.idPersona}"       onclick="obtenerDatosContrato(${Empleado.NumEmpleado}, ${Empleado.NumeroContrato})">
                                            <span class="glyphicon glyphicon-edit" aria-hidden="true"></span>
                                        </button>
                                    </td>
                                    <td>
                                        <input type="text" class="form-control numero-empleado" id="NumEmpleado${Empleado.idPersona}" value="${Empleado.NumEmpleado}" readonly style="width: 100px;">
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" id="Nombre${Empleado.idPersona}" value="${Empleado.Nombre}" readonly style="width: 500px;">
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" id="FechaInicio${Empleado.idPersona}" value="${FechaInicio}" readonly style="width: 150px">
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" id="FechaFin${Empleado.idPersona}" value="${FechaFin}" readonly style="width: 150px">
                                    </td>
                                    <td>
                                        <input type="text" class="form-control" id="CentroCosto${Empleado.idPersona}"   value="${Empleado.CentroCosto}" readonly style="width: 100px;">
                                    </td>
                                    <td>
                                        ${ColumnaDescarga}
                                    </td>
                                    <input type="hidden" id="idPersona${Empleado.idPersona}" class="idPersona-empleado" value="${Empleado.idPersona}">
                                    <input type="hidden" id="NumeroContrato${Empleado.idPersona}" class="numero-contrato" value="${Empleado.NumeroContrato}">
                                    <input type="hidden" id="ContratoGenerado${Empleado.idPersona}" class="contrato-generado" value="${Empleado.ContratoGenerado}">
                                </tr>
                            `;
                            $("#tablaEmpleadosHonorariosActivos tbody").append(text);
                            if(Empleado.ContratoGenerado){
                                $(`#DescargaContrato${Empleado.idPersona}`).wrap('<a href="' + Empleado.url_descarga + '"download></a>');
                            }
                        });
                        $("#btnSeleccionarTodo").show();
                        $("#btnGenerarContratosMasivos").show();
                    }else{
                        $("#EResultado").text("No se encontraron coincidencias.");
                        $("#tablaEmpleadosHonorariosActivos").hide();
                        // Limpiar la tabla existente
                        $("#tablaEmpleadosHonorariosActivos tbody").empty();
                        $("#btnSeleccionarTodo").hide();
                        $("#btnGenerarContratosMasivos").hide();
                    }
                }
            }
        });
    }else{
        abrirModal("Campos vacíos", "Escriba información a buscar en alguno de los campos disponibles", "");
    }
}

function enviarListaEmpleados(){
    var listaEmpleados = [];
    var listaNumeroContrato = [];

    $(".checkbox-empleado:checked").each(function(){
        // Obtener idPersona del empleado marcado
        let idPersona = $(this).closest('tr').find('.idPersona-empleado').val();
        let NumeroContrato = $(this).closest('tr').find('.numero-contrato').val();
        let ContratoGenerado = $(this).closest('tr').find('.contrato-generado').val();

        //Agregar el idPersona a la lista
        if(ContratoGenerado == 0){
            listaEmpleados.push(idPersona);
            listaNumeroContrato.push(NumeroContrato);
        }else{
            abrirModal("Ya se ha creado un contrato", "El contrato de un registro ya se ha generado. Se generarán los demás contratos que no existan.", "");
        }
    });

    if(listaEmpleados.length != 0 && listaNumeroContrato.length != 0){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/generar-contratos-masivo",
            contentType: "application/json",
            data: JSON.stringify({ListaEmpleados: listaEmpleados, ListaNumeroContrato: listaNumeroContrato}),
            success: function(data){
                if(data.respuesta == 99){
                    abrirModal("Contrato(s) generado(s)", "Los contratos se han generado de manera correcta.", "recargar");
                }
            }
        });
    }else{
        abrirModal("Registros no seleccionados", "No se ha seleccionado un registro para generar contrato. Verifique la selección de registros.", "");
    }
}

function SeleccionarTodosCheckbox(TodosSeleccionados){
    TodosSeleccionados = !TodosSeleccionados;
    $(".checkbox-empleado").prop("checked", TodosSeleccionados);

    return TodosSeleccionados;
}

function ProcesandoGenerarContrato(){
    $("#btnDescargaContrato").hide();
    $("#ModalModificarContrato").modal("hide");
    window.document.getElementById("btnGenerarContrato").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generar_contrato, 2000);
}

function modal_modificar_contrato(){
    $("#ModalModificarContrato").modal("show");
    $("#FechaInicio").blur(ValidarContratos)
    $("#FechaInicio").datepicker({ dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,
        beforeShow: function(){
            setTimeout(function(){
                $(".ui-datepicker").css("z-index", 99999);
            }, 0);
        }
    });
    $("#FechaFin").datepicker({ dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,
        beforeShow: function(){
            setTimeout(function(){
                $(".ui-datepicker").css("z-index", 99999);
            }, 0);
        }
    });
    $("#FechaFirma").datepicker({ dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,
        beforeShow: function(){
            setTimeout(function(){
                $(".ui-datepicker").css("z-index", 99999);
            }, 0);
        }
    });
    //obtenerDatosContrato();
}

function Guardar(){
    if(validarFormulario($("#formularioModificarContrato")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/guardar_empleado_contrato",
            data: $("#formularioModificarContrato, #idPersona, #NumeroContrato").serialize(),
            success: function(data){
                alert(data.respuesta);
            }
        });
    }
}

function ValidarContratos(){
    $("#FechaFirma").val($("#FechaInicio").val());
}

function obtenerDatosContrato(NumeroEmpleado, NumeroContrato){
    //let NumeroEmpleado = $(".numero-empleado").map(function(){
        //return $(this).val();
    //}).get();
    console.log(NumeroContrato);
    if(NumeroEmpleado != null){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/validar_empleado_contrato",
            data: {
                "NumeroBuscarEmpleado": NumeroEmpleado,
                "NumeroContrato": NumeroContrato
            },
            success: function(data){
                console.log(data);
                if(data.respuesta == 0){
                    resultadobusqueda("alert alert-danger","El empleado no existe.<br />No se puede generar contrato.");
                }else{
                    if(data.respuesta == 1){
                        resultadobusqueda("alert alert-warning","El empleado se encuentra inactivo.<br />No se puede generar    contrato.");
                    }else{
                        if(data.respuesta == 2){                 
                            resultadobusqueda("alert alert-warning","El empleado es de plaza.<br />No se puede generar  contrato.");
                        }else{
                            if(data.respuesta == 99){
                                if(data.DatosContrato != null){
                                    modal_modificar_contrato();
                                    FechaInicio = convertirFechaParaVisualizacion(data.DatosContrato.FechaInicio);
                                    FechaFin = convertirFechaParaVisualizacion(data.DatosContrato.FechaFin);
                                    FechaFirma = convertirFechaParaVisualizacion(data.DatosContrato.FechaFirma);
                                    window.document.getElementById("strMensaje").className = ""; 
                                    window.document.getElementById("strMensaje").innerHTML = "";
                                    $("#strMensaje").hide();
                                    $("#FechaInicio").val(FechaInicio);
                                    $("#FechaFin").val(FechaFin);
                                    $("#FechaFirma").val(FechaFirma);
                                    $("#Estado").val(data.DatosContrato.idEstado);
                                    $("#Municipio").val(data.DatosContrato.idMunicipio);
                                    $("#ImporteBruto").val(data.DatosContrato.ImporteBruto);
                                    $("#NumeroExhibiciones").val(data.DatosContrato.NumeroExhibicion);
                                    $("#MontoPactado").val(data.DatosContrato.MontoPactado);
                                    $("#Proyecto").val(data.DatosContrato.Proyecto);
                                    $("#Partida").val(data.DatosContrato.Partida);
                                    $("#Origen").val(data.DatosContrato.Origen);
                                    $("#ConocimientoPrestador").val(data.DatosContrato.ConocimientoPrestador);
                                    $("#OficioDictamen").val(data.DatosContrato.OficioDictamen);
                                    $("#ConocimientoExperiencia").val(data.DatosContrato.ConocimientoExperiencia);
                                    $("#Actividades").val(data.DatosContrato.Actividades);
                                    $("#CURPEntregable").val(data.DatosContrato.CURPEntrega);
                                    $("#CURPFirma").val(data.DatosContrato.CURPFirma);
                                    $("#idPersona").val(data.DatosContrato.idPersona);
                                }else{
                                    resultadobusqueda("alert alert-warning","No hay datos de contrato para el empleado.<br />No se puede generar  contrato.");
                                }
                            }
                        }
                    }
               }
            }
        });
    }
}

function resultadobusqueda(strClase, strMensaje){
    $("#frmCrearContrato").hide();
    //window.document.getElementById("NumeroBuscarEmpleado").value = "";
    window.document.getElementById("strMensaje").className = strClase; 
    window.document.getElementById("strMensaje").innerHTML = strMensaje;
    $("#strMensaje").show();
}