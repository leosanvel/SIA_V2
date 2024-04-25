// Para validar formularios, el HTML debe cumplir con lo siguiente:
// El input a verificar deberá tener AL MENOS UNA de las clases:
//     obligatorio
//     RFC
//     CURP
//     email
//     fecha
// La etiqueta de error debe estar inmediatamente despues del elemento input a verificar,
// y deberá contener la clase "etiquetaError" como primera clase.
// por ejemplo: 
//    <input type="text" id="CURP" class="obligatorio CURP form-control" placeholder="CURP" maxlength="18", value="{{empleado.CURP}}">
//    <small id="ECURP" class="etiquetaError form-text form-text-error"></small>
// Si se desea agregar una nueva validación, se agrega la función en el archivo validaciones.js

function validarFormulario(formulario) {
    let primerCampoInvalido = null;
    let primerCampoInvalidoTab = null;
    let encontradoInvalido = false;
    let hayCamposOpcionales = false;

    formulario.find(":input").each(function () { // Revisa elementos <input>, <textarea>, <select>, <button>,etc.
        const campo = $(this);
        const clases = campo.attr("class");
        const errorContainer = campo.nextAll(".etiquetaError");
        const tabId = campo.closest(".tab-pane").attr("id");

        if (clases) {
            const clasesArray = clases.split(" ");

            for (const clase of clasesArray) {
                const validador = validadores[clase];

                if (validador) {
                    campo.removeClass("form-control-error");
                    if (!validador(campo, errorContainer)) {
                        campo.addClass("form-control-error");
                        if (!encontradoInvalido) {
                            primerCampoInvalido = campo;
                            primerCampoInvalidoTab = tabId;
                            encontradoInvalido = true;
                        }

                    }

                    // Verifica si el campo es opcional
                    if (clase === "opcional" && campo.val() === "") {
                        hayCamposOpcionales = true;
                    }

                }
            }
        }
    });

    if (encontradoInvalido && primerCampoInvalido !== null) {
        // Encuentra la pestaña que contiene el campo inválido y ábrela
        $("a[data-toggle='tab'][href='#" + primerCampoInvalidoTab + "']").tab("show");
        primerCampoInvalido.focus();
        $("#AlertaError").show();
    } else {
        $("#AlertaError").hide();
    }
    return {
        valido: !encontradoInvalido,
        camposOpcionales: hayCamposOpcionales
    };
}

const validadores = {
    "obligatorio": validarObligatorio,
    "opcional": validarOpcional,
    "RFC": validarRFC,
    "email": validarCorreo,
    "CURP": validarCURP,
    "fecha": validarFecha,
    "telefono": validarTelefono,
    "clabe": validarClabe
    // Agrega más validadores según necesites
};

function validarObligatorio(elemento, error) {

    if (elemento.val() === null || elemento.val().trim() === "" || (elemento.is("select") && elemento.val() === "0")) {
        error.text("Este campo es obligatorio");
        return false;
    }
    error.text("");
    return true;

}

function validarCorreo(elemento, error) {
    if (elemento.val() !== null && elemento.val().trim() !== "") {
        // if (/^[\w.-]+@\w+\.\w+$/.test(elemento.val())) {
        if (/^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$/.test(elemento.val())) {
            error.text("");
            return true;
        } else {
            error.text("No es una dirección válida");
            return false;
        }
    } else {
        return true;
    }
}

function validarCURP(elemento, error) {
    if (elemento.val() !== null && elemento.val().trim() !== "") {
        if (/^([a-z]{4})(\d{6})([a-z]{6})(\d{2})$/i.test(elemento.val())) {
            error.text("");
            return true;
        } else {
            error.text("El formato del CURP es inválido");
            return false;
        }
    }
}

function validarRFC(elemento, error) {
    if (elemento.val() !== null && elemento.val().trim() !== "") {

        if (/^([a-z]{3,4})(\d{2})(\d{2})(\d{2})([0-9a-z]{3})$/i.test(elemento.val())) {
            error.text("");
            return true;
        } else {
            error.text("El formato del RFC es inválido");
            return false;
        }
    } else {
        return true;
    }
}

function validarFecha(elemento, error) {
    if (elemento.val() !== null && elemento.val().trim() !== "") {
        if (/^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/.test(elemento.val())) {
            error.text("");
            return true;
        } else {
            error.text("El formato de la fecha es inválido. Debe ser 'dd/mm/yyyy'");
            return false;
        }
    } else {
        return true;
    }
}

function validarTelefono(elemento, error) {
    if (elemento.val() !== null && elemento.val().trim() !== "") {
        const regexTelefono = /^\d{10}$/;
        if (regexTelefono.test(elemento.val())) {
            error.text("");
            return true;
        } else {
            error.text("El formato de teléfono es inválido.");
            return false;
        }
    }
}

function validarNumeroDeTelefono(numero) {
    // Expresión regular que verifica si el número de teléfono tiene 10 dígitos.
    const regexTelefono = /^\d{10}$/;
    return regexTelefono.test(numero);
}

function validarClabe(elemento, error) {
    if (elemento.val() !== null && elemento.val().trim() !== "") {
        if (/^\d{18}$/.test(elemento.val())) {
            error.text("");
            return true;
        } else {
            error.text("El formato de la Clabe es inválido.");
            return false;
        }
    }else{
        return true;
    }
}

function validarOpcional(elemento, error) {
    // Si el campo está vacío, no se muestra ningún mensaje de error y se devuelve true para indicar que la validación pasó
    if (elemento.val() === null || elemento.val().trim() === "" || (elemento.is("select") && elemento.val() === "0")) {
        error.text("Este campo es opcional, la información puede ser completada más adelante.");
        return true;
    }
    // Si el campo no está vacío, se muestra un mensaje indicando que la información puede ser completada más adelante
    error.text("");
    return true; // Se devuelve true para indicar que la validación pasó
}

function abrirModal(titulo, contenido, comportamiento) {

    // Modificar el contenido del modal
    document.getElementById('tituloModal').textContent = titulo;
    document.getElementById('contenidoModal').innerHTML = contenido;
    $('#myModal').attr('data-comportamiento', comportamiento);

    // Abrir el modal
    $('#myModal').modal('show');
}

function formularioVacio(formulario) {
    var campos = formulario.find('input, textarea, select');
    for (var i = 0; i < campos.length; i++) {
        var campo = campos[i];
        if (campo.type === 'checkbox') {
            if (campo.checked) {
                return false; // El formulario no está vacío
            }
        } else if (campo.type === 'radio') {
            if (formulario.find('input[type="radio"]:checked').length > 0) {
                return false; // El formulario no está vacío
            }
        } else if (campo.tagName === 'SELECT') {
            if ((campo.value !== '0') && (campo.value !== '')) {
                return false; // El formulario no está vacío (excluye select con valor "0")
            }
        } else {
            if (campo.value.trim() !== '') {
                return false; // El formulario no está vacío
            }
        }
    }
    return true; // El formulario está vacío
}

function convertirFechaParaEnvio(fecha) {
    // convierte formato 'dd/mm/yy' a 'YYYY-MM-DD' para la base de datos
    var partes = fecha.split('/');
    if (partes.length === 3) {
        var anio = partes[2];
        var mes = partes[1];
        var dia = partes[0];
        return anio + '-' + mes + '-' + dia;
    } else {
        return fecha; // En caso de que la fecha no sea válida
    }
}

function convertirFechaParaVisualizacion(fecha) {
    var fechaObj = new Date(fecha);
    var dia = fechaObj.getUTCDate();
    var mes = fechaObj.getUTCMonth() + 1; // Sumar 1 al mes ya que los meses van de 0 a 11
    var anio = fechaObj.getUTCFullYear();
    dia = dia < 10 ? '0' + dia : dia;
    mes = mes < 10 ? '0' + mes : mes;
    return dia + '/' + mes + '/' + anio;
}

function cargarMenu(){
    $.ajax({
        type: "POST",
        url: "/general/cargar-menu",
        success: function (data) {
            var MenuUsuario = document.getElementById('MenuUsuario');
            MenuUsuario.insertAdjacentHTML('afterbegin', data);
        }
    });
}
$gmx(document).ready(function () {
    cargarMenu();

    $(".botonModalBuscaEmpleado").click(function (event) {
        $('#ModalBuscaEmpleado').modal('show');
    });

    $('#ModalBuscaEmpleado').on('shown.bs.modal', function () {
        $('#WParametro').focus();
    });

    $("#cierraAlertaTiempo").click(function (event) {
        $.ajax({
            type: "POST",  // Puedes usar "GET" si es apropiado
            url: "autenticacion/actualiza-sesion",  // La URL de la ruta que manejará la petición
            success: function (response) {

                $("#start-time").attr('data-start-time', response.nueva_hora_inicio);
                $("#AlertTiempo").css("display", "none");
            },
            error: function (xhr, status, error) {
                // Maneja errores si es necesario
                console.error('Error en la petición vacía:', status, error);
            }
        });
    });

    // Cerrar Mymodal
    $('#myModal').on('hidden.bs.modal', function (e) {
        var comportamiento = $('#myModal').attr('data-comportamiento');
        if (comportamiento === 'recargar') {
            // Recargar la página
            window.scrollTo(0, 0);
            window.location.reload();
        }
        if (comportamiento === 'modificarEmpleado') {
            // Recargar la página
            window.location.href = "/rh/gestion-empleados/modificar-empleado";
        }
        if (comportamiento === 'inicio') {
            // Recargar la página
            window.location.href = "/principal/sia";
        }

    });

    $.datepicker.regional.es = {
        closeText: 'Cerrar',
        prevText: 'Ant',
        nextText: 'Sig',
        currentText: 'Hoy',
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Mi&eacute;rcoles', 'Jueves', 'Viernes', 'S&aacute;bado'],
        dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mi&eacute;', 'Juv', 'Vie', 'S&aacute;b'],
        dayNamesMin: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'S&aacute;b'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional.es);

});