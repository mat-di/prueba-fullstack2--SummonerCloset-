const limpiar = document.getElementById('limpiar-filtros');
const buscadorInput = document.getElementById('buscador-input');
const rol_top = document.getElementById('top');
const rol_jungle = document.getElementById('jungle');
const rol_mid = document.getElementById('mid');
const rol_bot = document.getElementById('bot');
const rol_supp = document.getElementById('supp');

function limpiarFiltros(){
    buscadorInput.value = '';
}