document.addEventListener('DOMContentLoaded', () => {
    const perros = document.getElementById('cantidad-perros');
    const gatos = document.getElementById('cantidad-gatos');
    const container = document.getElementById('mascotas-container');

    function crearCampos(tipo, cantidad) {
        for (let i = 1; i <= cantidad; i++) {
            const div = document.createElement('div');
            div.className = 'mascota';
            div.innerHTML = `
                <h3>${tipo} ${i}</h3>
                <input type="text" name="nombre_${tipo}_${i}" placeholder="Nombre del ${tipo}">
                <select name="servicio_${tipo}_${i}">
                    <option value="baño">Baño</option>
                    <option value="vacunación">Vacunación</option>
                    <option value="peluquería">Peluquería</option>
                    <option value="control">Control veterinario</option>
                </select>
            `;
            container.appendChild(div);
        }
    }

    function limpiarCampos() {
        container.innerHTML = '';
    }

    function generar() {
        limpiarCampos();
        crearCampos('perro', parseInt(perros.value) || 0);
        crearCampos('gato', parseInt(gatos.value) || 0);
    }

    perros.addEventListener('change', generar);
    gatos.addEventListener('change', generar);
});
