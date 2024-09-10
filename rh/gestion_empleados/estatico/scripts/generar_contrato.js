$gmx(document).ready(function(){
    //$("#btnGenerarContrato").click(generar_contrato);
    $("#btnConfirmarContrato").click(modal_modificar_contrato);
    $("#btnGuardarContrato").click(Guardar);
    $("#btnGenerarContrato").click(ProcesandoGenerarContrato);
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
    obtenerDatosContrato();
}

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
    obtenerDatosContrato();
}

function obtenerDatosContrato(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/validar_empleado_contrato",
        data: $("#frmBE").serialize(),
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