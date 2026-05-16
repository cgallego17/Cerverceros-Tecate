/**
 * Sistema de búsqueda y filtros para tablas del panel
 * Reutilizable para todas las tablas
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('tableSearch');
    const filterEstado = document.getElementById('filterEstado');
    const filterActivo = document.getElementById('filterActivo');
    const clearBtn = document.getElementById('clearFilters');
    const table = document.getElementById('dataTable');
    const noResults = document.getElementById('noResults');
    
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    
    // Función principal de filtrado
    function filterTable() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const estadoFilter = filterEstado ? filterEstado.value.toLowerCase() : '';
        const activoFilter = filterActivo ? filterActivo.value.toLowerCase() : '';
        
        let visibleCount = 0;
        
        rows.forEach(row => {
            const ciudad = row.dataset.ciudad || '';
            const estado = row.dataset.estado || '';
            const pais = row.dataset.pais || '';
            const activo = row.dataset.activo || '';
            
            // Búsqueda en texto
            const matchesSearch = !searchTerm || 
                ciudad.includes(searchTerm) || 
                estado.includes(searchTerm) || 
                pais.includes(searchTerm);
            
            // Filtro por estado
            const matchesEstado = !estadoFilter || estado === estadoFilter;
            
            // Filtro por activo/inactivo
            const matchesActivo = !activoFilter || activo === activoFilter;
            
            // Mostrar/ocultar fila
            if (matchesSearch && matchesEstado && matchesActivo) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Mostrar/ocultar mensaje de "sin resultados"
        if (table && noResults) {
            if (visibleCount === 0) {
                table.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                table.style.display = '';
                noResults.style.display = 'none';
            }
        }
        
        // Mostrar/ocultar botón de limpiar
        if (clearBtn) {
            if (searchTerm || estadoFilter || activoFilter) {
                clearBtn.style.display = 'inline-flex';
            } else {
                clearBtn.style.display = 'none';
            }
        }
    }
    
    // Event listeners
    if (searchInput) {
        searchInput.addEventListener('input', filterTable);
    }
    
    if (filterEstado) {
        filterEstado.addEventListener('change', filterTable);
    }
    
    if (filterActivo) {
        filterActivo.addEventListener('change', filterTable);
    }
    
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            if (searchInput) searchInput.value = '';
            if (filterEstado) filterEstado.value = '';
            if (filterActivo) filterActivo.value = '';
            filterTable();
        });
    }
    
    // Eliminar duplicados del select de estados
    if (filterEstado) {
        const options = Array.from(filterEstado.options);
        const seen = new Set();
        options.forEach(option => {
            if (option.value && seen.has(option.value)) {
                option.remove();
            } else if (option.value) {
                seen.add(option.value);
            }
        });
    }
});
