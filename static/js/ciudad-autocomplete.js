/**
 * Select con búsqueda integrada para el campo de ciudad
 * Convierte el select en un combobox con filtrado en tiempo real
 */

document.addEventListener('DOMContentLoaded', function() {
    const ciudadSelect = document.querySelector('.ciudad-autocomplete');
    
    if (!ciudadSelect) return;
    
    // Crear contenedor personalizado
    const wrapper = document.createElement('div');
    wrapper.className = 'select-autocomplete-wrapper';
    wrapper.style.position = 'relative';
    wrapper.style.width = '100%';
    
    // Crear input de búsqueda que reemplaza visualmente el select
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'panel-input';
    searchInput.placeholder = 'Buscar ciudad... (ej: Tecate, Tijuana, Monterrey)';
    searchInput.autocomplete = 'off';
    
    // Crear dropdown de opciones
    const dropdown = document.createElement('div');
    dropdown.className = 'select-autocomplete-dropdown';
    dropdown.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        max-height: 300px;
        overflow-y: auto;
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        margin-top: 4px;
        display: none;
        z-index: 1000;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    `;
    
    // Ocultar select original
    ciudadSelect.style.display = 'none';
    
    // Insertar wrapper y elementos
    ciudadSelect.parentNode.insertBefore(wrapper, ciudadSelect);
    wrapper.appendChild(searchInput);
    wrapper.appendChild(dropdown);
    wrapper.appendChild(ciudadSelect);
    
    // Guardar todas las opciones
    const allOptions = Array.from(ciudadSelect.options).slice(1);
    
    // Función para renderizar opciones
    function renderOptions(filter = '') {
        dropdown.innerHTML = '';
        const term = filter.toLowerCase().trim();
        
        const filtered = term ? 
            allOptions.filter(opt => opt.textContent.toLowerCase().includes(term)) : 
            allOptions;
        
        if (filtered.length === 0) {
            const noResult = document.createElement('div');
            noResult.textContent = 'No se encontraron ciudades';
            noResult.style.cssText = 'padding: 0.75rem; color: #6b7280; font-style: italic;';
            dropdown.appendChild(noResult);
            return;
        }
        
        filtered.forEach(option => {
            const item = document.createElement('div');
            item.textContent = option.textContent;
            item.dataset.value = option.value;
            item.style.cssText = `
                padding: 0.75rem;
                cursor: pointer;
                transition: background-color 0.15s;
            `;
            
            item.addEventListener('mouseenter', () => {
                item.style.backgroundColor = '#f3f4f6';
            });
            
            item.addEventListener('mouseleave', () => {
                item.style.backgroundColor = 'white';
            });
            
            item.addEventListener('click', () => {
                ciudadSelect.value = option.value;
                searchInput.value = option.textContent;
                dropdown.style.display = 'none';
            });
            
            dropdown.appendChild(item);
        });
    }
    
    // Mostrar dropdown al hacer clic en el input
    searchInput.addEventListener('focus', () => {
        renderOptions(searchInput.value);
        dropdown.style.display = 'block';
    });
    
    // Filtrar mientras se escribe
    searchInput.addEventListener('input', (e) => {
        renderOptions(e.target.value);
        dropdown.style.display = 'block';
    });
    
    // Cerrar dropdown al hacer clic fuera
    document.addEventListener('click', (e) => {
        if (!wrapper.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
    
    // Si hay valor pre-seleccionado, mostrarlo
    if (ciudadSelect.value) {
        const selected = ciudadSelect.options[ciudadSelect.selectedIndex];
        searchInput.value = selected.textContent;
    }
});
