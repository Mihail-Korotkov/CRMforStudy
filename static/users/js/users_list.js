// users_list.js - ТОЛЬКО НЕОБХОДИМЫЙ МИНИМУМ

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // 1. СОРТИРОВКА (отправка GET-запроса)
    // ============================================
    const sortSelect = document.getElementById('sortSelect');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const urlParams = new URLSearchParams(window.location.search);
            const currentFilter = urlParams.get('filter') || 'all';
            const searchQuery = urlParams.get('q') || '';
            const sortValue = this.value;
            
            let params = [];
            
            if (sortValue && sortValue !== 'id') {
                params.push('sort=' + sortValue);
            }
            if (currentFilter && currentFilter !== 'all') {
                params.push('filter=' + currentFilter);
            }
            if (searchQuery) {
                params.push('q=' + encodeURIComponent(searchQuery));
            }
            
            let url = window.location.pathname;
            if (params.length > 0) {
                url += '?' + params.join('&');
            }
            
            window.location.href = url;
        });
    }

    // ============================================
    // 2. АВТОПОИСК (отправка формы при вводе)
    // ============================================
    const searchInput = document.getElementById('searchInput');
    const searchForm = searchInput ? searchInput.closest('form') : null;
    
    if (searchInput && searchForm) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchForm.submit();
            }, 500);
        });
    }

    // ============================================
    // 3. ПОДСВЕТКА АКТИВНОЙ КНОПКИ (дополнительно)
    // ============================================
    // Кнопки уже подсвечиваются через класс active в Django
    // Но если нужно переключение вручную:
    const filterTabs = document.querySelectorAll('.filter-tab');
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            // Убираем active у всех
            filterTabs.forEach(t => t.classList.remove('active'));
            // Добавляем active текущей
            this.classList.add('active');
            // Ссылка сама перезагрузит страницу с параметром filter
        });
    });

    console.log('✅ users_list.js загружен (только UI)');
});