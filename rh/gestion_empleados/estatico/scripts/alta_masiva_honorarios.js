$gmx(document).ready(function(){
    var TodosSeleccionados = false;

    $("#btnBusqueda").click(function(){
        cargarEmpleadosHonorariosInactivos();
    });
    
    $("#btnGenerarAltas").click(function(){
        enviarListaEmpleados();
    });

    $("#btnSeleccionarTodo").click(function(){
        TodosSeleccionados = SeleccionarTodosCheckbox(TodosSeleccionados);
    });

    mostrarFechas();

    $("#Opcion").change(function(){
        mostrarFechas();
    });

    $("#FechaInicio").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true
    });

    $("#FechaFin").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true
    });
});

function cargarEmpleadosHonorariosInactivos(){
    var texto_busqueda = $("#Busqueda").val();
    var opcion = $("#Opcion").val();
    if(texto_busqueda != ""){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/buscar-empleados-honorarios",
            data : {
                "Busqueda": texto_busqueda,
                "Opcion": opcion
            },
            success: function(data){
                if(data.length > 0){
                    $("#EBusqueda").text("");
                    $("#EResultadoEmpleadosHonorarios").text("");
                    $("#tablaEmpleadosHonorariosInactivos").show();
                    // Limpiar la tabla existente
                    $("#tablaEmpleadosHonorariosInactivos tbody").empty();

                    data.forEach(function(Empleado){
                        text = `
                            <tr>
                                <td>
                                    <input type="checkbox" id="check${Empleado.idPersona}" class="checkbox-empleado"    style="width: 50px;">
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="NumEmpleado${Empleado.idPersona}" value="${Empleado.NumEmpleado}" readonly style="width: 100px;">
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="Nombre${Empleado.idPersona}" value="${Empleado.Nombre}" readonly style="width: 500px;">
                                </td>
                                <td>
                                    <input type="hidden" id="idPersona${Empleado.idPersona}" class="idPersona-empleado" value="${Empleado.idPersona}">
                                </td>
                            </tr>
                        `;
                        $("#tablaEmpleadosHonorariosInactivos tbody").append(text);
                    });
                    $("#btnSeleccionarTodo").show();
                    $("#btnGenerarAltas").show();
                }else{
                    $("#tablaEmpleadosHonorariosInactivos tbody").empty();
                    $("#tablaEmpleadosHonorariosInactivos").hide();
                    $("#btnSeleccionarTodo").hide();
                    $("#btnGenerarAltas").hide();
                    $("#EResultadoEmpleadosHonorarios").text("No se encontraron resultados.");
                }
            }
        });
    }else{
        $("#EBusqueda").text("Campo vacío. Agregue información.");
    }
}

function enviarListaEmpleados(){
    var listaEmpleados = [];

    $(".checkbox-empleado:checked").each(function(){
        // Obtener idPersona del empleado marcado
        let idPersona = $(this).closest('tr').find('.idPersona-empleado').val();
        console.log(idPersona);

        //Agregar el idPersona a la lista
        listaEmpleados.push(idPersona);
    });

    if(listaEmpleados.length != 0){
        if(validarFormulario($("#formularioAltaMasivoHonorarios")).valido){
            var Option = $("#Opcion").val();
            var FechaInicio = $("#FechaInicio").val();
            var FechaFin = $("#FechaFin").val();
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-empleados/generar-bajas-altas-masivo-honorarios",
                contentType: 'application/json',
                data: JSON.stringify({ ListaEmpleados: listaEmpleados, 
                    Opcion: Option,
                    FechaInicio: FechaInicio,
                    FechaFin: FechaFin
                }),
                success: function(data){
                    if(Option == "1"){
                        abrirModal("Baja/Alta de empleado(s)", "La alta y baja del(os) empleado(s) se realizó de manera     correcta.", "recargar");
                    }else{
                        abrirModal("Baja de empleado", "La baja del(os) empleado(s) se realizó de manera correcta.",    "recargar");
                    }
                }
            });
        }
    }else{
        abrirModal("No hay empleados seleccionados", "Seleccione uno o más empleados para generar la alta/baja masiva.", "");
    }
}

function SeleccionarTodosCheckbox(TodosSeleccionados){
    TodosSeleccionados = !TodosSeleccionados;
    $(".checkbox-empleado").prop("checked", TodosSeleccionados);

    return TodosSeleccionados;
}

function mostrarFechas(){
    var opcion = $("#Opcion").val();
    if(opcion == "1"){
        $("#Fechas").show();
        $("#FechaInicio").addClass("obligatorio");
        $("#FechaFin").addClass("obligatorio");
    }else{
        $("#Fechas").hide();
        $("#FechaInicio").removeClass("obligatorio");
        $("#FechaFin").removeClass("obligatorio");
    }
}