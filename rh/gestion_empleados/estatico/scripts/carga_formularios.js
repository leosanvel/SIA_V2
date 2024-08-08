function obtenerDomicilio(tipo) {
    $.ajax({
        type: "POST",
        url: "/rh/gestion-empleados/obtener-domicilio",
        data: {
            tipo: tipo
        },
        success: function (data) {
            if (data != null) {
                if (data.idTipoDomicilio == 1) {
                    var formulario = $("#formularioDomicilioParticular");
                } else {
                    var formulario = $("#formularioDomicilioFiscal");
                }

                formulario.find("#Entidad").val(data.idEntidad);
                cargarMunicipio(data.idTipoDomicilio);
                formulario.find("#Municipio").val(data.idMunicipio);
                cargarLocalidad(data.idTipoDomicilio);
                formulario.find("#Localidad").val(data.idLocalidad);
                formulario.find("#TipoAsentamiento").val(data.idTipoAsentamiento);
                cargaAsentamiento(data.idTipoDomicilio);
                formulario.find("#Asentamiento").val(data.idAsentamiento);
                formulario.find("#CP").val(data.idCP);
                formulario.find("#TipoVialidad").val(data.idTipoVialidad);
                formulario.find("#Vialidad").val(data.Vialidad);
                formulario.find("#SN").prop("checked", data.SinNumero);
                cargaSinNumero(data.idTipoDomicilio);
                formulario.find("#DC").prop("checked", data.DomicilioConocido);
                formulario.find("#NumExt").val(data.NumExterior);
                formulario.find("#NumInt").val(data.NumInterior);
                formulario.find("#TipoVialidad01").val(data.idTipoVialidad01 !== null ? data.idTipoVialidad01 : 0);
                formulario.find("#Vialidad01").val(data.Vialidad01);
                formulario.find("#TipoVialidad02").val(data.idTipoVialidad02 !== null ? data.idTipoVialidad02 : 0);
                formulario.find("#Vialidad02").val(data.Vialidad02);
                formulario.find("#TipoVialidad03").val(data.idTipoVialidad03 !== null ? data.idTipoVialidad03 : 0);
                formulario.find("#Vialidad03").val(data.Vialidad03);
            }
        }
    });
}

function obtenerEscolaridad(){
    $.ajax({
        type: "POST",
        url: "/rh/gestion-empleados/obtener-escolaridad",
        success: function(data){
            if(data != null){
                $("#idEscolaridad").val(data.idEscolaridad);
                //cargarEstNivEsc();
                //cargarEscuela();
                $("#idNivelEscolaridad").val(data.idNivelEscolaridad);
                $("#idInstitucionEscolar").val(data.idInstitucionEscolar);
                //cargarFormacionEducativa();
                $("#idFormacionEducativa").val(data.idFormacionEducativa);
                $("#Especialidad").val(data.Especialidad);
            }
        }
    })
}

function obtenerInfoEmpleado() {
    $.ajax({
        type: "POST",
        url: "/rh/gestion-empleados/obtener-info-empleado",
        success: function (data) {
            if (data != null) {
                console.log(data);
                if(data.FechaNacimiento){
                    var FechaNacimientoFormateada = convertirFechaParaVisualizacion(data.FechaNacimiento);
                }else
                    var FechaNacimientoFormateada = "";
                if(data.fechaIngGob){
                    var FecIngresoGobFormateada = convertirFechaParaVisualizacion(data.FecIngGobierno);
                }else{
                    var FecIngresoGobFormateada = "";
                }
                if(data.FecIngFonaes){
                    var FecIngresoFormateada = convertirFechaParaVisualizacion(data.FecIngFonaes);
                }else{
                    var FecIngresoFormateada = "";
                }
                
                
                $("#CURP").val(data.CURP);
                $("#Nombre").val(data.Nombre);
                $("#Paterno").val(data.ApPaterno);
                $("#Materno").val(data.ApMaterno);
                $("#Sexo").val(data.Sexo);
                $("#FechaNacimiento").val(FechaNacimientoFormateada);
                $("#RFC").val(data.RFC);
                $("#idTipoPersona").val(data.idTipoPersona);
                $("#idEstadoCivil").val(data.idEstadoCivil);
                $("#idNacionalidad").val(data.idNacionalidad);
                cargaCalidadMigratoria();
                $("#CalidadMigratoria").val(data.CalidadMigratoria);
                $("#TelCasa").val(data.TelCasa);
                $("#TelCelular").val(data.TelCelular);
                $("#CorreoPersonal").val(data.CorreoPersonal);
                $("#CorreoInstitucional").val(data.CorreoInstitucional);
                if(data.idEstatusEP){
                    $("#idTipoEmpleo").val(data.idTipoEmpleado);
                    cargarTipAlt();
                    $("#idTipoAlta").val(data.idTipoAlta);
                    cargarGrupo();
                    $("#idGrupo").val(data.idGrupo);
                    $("#idCC").val(data.idCentroCosto);
                    cargarPlaza();
                    $("#idPlazaHom").append(`<option value = ${data.idPuesto}>${data.Puesto}</option>`);
                    $("#idPlazaHom").val(data.idPuesto);
                    $("#idUbicacion").val(data.idCentroCosto);
                }
                $("#HoraEntrada").val(data.HoraEntrada);
                $("#HoraSalida").val(data.HoraSalida);
                $("#FecIngresoGob").val(FecIngresoGobFormateada);
                cargarMesesSerGob();
                $("#FecIngreso").val(FecIngresoFormateada);
                //$("#MesesServicio").val(data.MesesServicio);
                
                $("#NumQuincena").val(data.idQuincena);
                $("#idEstatus").val(data.Activo);

                if(data.Activo){
                    $("#idCC").prop("disabled", true);
                    $("#idPlazaHom").prop("disabled", true);
                    $("#idTipoEmpleo").prop("disabled", true);
                    $("#idTipoAlta").prop("disabled", true);
                    $("#idGrupo").prop("disabled", true);
                }

            }
        }
    });
}

function obtenerDatosBanco(){
    $.ajax({
        type: "POST",
        url: "/rh/gestion-empleados/obtener-datos-bancarios",
        success: function(data){
            if(data.datos_bancarios != null){
                $("#Clabe").val(data.datos_bancarios.Clabe);
                $("#Banco").val(data.datos_bancarios.Banco);
                if(data.datos_bancarios.Verificado){
                    $("#Clabe").prop("readonly", true);
                }
                if(data.url){
                    $("#btnDescargarEstadoCuenta").show();
                    $("#btnDescargarEstadoCuenta").wrap('<a href="' + data.url + '" download></a>');
                }
            }
        }
    });
}

function obtenerExpediente(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/obtener-expediente",
        success: function(data){
            if(data){
                if(data.expediente){
                    for(const prop in data.expediente){
                        if(data.expediente[prop]){
                            $("#check" + prop).prop("checked", true);
                        }
                    }
                }
                if(data.url){
                    $("#btnDescargarExpediente").show();
                    $("#btnDescargarExpediente").wrap('<a href="' + data.url + '" download></a>');
                }
            }
        }
    });
}

function obtenerMasInformacion(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/obtener-mas-informacion",
        success: function(data){
            console.log(data);
            if(data){
                if(data.mas_informacion){
                    $("#Indigena").val(data.mas_informacion.idIdiomaIndigena);
                    $("#Afroamericano").val(data.mas_informacion.idAfroamericano);
                    $("#Discapacidad").val(data.mas_informacion.idDiscapacidad);
                }

                if(data.Idiomas){
                    var cont = 2;
                    data.Idiomas.forEach(function(Idioma, index){
                        if(index == 0){
                            $("#Idioma1").val(Idioma.idIdioma);
                        }else{
                            text = `
                                <div class="row fila-idioma">
                                    <div class="col-md-8">
                                        <div class="form-group">
                                            <select id="Idioma${cont}" name="Idioma${cont}" class="opcional form-control idioma">

                                            </select>
                                            <small id="EIdioma${cont}" class="etiquetaError form-text form-text-error"></small>
                                        </div>
                                    </div>
                                    <div class="col-md-2">
                                        <button type="button" class="btn btn-primary btn-sm remover" id="RemoverIdioma${cont}">
                                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                                        </button>
                                    </div>
                                </div>
                            `;
                            $(`#ColIdiomas`).append(text);
                            $("#Idioma1 option").clone().appendTo(`#Idioma${cont}`);
                            $("#Idioma" + cont).val(Idioma.idIdioma);
                            cont++;
                        }
                    });
                }

                if(data.Indigena){
                    var cont = 1;
                    data.Indigenas.forEach(function(Indigena){
                        text = `
                            <div class="row fila-idioma">
                                <div class="col-md-8">
                                    <div class="form-group">
                                        <select id="IdiomaIndigena${cont}" name="IdiomaIndigena${cont}" class="opcional form-control indigena">
                                            <option value="0">-- Seleccione --</option>
                                        </select>
                                        <small id="EIdiomaIndigena${cont}" class="etiquetaError form-text form-text-error"></small>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <button type="button" class="btn btn-primary btn-sm remover" id="RemoverIdiomaIndigena${cont}">
                                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                                    </button>
                                </div>
                            </div>
                        `;
                        $("#ColIdiomasIndigenas").append(text);
                        $("#IdiomaIndigena" + cont).val(Indigena.idIndigena);
                        cont++;
                    });
                }
            }
        }
    });
}

function cargarMesesSerGob() {
    // Obtiene la cadena de fecha en formato "DD/MM/AAAA"
    var fechaString = $("#FecIngresoGob").val();
    // Divide la cadena en día, mes y año
    var partes = fechaString.split('/');
    var dia = parseInt(partes[0], 10);
    var mes = parseInt(partes[1], 10) - 1; // Resta 1 al mes ya que en JavaScript los meses van de 0 a 11
    var anio = parseInt(partes[2], 10);

    // Crea la fecha con los valores extraídos
    var fechaIngGob = new Date(anio, mes, dia);
    if (!isNaN(fechaIngGob.getTime())) {
        var mesesServicio = calcularMesesServicio(fechaIngGob);
        $("#MesesServicio").val(mesesServicio);
    }
}

function calcularMesesServicio(fechaIngGob) {
    // Obtén la fecha actual
    var fechaActual = new Date();
    // Calcula la diferencia en años y meses
    var añosDiferencia = fechaActual.getFullYear() - fechaIngGob.getFullYear();
    var mesesDiferencia = fechaActual.getMonth() - fechaIngGob.getMonth();
    // Ajusta la diferencia si los meses son negativos
    if (mesesDiferencia < 0) {
        añosDiferencia--;
        mesesDiferencia += 12;
    }
    // Calcula el número total de meses
    var mesesServicio = añosDiferencia * 12 + mesesDiferencia;
    return mesesServicio;
}

// Funciones para cargar datos de SELECT mediante peticiones AJAX
function cargarTipAlt() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/select_TipAlt",
        data: {
            "idTipoEmpleo": $("#idTipoEmpleo").val(),
        },
        success: function (data) {
            $("#idTipoAlta").html(data);
            $("#idTipoAlta").trigger('change');
        }
    });
}

function cargarGrupo() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/select_Grupo",
        data: {
            "idTipoAlta": $("#idTipoAlta").val(),
        },
        success: function (data) {
            $("#idGrupo").html(data);

        }
    });
}

function cargarMunicipio(tipo) {
    if (tipo == 1) {
        var formulario = $("#formularioDomicilioParticular");
    } else {
        var formulario = $("#formularioDomicilioFiscal");
    }
    var entidad = formulario.find("#Entidad").val();
    $.ajax({
        async: false,
        type: "POST",
        url: "/select_municipio",
        data: {
            "Entidad": entidad
        },
        success: function (data) {
            if (tipo == 1) {
                var formulario = $("#formularioDomicilioParticular");
            } else {
                var formulario = $("#formularioDomicilioFiscal");
            }
            formulario.find("#Municipio").html(data);
            formulario.find("#Municipio").trigger("change")
            formulario.find("#Asentamiento").trigger("change");
            // formulario.find("#Asentamiento").trigger("change");
            formulario.find("#BCP").val("");
        }
    });
}

function cargarLocalidad(tipo) {
    if (tipo == 1) {
        var formulario = $("#formularioDomicilioParticular");
    } else {
        var formulario = $("#formularioDomicilioFiscal");
    }
    var entidad = formulario.find("#Entidad").val();
    var municipio = formulario.find("#Municipio").val();
    $.ajax({
        async: false,
        type: "POST",
        url: "/select_localidad",
        data: {
            "Entidad": entidad,
            "Municipio": municipio
        },
        success: function (data) {
            if (tipo == 1) {
                var formulario = $("#formularioDomicilioParticular");
            } else {
                var formulario = $("#formularioDomicilioFiscal");
            }
            formulario.find("#Localidad").html(data);
            formulario.find("#TipoAsentamiento").val("0");
            formulario.find("#Asentamiento").trigger("change");
            formulario.find("#BCP").val("");
        }
    });
}

function cargaAsentamiento(tipo) {
    if (tipo == 1) {
        var formulario = $("#formularioDomicilioParticular");
    } else {
        var formulario = $("#formularioDomicilioFiscal");
    }
    if ((formulario.find("#Entidad").val() != 0) && (formulario.find("#Municipio").val != 0) && (formulario.find("#TipoAsentamiento").val() != 0)) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/select_asentamiento",
            data: {
                "Entidad": formulario.find("#Entidad").val(),
                "Municipio": formulario.find("#Municipio").val(),
                "TipoAsentamiento": formulario.find("#TipoAsentamiento").val()
            },
            success: function (data) {
                formulario.find("#Asentamiento").html(data);
                formulario.find("#Asentamiento").trigger("change");
                formulario.find("#BCP").val("");
            }
        });
    }
    else {
        text = "<option value = '0'>-- Seleccione --</option>";
        formulario.find("#Asentamiento").html(text);
    }
}

function cargarCP(tipo) {
    if (tipo == 1) {
        var formulario = $("#formularioDomicilioParticular");
    } else {
        var formulario = $("#formularioDomicilioFiscal");
    }
    if ((formulario.find("#Entidad").val() != 0) && (formulario.find("#Municipio").val != 0) && (formulario.find("#TipoAsentamiento").val() != 0) && (formulario.find("#Asentamiento").val() != 0)) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/cargar-cp",
            data: {
                "Entidad": formulario.find("#Entidad").val(),
                "Municipio": formulario.find("#Municipio").val(),
                "TipoAsentamiento": formulario.find("#TipoAsentamiento").val(),
                "Asentamiento": formulario.find("#Asentamiento").val()
            },
            success: function (data) {
                if (data == "no encontrado") {
                    formulario.find("#CP").val("");
                } else {
                    formulario.find("#CP").val(data)
                }


            }
        });
    }
    else {
        formulario.find("#CP").val("");
    }

    formulario.find("#TipoVialidad").val("0");
    formulario.find("#Vialidad").val("");

    formulario.find("#DC").prop("checked", false);
    formulario.find("#SN").prop("checked", false);
    cargaSinNumero(tipo);

    formulario.find("#TipoVialidad01").val("0");
    formulario.find("#Vialidad01").val("");

    formulario.find("#TipoVialidad02").val("0");
    formulario.find("#Vialidad02").val("");

    formulario.find("#TipoVialidad03").val("0");
    formulario.find("#Vialidad03").val("");
}

function cargarPlaza() {
    if($("#idTipoEmpleo").val() == 2){
        $.ajax({
            async: false,
            type: "POST",
            url: "/cargar_Plaza",
            data: {
                "idCentroCostos": $("#idCC").val()
            },
            success: function (data) {
                $("#idPlazaHom").html(data);
                $("#idUbicacion").val($("#idCC").val());
            }
        });
    }
}

function cargarPuestosHonorarios(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/cargar-puestos-honorarios",
        success: function(data){
            $("#idPlazaHom").html(data);
        }
    });
}

function cargarEstNivEsc() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/cargar_EstNivEsc",
        data: {
            "idEscolaridad": $("#idEscolaridad").val()
        },
        success: function (data) {
            $("#idNivelEscolaridad").html(data);
            $("#Especialidad").val("");
        }
    });
}
function cargarEscuela() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/cargar_Escuela",
        data: {
            "idEscolaridad": $("#idEscolaridad").val()
        },
        success: function (data) {
            $("#idInstitucionEscolar").html(data);
            $("#Especialidad").val("");
        }
    });
}
function cargarFormacionEducativa() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/cargar_FormacionEducativa",
        data: {
            "idInstitucionEscolar": $("#idInstitucionEscolar").val()
        },
        success: function (data) {
            $("#idFormacionEducativa").html(data);
            $("#Especialidad").val("");
        }
    });
}

function cargaSinNumero(tipo) {
    if (tipo == 1) {
        var formulario = $("#formularioDomicilioParticular");
    } else {
        var formulario = $("#formularioDomicilioFiscal");
    }
    if (formulario.find("#SN").prop("checked")) {
        formulario.find("#NumExt").val("N/A");
        formulario.find("#NumInt").val("N/A");

        formulario.find("#NumExt").prop("readonly", true);
        formulario.find("#NumInt").prop("readonly", true);

    } else {
        formulario.find("#NumExt").val("");
        formulario.find("#NumInt").val("");

        formulario.find("#NumExt").prop("readonly", false);
        formulario.find("#NumInt").prop("readonly", false);

    }
}

function cargaCalidadMigratoria() {
    var nacionalidad = $("#idNacionalidad").val();
    if (nacionalidad == 700) {
        $("#CalidadMigratoria").val("N/A");
        $("#CalidadMigratoria").prop("readonly", true); // Establece el campo como solo lectura
    } else {
        $("#CalidadMigratoria").val("");
        $("#CalidadMigratoria").prop("readonly", false); // Si no es igual a 700, permite la edición
    }

}

function cargarModoHonorarios(){
    if($("#idTipoEmpleo").val() == 1){
        $("#FecIngresoGob").prop("disabled", true);
        $("#FecIngresoGob").val("");
        $("#FecIngreso").prop("disabled", true);
        $("#FecIngreso").val("");
        $("#MesesServicio").prop("disabled", true);
        $("#MesesServicio").val("");
        cargarPuestosHonorarios();
    }else{
        $("#FecIngresoGob").prop("disabled", false);
        $("#FecIngreso").prop("disabled", false);
        $("#MesesServicio").prop("disabled", false);
        cargarPlaza();
    }
}

$gmx(document).ready(function () {
    $("#idTipoEmpleo").change(cargarTipAlt);
    $("#idTipoEmpleo").change(cargarModoHonorarios);
    $("#idTipoAlta").change(cargarGrupo);

    $("#idNacionalidad").change(cargaCalidadMigratoria);

    $("#idCC").change(cargarPlaza);
    //$("#idEscolaridad").change(cargarEstNivEsc);
    //$("#idEscolaridad").change(cargarEscuela);
    //$("#idEscolaridad").change(cargarFormacionEducativa);
    //$("#idInstitucionEscolar").change(cargarFormacionEducativa);

    $("#FecIngresoGob").change(cargarMesesSerGob);

    $("#formularioDomicilioParticular #Entidad").change(function () { cargarMunicipio(1); });
    $("#formularioDomicilioParticular #Municipio").change(function () { cargarLocalidad(1); });
    $("#formularioDomicilioParticular #Municipio").change(function () { cargaAsentamiento(1); });
    $("#formularioDomicilioParticular #TipoAsentamiento").change(function () { cargaAsentamiento(1); });
    $("#formularioDomicilioParticular #Asentamiento").change(function () { cargarCP(1); });
    $("#formularioDomicilioParticular #SN").change(function () { cargaSinNumero(1); });

    $("#formularioDomicilioFiscal #Entidad").change(function () { cargarMunicipio(2); });
    $("#formularioDomicilioFiscal #Municipio").change(function () { cargarLocalidad(2); });
    $("#formularioDomicilioFiscal #Municipio").change(function () { cargaAsentamiento(2); });
    $("#formularioDomicilioFiscal #TipoAsentamiento").change(function () { cargaAsentamiento(2); });
    $("#formularioDomicilioFiscal #Asentamiento").change(function () { cargarCP(2); });
    $("#formularioDomicilioFiscal #SN").change(function () { cargaSinNumero(2); });

    var rutaActual = window.location.href;
    if (rutaActual.includes("/rh/gestion-empleados/modificar-empleado")) {

        obtenerInfoEmpleado();
        obtenerEscolaridad();
        obtenerDomicilio(1);
        obtenerDomicilio(2);
        obtenerDatosBanco();
        obtenerExpediente();
        obtenerMasInformacion();
        $("#busquedaCurp").hide();
        $("#tablaEmpleadoSeleccionado").show();
    }
    else {
        $("#busquedaCurp").show();
        $("#tablaEmpleadoSeleccionado").hide();
    }

    $("#mismoDomicilio").on("change", function () {
        if (this.checked) {
            $("#tab-DomicilioFiscal").hide();
        } else {
            $("#tab-DomicilioFiscal").show();
            obtenerDomicilio(2);
        }
    });

});