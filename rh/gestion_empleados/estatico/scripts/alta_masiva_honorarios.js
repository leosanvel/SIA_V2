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
});

function cargarEmpleadosHonorariosInactivos(){
    texto_busqueda = $("#Busqueda").val();
    if(texto_busqueda != ""){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/buscar-empleados-honorarios",
            data : {
                "Busqueda": texto_busqueda
            },
            success: function(data){
                if(data.length > 0){
                    $("#EResultado").text("");
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
                }
            }
        });
    }else{
        $("#EResultado").text("No se encontraron resultados.");
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
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/generar-bajas-altas-masivo-honorarios",
            contentType: 'application/json',
            data: JSON.stringify({ ListaEmpleados: listaEmpleados }),
            success: function(data){
                abrirModal("Baja/Alta de empleado", "La baja y alta del(os) empleado(s) se realizó de manera correcta.", "");
            }
        });
    }
}

function SeleccionarTodosCheckbox(TodosSeleccionados){
    TodosSeleccionados = !TodosSeleccionados;
    $(".checkbox-empleado").prop("checked", TodosSeleccionados);

    return TodosSeleccionados;
}