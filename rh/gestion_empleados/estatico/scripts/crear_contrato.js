$gmx(document).ready(function(){
    $("#Estado option[value = 9]").attr("selected",true);
    $("#Municipio option[value = 3]").attr("selected",true);
    $("#FechaInicio").blur(ValidarContratos)
    $("#FechaInicio").datepicker({ dateFormat: 'dd/mm/yy', changeYear: true, changeMonth: true });
    $("#FechaFin").datepicker({ dateFormat: 'dd/mm/yy', changeYear: true, changeMonth: true });
    $("#FechaFirma").datepicker({ dateFormat: 'dd/mm/yy', changeYear: true, changeMonth: true });
    $("#btnCrearContrato").click(Guardar);
   // $("#btnCrearContrato").click(function (event) {Guardar()});
    
});

function Guardar(){
    if (validarFormulario($("#frmCrearContrato")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/guardar_empleado_contrato",
            data: $("#frmCrearContrato").serialize(),
            success: function(data){
                alert(data.respuesta);
            }
        });
    }
}
function ValidarContratos(){
    $("#FechaFirma").val($("#FechaInicio").val());
}

function funcionSeleccionar() {
    filtrar_formulario();
}
function filtrar_formulario(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/validar_empleado_contrato",
        data: $("#frmBE").serialize(),
        success: function(data){
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
                            window.document.getElementById("strMensaje").className = ""; 
                            window.document.getElementById("strMensaje").innerHTML = "";
                            $("#strMensaje").hide();                            
                            $("#tablaEmpleadoSeleccionado").show();
                            $("#frmCrearContrato").show();
                            $("#MontoPactado").val(data.sueldo);
                            $("#ConocimientoExperiencia").val(data.conocimiento);
                            $("#ConocimientoPrestador").val(data.conocimiento);
                            $("#Actividades").val(data.conocimiento);
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