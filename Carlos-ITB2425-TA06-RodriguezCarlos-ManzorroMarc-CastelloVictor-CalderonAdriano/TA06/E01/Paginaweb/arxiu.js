document.addEventListener("DOMContentLoaded", function() {
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            // Insertar datos en la lista de años lluviosos pasados
            const lluviososPasados = document.getElementById('lluviosos-pasados');
            data.lluviosos_pasados.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Año: ${item.anio}, Precipitación: ${item.total_precipitacion} L/m²`;
                lluviososPasados.appendChild(li);
            });

            // Insertar datos en la lista de años secos pasados
            const secosPasados = document.getElementById('secos-pasados');
            data.secos_pasados.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Año: ${item.anio}, Precipitación: ${item.total_precipitacion} L/m²`;
                secosPasados.appendChild(li);
            });

            // Insertar datos en la lista de años lluviosos futuros
            const lluviososFuturos = document.getElementById('lluviosos-futuros');
            data.lluviosos_futuros.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Año: ${item.anio}, Precipitación: ${item.total_precipitacion} L/m²`;
                lluviososFuturos.appendChild(li);
            });

            // Insertar datos en la lista de años secos futuros
            const secosFuturos = document.getElementById('secos-futuros');
            data.secos_futuros.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Año: ${item.anio}, Precipitación: ${item.total_precipitacion} L/m²`;
                secosFuturos.appendChild(li);
            });
        })
        .catch(error => console.error('Error al cargar los datos:', error));
});