$gmx(document).ready(function(){
    $("#btnCargarArchivo").click(cargar_archivo);
    $("#btnModalCrearPuesto").click(modal_crear_puesto);
    $("#btnCrearPuesto").click(crear_puesto);
    $("#btnBuscaPuesto").click(buscar_puesto);

    $("#PuestoExistente").on("focus", function(){
        $("#lista_puestos").show();
    });

    $("#PuestoExistente").on("blur", function(event){
        if(!$(event.relatedTarget).closest("#lista_puestos").length){
            $("#lista_puestos").hide();
        }
    });

    $("#PuestoExistente").on("input", function(){
        var textoBusqueda = $(this).val();
        $.ajax({
            url: "/catalogos/actualizar-busqueda-puestos",
            method: "GET",
            data: {
                texto_busqueda: textoBusqueda
            },
            success: function(response){
                actualizarListaDesplegable(response);
            }
        })
    });

    $("#FechaInicio").datepicker({changeYear: true, changeMonth: true});
    $("#FechaFin").datepicker({changeYear: true, changeMonth: true});

    configuraDatepickers("FechaInicio", "FechaFin", "");

});

function modal_crear_puesto(){
    $("#ModalCrearPuesto").modal("show");

    $("#ConsecutivoPuesto").val("");
    $("#consecutivo").val("");

    $("#Ramo").prop("disabled", false);
    $("#UA").prop("disabled", false);
    $("#CodigoPuesto").prop("readonly", false);
    $("#ZonaEconomica").prop("disabled", false);
    $("#Puesto").prop("readonly", false);
    $("#ReferenciaTabular").prop("readonly", false);
    $("#ConsPuesto").prop("readonly", false);
    $("#TipoPlazaPuesto").prop("disabled", false);
    $("#CaracterOcupacional").prop("disabled", false);
    $("#TipoFuncion").prop("disabled", false);
    $("#NivelSalarial").prop("readonly", false);
    $("#Tabulador").prop("readonly", false);
    $("#CodigoPresupuestal").prop("readonly", false);
    $("#OrdinalCP").prop("readonly", false);
    $("#Grupo").prop("disabled", false);
    $("#Grado").prop("disabled", false);
    $("#Nivel").prop("disabled", false);
    $("#EstatusPuesto").prop("disabled", false);
    $("#Vigencia").prop("disabled", false);
    $("#FechaInicio").prop("readonly", false);
    $("#FechaFin").prop("readonly", false);
    $("#CentroTrabajo").prop("disabled", false);
    $("#FolioSival").prop("readonly", false);
    $("#RegimenLaboral").prop("readonly", false);
    $("#RemuneracionTotal").prop("readonly", false);
    $("#TitularAU").prop("readonly", false);
    $("#DeclaracionPatrimonial").prop("readonly", false);
    $("#PlazasSubordinadas").prop("readonly", false);
    $("#PuestoJefe").prop("readonly", false);
    $("#PresupuestalJefe").prop("readonly", false);
    $("#CentroCosto").prop("disabled", false);

    $("#tituloModalCrearPuesto")[0].textContent = "Crear nuevo puesto";
    $("#btnCrearPuesto")[0].textContent = "Crear";

    $("#Ramo").val("0");
    $("#UA").val("0");
    $("#CodigoPuesto").val("");
    $("#ZonaEconomica").val("0");
    $("#Puesto").val("");
    $("#ReferenciaTabular").val("");
    $("#ConsPuesto").val("");
    $("#TipoPlazaPuesto").val("");
    $("#CaracterOcupacional").val("0");
    $("#TipoFuncion").val("0");
    $("#NivelSalarial").val("");
    $("#Tabulador").val("");
    $("#CodigoPresupuestal").val("");
    $("#OrdinalCP").val("");
    $("#Grupo").val("0");
    $("#Grado").val("0");
    $("#Nivel").val("0");
    $("#EstatusPuesto").val("0");
    $("#Vigencia").val("0");
    $("#FechaInicio").val("");
    $("#FechaFin").val("");
    $("#CentroTrabajo").val("0");
    $("#FolioSival").val("");
    $("#RegimenLaboral").val("");
    $("#RemuneracionTotal").val("");
    $("#TitularAU").val("");
    $("#DeclaracionPatrimonial").val("");
    $("#PlazasSubordinadas").val("");
    $("#PuestoJefe").val("");
    $("#PresupuestalJefe").val("");
    $("#CentroCosto").val("0");
}

function actualizarListaDesplegable(resultados){
    var listaDesplegable = $("#lista_puestos");
    listaDesplegable.empty(); // Vaciar la lista desplegable antes de agregar nuevos elementos
    resultados.forEach(function(resultado){
        var nuevoElemento = $('<div>', {
            'class': 'dropdown-item form-group',
            'html': $('<a>', {
                'href': 'javascript:void(0)', // El href está configurado para evitar que la página se recargue
                'data-id': resultado.ConsPuesto,
                'data-texto': resultado.Puesto,
                'text': resultado.Puesto,
                'click': function(){
                    var textoSeleccionado = $(this).data('texto');
                    $("#PuestoExistente").val(textoSeleccionado);
                    $("#lista_puestos").hide();
                }
            })
        });
        listaDesplegable.append(nuevoElemento);
    });
}

function crear_puesto(){
    if(validarFormulario($("#formularioCrearPuesto")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/crear-puesto",
            data: $("#formularioCrearPuesto, #consecutivo").serialize(),
            success: function(data){
                if(data){
                    abrirModal("Información guardada", "Operación realizada con éxito.", "");
                    $("#ModalCrearPuesto").modal("hide");
                }
            }
        });
    }
}

function buscar_puesto(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/buscar-puesto",
        data: $("#formularioBuscarPuesto").serialize(),
        success: function(respuesta){
            if(respuesta.NoEncontrado){
                abrirModal("No encontrado", "No se encontraron coincidencias.", "");
            }else{
                $("#tablaResultadosPuestos").show();
                $("#tablaResultadosPuestos tbody").empty();
                var cont = 1;

                respuesta.ListaPuestos.forEach(function(puesto){
                    text = `
                        <tr>
                            <input type="hidden" id="Ramo${cont}" value="${puesto.idRamo}"></input>
                            <input type="hidden" id="UA${cont}" value="${puesto.idUA}"></input>
                            <input type="hidden" id="ConsecutivoPuesto${cont}" value="${puesto.ConsecutivoPuesto}"></input>
                            <input type="hidden" id="CodigoPuesto${cont}" value="${puesto.CodigoPuesto}"></input>
                            <input type="hidden" id="ZonaEconomica${cont}" value="${puesto.idZonaEconomica}"></input>
                            <input type="hidden" id="ReferenciaTabular${cont}" value="${puesto.ReferenciaTabular}"></input>
                            <input type="hidden" id="ConsPuesto${cont}" value="${puesto.ConsPuesto}"></input>
                            <input type="hidden" id="TipoPlazaPuesto${cont}" value="${puesto.idTipoPlazaPuesto}"></input>
                            <input type="hidden" id="CaracterOcupacional${cont}" value="${puesto.idCaracterOcupacional}"></input>
                            <input type="hidden" id="TipoFuncion${cont}" value="${puesto.idTipoFuncion}"></input>
                            <input type="hidden" id="NivelSalarial${cont}" value="${puesto.NivelSalarial}"></input>
                            <input type="hidden" id="Tabulador${cont}" value="${puesto.Tabulador}"></input>
                            <input type="hidden" id="CodigoPresupuestal${cont}" value="${puesto.CodigoPresupuestal}"></input>
                            <input type="hidden" id="OrdinalCP${cont}" value="${puesto.OrdinalCP}"></input>
                            <input type="hidden" id="Grupo${cont}" value="${puesto.idGrupo}"></input>
                            <input type="hidden" id="Grado${cont}" value="${puesto.idGrado}"></input>
                            <input type="hidden" id="EstatusPuesto${cont}" value="${puesto.idEstatusPuesto}"></input>
                            <input type="hidden" id="Vigencia${cont}" value="${puesto.idVigencia}"></input>
                            <input type="hidden" id="FechaInicio${cont}" value="${puesto.FechaInicio}"></input>
                            <input type="hidden" id="FechaFin${cont}" value="${puesto.FechaFin}"></input>
                            <input type="hidden" id="CentroTrabajo${cont}" value="${puesto.idCentroTrabajo}"></input>
                            <input type="hidden" id="FolioSival${cont}" value="${puesto.FolioSival}"></input>
                            <input type="hidden" id="RegimenLaboral${cont}" value="${puesto.RegimenLaboral}"></input>
                            <input type="hidden" id="RemuneracionTotal${cont}" value="${puesto.RemuneracionTotal}"></input>
                            <input type="hidden" id="TitularAU${cont}" value="${puesto.TitularAU}"></input>
                            <input type="hidden" id="DeclaracionPatrimonial${cont}" value="${puesto.DeclaracionPatrimonial}"></input>
                            <input type="hidden" id="PlazasSubordinadas${cont}" value="${puesto.PlazasSubordinadas}"></input>
                            <input type="hidden" id="PuestoJefe${cont}" value="${puesto.PuestoJefe}"></input>
                            <input type="hidden" id="PresupuestalJefe${cont}" value="${puesto.PresupuestalJefe}"></input>
                            <input type="hidden" id="CentroCosto${cont}" value="${puesto.idCentroCosto}"></input>
                            <td>
                                <input type="text" id="Puesto${cont}" value="${puesto.Puesto}" class="form-control" readonly></input>
                            </td>

                            <td>
                                <div style="display: block;">
                                    <button type="button" class="btn btn-primary btn-sm" id="Editar_Aceptar${cont}" onclick="editar_puesto(${cont})"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>
                                </div>
                            </td>
                        </tr>
                    `;
                    $("#tablaResultadosPuestos tbody").append(text);
                    cont++;
                });
            }
        }
    });
}

function editar_puesto(consecutivo){
    $("#ModalCrearPuesto").modal("show");

    $("#consecutivo").val(consecutivo);

    $("#Ramo").prop("disabled", false);
    $("#UA").prop("disabled", false);
    $("#CodigoPuesto").prop("readonly", false);
    $("#ZonaEconomica").prop("disabled", false);
    $("#Puesto").prop("readonly", false);
    $("#ReferenciaTabular").prop("readonly", false);
    $("#ConsPuesto").prop("readonly", false);
    $("#TipoPlazaPuesto").prop("disabled", false);
    $("#CaracterOcupacional").prop("disabled", false);
    $("#TipoFuncion").prop("disabled", false);
    $("#NivelSalarial").prop("readonly", false);
    $("#Tabulador").prop("readonly", false);
    $("#CodigoPresupuestal").prop("readonly", false);
    $("#OrdinalCP").prop("readonly", false);
    $("#Grupo").prop("disabled", false);
    $("#Grado").prop("disabled", false);
    $("#Nivel").prop("disabled", false);
    $("#EstatusPuesto").prop("disabled", false);
    $("#Vigencia").prop("disabled", false);
    $("#FechaInicio").prop("readonly", false);
    $("#FechaFin").prop("readonly", false);
    $("#CentroTrabajo").prop("disabled", false);
    $("#FolioSival").prop("readonly", false);
    $("#RegimenLaboral").prop("readonly", false);
    $("#RemuneracionTotal").prop("readonly", false);
    $("#TitularAU").prop("readonly", false);
    $("#DeclaracionPatrimonial").prop("readonly", false);
    $("#PlazasSubordinadas").prop("readonly", false);
    $("#PuestoJefe").prop("readonly", false);
    $("#PresupuestalJefe").prop("readonly", false);
    $("#CentroCosto").prop("disabled", false);

    $("#tituloModalCrearPuesto")[0].textContent = "Editar puesto";
    $("#btnCrearPuesto")[0].textContent = "Editar";

    FechaInicio = convertirFechaParaVisualizacion($("#FechaInicio" + consecutivo).val());
    FechaFin = convertirFechaParaVisualizacion($("#FechaFin" + consecutivo).val())

    $("#Ramo").val($("#Ramo" + consecutivo).val());
    $("#UA").val($("#UA" + consecutivo).val());
    $("#ConsecutivoPuesto").val($("#ConsecutivoPuesto" + consecutivo).val())
    $("#CodigoPuesto").val($("#CodigoPuesto" + consecutivo).val());
    $("#ZonaEconomica").val($("#ZonaEconomica" + consecutivo).val());
    $("#Puesto").val($("#Puesto" + consecutivo).val());
    $("#ReferenciaTabular").val($("#ReferenciaTabular" + consecutivo).val());
    $("#ConsPuesto").val($("#ConsPuesto" + consecutivo).val());
    $("#TipoPlazaPuesto").val($("#TipoPlazaPuesto" + consecutivo).val());
    $("#CaracterOcupacional").val($("#CaracterOcupacional" + consecutivo).val());
    $("#TipoFuncion").val($("#TipoFuncion" + consecutivo).val());
    $("#NivelSalarial").val($("#NivelSalarial" + consecutivo).val());
    $("#Tabulador").val($("#Tabulador" + consecutivo).val());
    $("#CodigoPresupuestal").val($("#CodigoPresupuestal" + consecutivo).val());
    $("#OrdinalCP").val($("#OrdinalCP" + consecutivo).val());
    $("#Grupo").val($("#Grupo" + consecutivo).val());
    $("#Grado").val($("#Grado" + consecutivo).val());
    $("#Nivel").val($("#Nivel" + consecutivo).val());
    $("#EstatusPuesto").val($("#EstatusPuesto" + consecutivo).val());
    $("#Vigencia").val($("#Vigencia" + consecutivo).val());
    $("#FechaInicio").val(FechaInicio);
    $("#FechaFin").val(FechaFin);
    $("#CentroTrabajo").val($("#CentroTrabajo" + consecutivo).val());
    $("#FolioSival").val($("#FolioSival" + consecutivo).val());
    $("#RegimenLaboral").val($("#RegimenLaboral" + consecutivo).val());
    $("#RemuneracionTotal").val($("#RemuneracionTotal" + consecutivo).val());
    $("#TitularAU").val($("#TitularAU" + consecutivo).val());
    $("#DeclaracionPatrimonial").val($("#DeclaracionPatrimonial" + consecutivo).val());
    $("#PlazasSubordinadas").val($("#PlazasSubordinadas" + consecutivo).val());
    $("#PuestoJefe").val($("#PuestoJefe" + consecutivo).val());
    $("#PresupuestalJefe").val($("#PresupuestalJefe" + consecutivo).val());
    $("#CentroCosto").val($("#CentroCosto" + consecutivo).val());

}

function cargar_archivo(){
    const archivo = new FormData();
    archivo.append('archivo', $("#Archivo")[0].files[0]);

    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/cargar-archivo-puestos",
        data: archivo,
        enctype: "multipart/form-data",
        contentType: false,
        processData: false,
        success: function(data){
            if(data.guardado){
                abrirModal("Datos cargados", "Los datos se han cargado correctamente.", "recargar");
            }else{
                abrirModal("Datos no cargados", "No se seleccionó un archivo.", "");
            }
        }
    });
}

function configuraDatepickers(idInicio, idFin, data) {
    $(`#${idInicio}${data}, #${idFin}${data}`).datepicker({
        // $(`#fechaInicioFormateada${data}, #fechaFinFormateada${data}`).datepicker({
        changeYear: true,
        changeMonth: true,
        beforeShow: function (input, inst) {
            var fechaLimite = this.id === `${idInicio}${data}` ? $(`#${idFin}${data}`).datepicker("getDate") : $(`#${idInicio}${data}`).datepicker("getDate");
            if (this.id === `${idInicio}${data}`) {
                if (fechaLimite) {
                    $(this).datepicker("option", "maxDate", fechaLimite);
                } else {
                    //$(this).datepicker("option", "maxDate", null);
                }
            } else {
                if (fechaLimite) {
                    $(this).datepicker("option", "minDate", fechaLimite);
                }
                else {
                    //$(this).datepicker("option", "minDate", null);
                }
            }
        },
        onSelect: function (dateText) {
            var fechaInicial = $(`#${idInicio}${data}`).datepicker("getDate");
            var fechaFinal = $(`#${idFin}${data}`).datepicker("getDate");

            if (fechaFinal && fechaInicial) {
                if (fechaInicial > fechaFinal) {
                    abrirModal("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.", "");
                    $(this).val("");

                } else {
                    // var fechaInicioISO = $.datepicker.formatDate('yy-mm-dd', fechaInicial);
                    // var fechaFinISO = $.datepicker.formatDate('yy-mm-dd', fechaFinal);

                    // $.ajax({
                    //     async: false,
                    //     type: "POST",
                    //     url: "/RH/obtener_quincenas_entre_fechas",
                    //     data: {
                    //         "FechaInicio": fechaInicioISO,
                    //         "FechaFin": fechaFinISO
                    //     },
                    //     success: function (data) {
                    //         $("#NumeroQuincena").val(data)
                    //      }
                    // });
                }
            }
        }
    });
}