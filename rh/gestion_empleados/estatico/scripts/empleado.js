function seleccionaEmpleado(idPersona) {
    $.ajax({
        type: "POST",
        url: "/rh/gestion-empleados/selecciona-empleado",
        data: { "idPersona": idPersona },
        success: function (data) {
            if (data) {
                var path = window.location.pathname;
                if (path === "/rh/gestion-empleados/busqueda-empleado") {
                    window.location.href = "/rh/gestion-empleados/modificar-empleado"
                } else {
                    
                    // resetearTodosLosFormularios();
                    $("#tablaEmpleadoSeleccionado").show();

                    $("#idPersona").val(data.idPersona);
                    $("#NumeroEmpleado").text(data.NumeroEmpleado);

                    $("#NumeroEmpleadoSeleccionado").val(data.NumeroEmpleado);
                    $("#NumeroBuscarEmpleado").val(data.NumeroEmpleado);

                    $("#CurpEmpleado").text(data.CURP);
                    $("#NombreEmpleado").text(data.Nombre);
                    $("#ApellidosEmpleado").text(data.ApPaterno + ' ' + data.ApMaterno);
                    $('#ModalBuscaEmpleado').modal('hide');

                    $("#tablaResultadosJustificantes tbody").empty();
                    $("#tablaResultadosJustificantes").hide();

                    $("#tablaResultadosPolitica tbody").empty();
                    $("#tablaResultadosPolitica").hide();
                    $("#btnGuardaPoliticaPersona").hide();

                    $("#ResultadoPuesto").hide();

                    if (typeof funcionSeleccionar === 'function') {
                        // Ejecutar la función
                        funcionSeleccionar();
                    }

                }
            }
        }
    });
}

function resetearTodosLosFormularios() {
    // Selecciona todos los formularios en la página
    var formularios = $("form");
    // Recorre cada formulario y llama a la función reset() para restablecerlo
    formularios.each(function () {
        this.reset();
    });
}

function buscarCP(idTipoDomicilio) {
    $("#spinnerCP" + idTipoDomicilio).show();

    if (idTipoDomicilio == 1) {
        var formulario = "#formularioDomicilioParticular";
    } else {
        var formulario = "#formularioDomicilioFiscal";
    }

    var cpElement = $(formulario).find("#BCP"); // Selecciona el campo CP dentro del formulario
    if (cpElement.val() != "") {
        $.ajax({
            type: "POST",
            url: "/rh/gestion-empleados/buscar-cp",
            data: {
                "CP": $(formulario).find("#BCP").val(),
            },
            success: function (data) {
                if (data == "no encontrado") {
                    $(formulario).find("#EBCP").text("Código Postal no encontrado");
                } else {
                    $(formulario).find("#Entidad").val(data.idEntidad);
                    cargarMunicipio(idTipoDomicilio);
                    $(formulario).find("#Municipio").val(data.idMunicipio);
                    cargarLocalidad(idTipoDomicilio);
                    $(formulario).find("#TipoAsentamiento").val(data.idTipoAsentamiento);
                    cargaAsentamiento(idTipoDomicilio);
                    $(formulario).find("#Asentamiento").val(data.idAsentamiento);
                    $(formulario).find("#EBCP").text("");
                    $(formulario).find("#Asentamiento").trigger("change");
                }
            },
            complete: function () {
                $("#spinnerCP" + idTipoDomicilio).hide();
            }
        });
    } else {
        $("#spinnerCP" + idTipoDomicilio).hide();
    }
}

function abrirPestana(tabId) {
    // Utiliza código para activar la pestaña correspondiente
    var tabElement = document.getElementById(tabId);
    if (tabElement) {
        $('#' + tabId).tab('show');
        window.scrollTo(0, 0);
    }
}
function guardarDomicilio(idTipoDomicilio, formulario) {
    var formData = new FormData(formulario[0]);
    formData.append("idTipoDomicilio", idTipoDomicilio);
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/guardar-direccion",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) { }
    });
}

function guardarDatosBancarios(formulario){
    var formData = new FormData(formulario[0]);
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/guardar-datos-bancarios",
        data: formData,
        enctype: 'multipart/form-data',
        contentType: false,
        processData: false,
        success: function(data){ }
    });
}

function agregarConceptos(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/agregar-conceptos",
        success: function(data){ }
    })
}

$gmx(document).ready(function () {
    $("#btnBuscaEmpleado").click(function (event) {
        event.preventDefault();
        if (validarFormulario($("#frmBuscarEmpleado")).valido) {
            $.ajax({
                type: "POST",
                url: "/rh/gestion-empleados/buscar-empleado",
                data: $("#frmBuscarEmpleado").serialize(),
                success: function (data) {
                    if (data.length > 0) {
                        $("#tablaEmpleados").show();

                        // Limpiar la tabla existente
                        $("#tablaEmpleados tbody").empty();

                        // Iterar sobre los empleados y agregar filas a la tabla
                        data.forEach(function (empleado) {
                            $("#tablaEmpleados tbody").append(`
                                <tr>
                                <td>
                                    <button onclick="seleccionaEmpleado(${empleado.idPersona})" class="btn btn-primary btn-sm boton-seleccionar">Sel.</button>
                                </td>
                               <td >${empleado.NumeroEmpleado}</td>
                                <td >${empleado.CURP}</td>
                                <td >${empleado.Nombre}</td>
                                <td >${empleado.ApPaterno} ${empleado.ApMaterno}</td>
                                </tr>
                            `);
                        });
                    } else {
                        $("#EParametro").text("Empleado no encontrado");
                        $("#tablaEmpleados").hide();
                    }
                }
            });
        }
    });

    $("#botonGuardarEmpleado").click(function (event) {
        let mensajeError = '';
        let mensajeGuardado = '';
        var validacionExitosa = true;
        if (!validarFormulario($("#formularioDatosPersonales")).valido) {
            mensajeError += '<a href="javascript:void(0);" onclick="abrirPestana(\'tab-DatosPersonales\')">-Datos personales</a>. <br>';
            validacionExitosa = false;
        }
        if (!validarFormulario($("#formularioDatosEmpleado")).valido) {
            mensajeError += '<a href="javascript:void(0);" onclick="abrirPestana(\'tab-DatosEmpleado\')">-Datos empleado</a>. <br>';
            validacionExitosa = false;
        }
        if (!validarFormulario($("#formularioEscolaridad")).valido) {
            mensajeError += '<a href="javascript:void(0);" onclick="abrirPestana(\'tab-Escolaridad\')">-Escolaridad</a>. <br>';
            validacionExitosa = false;
        }

        validarFormulario($("#formularioDatosBancarios"));

        if (validacionExitosa) {

            var FechaNacimiento_string = $("#FechaNacimiento").val();
            var FecIngresoGob_string = $("#FecIngresoGob").val();
            var FecIngreso_string = $("#FecIngreso").val();

            var FechaNacimiento = convertirFechaParaEnvio(FechaNacimiento_string);
            var FecIngresoGob = convertirFechaParaEnvio(FecIngresoGob_string);
            var FecIngreso = convertirFechaParaEnvio(FecIngreso_string);
            // Agrega las fechas al formulario

            $("#formularioDatosPersonales input[name='FechaNacimiento_format']").remove();
            $("#formularioDatosEmpleado input[name='FecIngresoGob_format']").remove();
            $("#formularioDatosEmpleado input[name='FecIngreso_format']").remove();

            $("#formularioDatosPersonales").append('<input type="hidden" name="FechaNacimiento_format" value="' + FechaNacimiento + '">');
            $("#formularioDatosEmpleado").append('<input type="hidden" name="FecIngresoGob_format" value="' + FecIngresoGob + '">');
            $("#formularioDatosEmpleado").append('<input type="hidden" name="FecIngreso_format" value="' + FecIngreso + '">');

            const formDatosPersonales = new FormData($("#formularioDatosPersonales")[0]);
            const formDatosEmpleado = new FormData($("#formularioDatosEmpleado")[0]);
            const formEscolaridad = new FormData($("#formularioEscolaridad")[0]);
            //const formDatosBancarios = new FormData($("#formularioDatosBancarios")[0]);
            //const formularioEstatus = new FormData($("#formularioEstatus")[0]);

            const FormularioCompleto = new FormData();
            for(const[key, value] of [...formDatosPersonales.entries(), ...formDatosEmpleado.entries(), ...formEscolaridad.entries()]){
                FormularioCompleto.append(key, value);
            }

            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-empleados/guarda-empleado",
                data: FormularioCompleto,
                enctype: 'multipart/form-data',
                contentType: false,
                processData: false,
                success: function (data) {
                    
                    if (data.guardado) {
                        // abrirModal("Información guardada", "Los datos personales, de empleado y de escolaridad han sido actualizados correctamente en la base de datos.", "");
                        mensajeGuardado += "-Datos personales.<br>";
                        mensajeGuardado += "-Datos de empleado.<br>";
                        mensajeGuardado += "-Datos de escolaridad.<br>";
                        if(data.NumeroEmpleado){
                           mensajeGuardado += "-El número de Empleado asignado es" + data.NumeroEmpleado;
                        }
                        if (data.correo_enviado) {
                            mensajeGuardado += "<br>";
                            mensajeGuardado += "Una notificación ha sido enviada vía correo electrónico.<br>";
                        }

                    }
                    if(data.existe_clabe){
                        mensajeGuardado += "-No se guardó la Clabe interbancaria porque ya hay una activa.";
                    }
                }
            });
        }
        if (!formularioVacio($("#formularioDomicilioParticular"))) {
            if (validarFormulario($("#formularioDomicilioParticular")).valido) {
                guardarDomicilio(1, $("#formularioDomicilioParticular"));
                mensajeGuardado += "-Domicilio particular. <br>"
            } else {
                mensajeError += '<a href="javascript:void(0);"  onclick="abrirPestana(\'tab-DomicilioParticular\')">-Domicilio particular</a>. <br>';
            }
        }

        let formulario = "#formularioDomicilioFiscal";
        if ($("#mismoDomicilio").prop("checked")) {
            formulario = "#formularioDomicilioParticular";
        }

        if (!formularioVacio($(formulario))) {
            if (validarFormulario($(formulario)).valido) {
                guardarDomicilio(2, $(formulario));
                mensajeGuardado += "-Domicilio Fiscal. <br>"
            } else {
                mensajeError += '<a href="javascript:void(0);" onclick="abrirPestana(\'tab-DomicilioFiscal\')">-Domicilio fiscal</a>. <br>';
            }
        }

        if(!formularioVacio($("#formularioDatosBancarios"))){
            
            if(validarFormulario($("#formularioDatosBancarios")).valido){
                guardarDatosBancarios($("#formularioDatosBancarios"))
            }
        }
        var path = window.location.pathname;
        if (path === "/rh/gestion-empleados/agregar-empleado") {
            agregarConceptos();
        }
        //Recorremos formularios para validar y mostrar el primer error
        var formularios = [
            $("#formularioDomicilioFiscal"),
            $("#formularioDomicilioParticular"),
            $("#formularioEscolaridad"),
            $("#formularioDatosEmpleado"),
            $("#formularioDatosPersonales"),
        ];
        let hayCamposOpcionales = false;
        formularios.forEach(function (formulario) {
            if ((formulario[0].id !== "formularioDomicilioFiscal" && formulario[0].id !== "formularioDomicilioParticular") || !formularioVacio(formulario)) {
                validarFormulario(formulario);
                if (validarFormulario(formulario).camposOpcionales)
                    hayCamposOpcionales = true;
            }
        });
        // Mostramos liste de errores 
        if (mensajeError !== '') {
            $("#AlertaError").html(`<strong>Error:</strong> Por favor verifique la siguiente información:<br> ${mensajeError}`);
            $("#AlertaError").show();
        }
        else {
            $("#AlertaError").hide();
            if (hayCamposOpcionales) {
                abrirModal("Información guardada", `
                <strong>AVISO:</strong> Algunos campos están vacíos, sin embargo,
                la información principal se ha guardado correctamente.
                Puedes añadir la información faltante más tarde.
                <br> <br> La siguiente información ha sido guardada correctamente:<br> ${mensajeGuardado}`, "");
            } else {
                abrirModal("Información guardada", `La siguiente información ha sido guardada correctamente:<br> ${mensajeGuardado}`, "");
            }
        }



    });

    $("#btnBuscarCurp").click(function (event) {
        event.preventDefault();
        if (validarFormulario($("#frmBuscarCURP")).valido) {
            $("#spinnerCURP").show();
            $.ajax({
                // async: false,
                type: "POST",
                url: "/rh/gestion-empleados/buscar-curp",
                data: $("#frmBuscarCURP").serialize(),
                success: function (data) {
                    $("#spinnerCURP").hide();
                    $('#formularioDatosPersonales')[0].reset();
                    $('#formularioDatosEmpleado')[0].reset();
                    $('#formularioEscolaridad')[0].reset();
                    $('#formularioDomicilioParticular')[0].reset();
                    $('#formularioDomicilioFiscal')[0].reset();
                    if(data.tiempo_error){
                        $("#spinnerCURP").hide();
                        $("#EBCURP").text("No hay respuesta del servidor RENAPO.");
                    }else if(data.conexion_error){
                        $("#spinnerCURP").hide();
                        $("#EBCURP").text("Error en la conexión.");
                    }else if (data.Status) { //No está registrado
                        if (data.Status == "EXITOSO") { //Curp encontrada
                            $("#Nombre").val(data.Nombre);
                            $("#Paterno").val(data.ApPaterno);
                            $("#Materno").val(data.ApMaterno);
                            $("#Sexo").val(data.Sexo);
                            $("#FechaNacimiento").val(data.FechaNacimiento);
                            $("#CURP").val(data.CURP);
                            $("#tablaEmpleadoSeleccionado").show();

                        } else {
                            $("#EBCURP").text(data.Mensaje);
                            $("#tablaEmpleadoSeleccionado").hide();
                        }
                    } else {
                        abrirModal("El empleado ya está registrado", "El empleado ya está en la base de datos. A continuación puede actualizar la información.", "modificarEmpleado");
                    }

                    if (data.Status != "EXITOSO") {
                        $("#BCURP").val(data.CURP);
                        $("#EECURP").text(data.Mensaje);
                    }
                }
            });
        }
    });

    $("#submitCP1").click(function (event) {
        $("#spinnerCP1").show();
        event.preventDefault();
        buscarCP(1);
    });

    $("#submitCP2").click(function (event) {
        event.preventDefault();
        buscarCP(2)
    });

    $("#btnHabilitarCampos").click(function (event) {
        event.preventDefault();

        if ($("#Nombre").prop("readonly")) {
            $("#Nombre").attr("readonly", false);
            $("#Paterno").attr("readonly", false);
            $("#Materno").attr("readonly", false);
            $("#Sexo").attr("readonly", false);
            $("#FechaNacimiento").attr("readonly", false);
            $("#CURP").attr("readonly", false);
            $("#btnHabilitarCampos").addClass("active");

        } else {
            $("#Nombre").attr("readonly", true);
            $("#Paterno").attr("readonly", true);
            $("#Materno").attr("readonly", true);
            $("#Sexo").attr("readonly", true);
            $("#FechaNacimiento").attr("readonly", true);
            $("#CURP").attr("readonly", true);
            $("#btnHabilitarCampos").removeClass("active");

        }

    });

    $("#FecIngresoGob").datepicker({ dateFormat: 'dd/mm/yy', maxDate: 0, changeYear: true, changeMonth: true });
    $("#FecIngreso").datepicker({ dateFormat: 'dd/mm/yy', maxDate: 0, changeYear: true, changeMonth: true });

    $("#Clabe").keydown(validarSoloNumeros);
    $("#Clabe").on("input", verBanco);
    $("#idEstatus").change(modalReafirmar);
    $("#btnCancelarModalAltaBaja").on("click", function () { cancelarSelectEstatus(); });
});

function validarSoloNumeros(event) {
    //$("#Clabe").keydown(function(event){
    //
    if ((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105) && event.keyCode !== 190 && event.keyCode !== 110 && event.keyCode !== 8 && event.keyCode !== 9 && event.keyCode !== 46) {
        return false;
    }
    //});
}

function verBanco() {
    if ($("#Clabe").val().length >= 3) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/obtener-banco",
            data: {
                "subClabe": $("#Clabe").val().substring(0, 3)
            },
            success: function (data) {
                $("#Banco").val(data.Nombre);
                $("#idBanco").val(data.idBanco);
            }
        });
    }else{
        $("#Banco").val("");
    }
}

function modalReafirmar() {
    $('#ModalAltaBaja').attr('data-valorInicial', $("#idEstatus").val());
    $('#ModalAltaBaja').modal('show');
}

function cancelarSelectEstatus() {
    var estadoInicial = $('#ModalAltaBaja').attr('data-valorInicial');
    
    if (estadoInicial == 0) {
        $("#idEstatus").val(1)
    } else {
        $("#idEstatus").val(0)
    }
}

function modalReafirmar() {
    $('#ModalAltaBaja').attr('data-valorInicial', $("#idEstatus").val());
    $('#ModalAltaBaja').modal('show');
}

function cancelarSelectEstatus() {
    var estadoInicial = $('#ModalAltaBaja').attr('data-valorInicial');
    
    if (estadoInicial == 0) {
        $("#idEstatus").val(1)
    } else {
        $("#idEstatus").val(0)
    }
}