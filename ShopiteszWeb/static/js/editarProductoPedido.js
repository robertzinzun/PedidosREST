
function incrementar(){
    var cantidad=parseInt(document.getElementById("cantidad").value);
    cantidad++;
    document.getElementById("cantidad").value=cantidad;
    calcularTotales();

}
function decrementar(){
    var cantidad=parseInt(document.getElementById("cantidad").value);
    if(cantidad>1)
        cantidad--;
    document.getElementById("cantidad").value=cantidad;
    calcularTotales();
}
function calcularTotales(){
    var cantidad=parseInt(document.getElementById("cantidad").value);
    var precio=parseFloat(document.getElementById("precio").textContent);
    var costoEnvio=parseFloat(document.getElementById("costoEnvio").textContent);
    var subtotal=cantidad*precio;
    var subtotalE=cantidad*costoEnvio;
    document.getElementById("subtotal").textContent=subtotal;
    document.getElementById("subtotalE").textContent=subtotalE;
}