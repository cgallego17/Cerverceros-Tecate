/**
 * Autocomplete para el campo de ciudad en formulario de equipos
 * Permite búsqueda en tiempo real mientras el usuario escribe
 */

document.addEventListener('DOMContentLoaded', function() {
    const ciudadSelect = document.querySelector('.ciudad-autocomplete');
    
    if (!ciudadSelect) return;
    
    // Crear input de búsqueda
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'panel-input ciudad-search';
    searchInput.placeholder = 'Buscar ciudad... (ej: Tecate, Tijuana, Monterrey)';
    searchInput.style.marginBottom = '0.5rem';
    
    // Insertar input de búsqueda antes del select
    ciudadSelect.parentNode.insertBefore(searchInput, ciudadSelect);
    
    // Guardar todas las opciones originales
    const allOptions = Array.from(ciudadSelect.options).slice(1); // Excluir opción vacía
    
    // Función para filtrar opciones
    function filterOptions(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        
        // Limpiar select (mantener opción vacía)
        while (ciudadSelect.options.length > 1) {
            ciudadSelect.remove(1);
        }
        
        if (!term) {
            // Si no hay búsqueda, mostrar todas las opciones
            allOptions.forEach(option => {
                ciudadSelect.add(option.cloneNode(true));
            });
            return;
        }
        
        // Filtrar y agregar opciones que coincidan
        const filtered = allOptions.filter(option => {
            const text = option.textContent.toLowerCase();
            return text.includes(term);
        });
        
        filtered.forEach(option => {
            ciudadSelect.add(option.cloneNode(true));
        });
        
        // Mostrar mensaje si no hay resultados
        if (filtered.length === 0) {
            const noResults = document.createElement('option');
            noResults.textContent = 'No se encontraron ciudades';
            noResults.disabled = true;
            ciudadSelect.add(noResults);
        }
    }
    
    // Event listener para búsqueda en tiempo real
    searchInput.addEventListener('input', function(e) {
        filterOptions(e.target.value);
    });
    
    // Limpiar búsqueda cuando se selecciona una ciudad
    ciudadSelect.addEventListener('change', function() {
        if (ciudadSelect.value) {
            const selectedText = ciudadSelect.options[ciudadSelect.selectedIndex].textContent;
            searchInput.value = selectedText;
        }
    });
    
    // Si hay una ciudad pre-seleccionada, mostrarla en el input de búsqueda
    if (ciudadSelect.value) {
        const selectedText = ciudadSelect.options[ciudadSelect.selectedIndex].textContent;
        searchInput.value = selectedText;
    }
});
