$gmx(document).ready(function(){
    //$("#Estado option[value = 9]").attr("selected",true);
    //$("#Municipio option[value = 3]").attr("selected",true);
    $("#FechaInicio").blur(function(){
        ValidarContratos();
        CalcularExhibiciones();
    });

    $("#FechaFin").blur(function(){
        CalcularExhibiciones();
    });

    $("#FechaInicio").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,

        onSelect: function(dateText){
            CalcularExhibiciones();
            ValidarContratos();
        }
    });
    $("#FechaFin").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,

        onSelect: function(dateText){
            CalcularExhibiciones();
        }
    });
    $("#FechaFirma").datepicker({ dateFormat: 'dd/mm/yy', changeYear: true, changeMonth: true });
    $("#btnCrearContrato").click(Guardar);
    $("#MontoPactado").on('change', function(){
        CalcularImporteBruto();
    });
   // $("#btnCrearContrato").click(function (event) {Guardar()});
    
});

function Guardar(){
    if (validarFormulario($("#frmCrearContrato")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/guardar_empleado_contrato",
            data: $("#frmCrearContrato, #idPersona").serialize(),
            success: function(data){
                if(data.respuesta == 1){
                    abrirModal("Existe el registro", "Ya existe un registro de contrato con las fechas introducidas. Valide Fecha de inicio y/o Fecha fin.", "");
                }else{
                    if(data.respuesta == 2){
                        abrirModal("Error al guardar los datos", "Los datos no se pudieron guardar. Intente nuevamente.", "");
                    }else{
                        if(data.respuesta == 99){
                            abrirModal("Datos guardados", "Los datos se han guardado correctamente.", "recargar");
                        }
                    }
                }
            }
        });
    }
}
function ValidarContratos(){
    $("#FechaFirma").val($("#FechaInicio").val());
}

function CalcularExhibiciones(){
    var Exhibiciones = null
    if($("#FechaInicio").val() != "" && $("#FechaFin").val() != ""){
        var Exhibiciones = calcularMesesFechas($("#FechaInicio").val(), $("#FechaFin").val());
        if(Exhibiciones != null){
            $("#NumeroExhibiciones").val(Exhibiciones);
            Monto = $("#MontoPactado").val();
            Monto_dec = parseFloat(Monto);
            ImporteBruto = Monto_dec*Exhibiciones/1.0;
            $("#ImporteBruto").val(ImporteBruto.toFixed(2));
        }
    }else{
        $("#NumeroExhibiciones").val("");
    }
}

function CalcularImporteBruto(){
    if($("#MontoPactado").val() != "" && $("#NumeroExhibiciones").val() != ""){
        ImporteBruto = parseFloat($("#MontoPactado").val())*parseInt($("#NumeroExhibiciones").val());
        $("#ImporteBruto").val(ImporteBruto.toFixed(2));
    }
}

function calcularMesesFechas(FechaInicio, FechaFin){
     const FechaInicioConv = convertirFechaParaEnvio(FechaInicio);
     const FechaFinConv = convertirFechaParaEnvio(FechaFin);

     const FechaInicioDate = new Date(FechaInicioConv + "T00:00:00");
     const FechaFinDate = new Date(FechaFinConv + "T00:00:00");

     let anios = FechaFinDate.getFullYear() - FechaInicioDate.getFullYear();
     let meses = FechaFinDate.getMonth() - FechaInicioDate.getMonth();

    if(meses < 0){
        anios--;
        meses += 12;
    }

    return (anios * 12) + meses + 1;
}

function funcionSeleccionar() {
    filtrar_formulario();
}
function filtrar_formulario(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/buscar-empleado-contrato",
        data: {
            idPersona: $("#idPersona").val()
        },
        success: function(data){
            console.log(data);
            if(data.respuesta == 0){
                resultadobusqueda("alert alert-danger","El empleado no existe.<br />No se puede generar contrato.");
            }else{
                if(data.respuesta == 1){
                    resultadobusqueda("alert alert-warning","El empleado se encuentra inactivo.<br />No se puede generar contrato.");
                }else{
                    if(data.respuesta == 2){                 
                        resultadobusqueda("alert alert-warning","El empleado es de plaza.<br />No se puede generar contrato.");
                    }else{
                        if(data.respuesta == 99){
                            if(data.Conocimiento != null){
                                //FechaInicio = convertirFechaParaVisualizacion(data.DatosContrato.FechaInicio);
                                //FechaFin = convertirFechaParaVisualizacion(data.DatosContrato.FechaFin);
                                //FechaFirma = convertirFechaParaVisualizacion(data.DatosContrato.FechaFirma);
                                window.document.getElementById("strMensaje").className = ""; 
                                window.document.getElementById("strMensaje").innerHTML = "";
                                $("#strMensaje").hide();                            
                                $("#tablaEmpleadoSeleccionado").show();
                                $("#frmCrearContrato").show();
                                //$("#FechaInicio").val(FechaInicio);
                                //$("#FechaFin").val(FechaFin);
                                //$("#FechaFirma").val(FechaFirma);
                                //$("#Estado").val(data.DatosContrato.idEstado);
                                //$("#Municipio").val(data.DatosContrato.idMunicipio);
                                //$("#ImporteBruto").val(data.DatosContrato.ImporteBruto);
                                //$("#NumeroExhibiciones").val(data.DatosContrato.NumeroExhibicion);
                                //$("#MontoPactado").val(data.DatosContrato.MontoPactado);
                                //$("#Proyecto").val(data.DatosContrato.Proyecto);
                                $("#Partida").val(12101);
                                $("#Origen").val(1);
                                $("#ConocimientoPrestador").val(data.Conocimiento);
                                //$("#OficioDictamen").val(data.DatosContrato.OficioDictamen);
                                $("#ConocimientoExperiencia").val(data.Conocimiento);
                                //$("#Actividades").val(data.DatosContrato.Actividades);
                                //$("#CURPEntregable").val(data.DatosContrato.CURPEntrega);
                                //$("#CURPFirma").val(data.DatosContrato.CURPFirma);
                                CalcularExhibiciones();
                            }
                        }
                    }
                }
           }
        }
    });
}

function resultadobusqueda(strClase, strMensaje){
    $("#frmCrearContrato").hide();
    window.document.getElementById("NumeroBuscarEmpleado").value = "";
    window.document.getElementById("strMensaje").className = strClase; 
    window.document.getElementById("strMensaje").innerHTML = strMensaje;
    $("#strMensaje").show();
}