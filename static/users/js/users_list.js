// ========== ФИЛЬТРАЦИЯ ==========
const filterTabs = document.querySelectorAll('.filter-tab');
const userItems = document.querySelectorAll('.user-item');
const searchInput = document.getElementById('searchInput');

// Функция фильтрации
function filterUsers() {
  const activeFilter = document.querySelector('.filter-tab.active');
  const filter = activeFilter ? activeFilter.dataset.filter : 'all';
  const searchText = searchInput.value.toLowerCase().trim();

  let visibleCount = 0;
  let leadersCount = 0;
  let newCount = 0;

  userItems.forEach(item => {
    const name = item.dataset.name.toLowerCase();
    const badge = item.dataset.badge;
    let show = true;

    // Фильтр по категории
    if (filter === 'leaders' && badge !== 'leader') {
      show = false;
    } else if (filter === 'new' && badge !== 'new') {
      show = false;
    }

    // Поиск по имени
    if (show && searchText && !name.includes(searchText)) {
      show = false;
    }

    // Показываем/скрываем
    if (show) {
      item.classList.remove('hidden');
      visibleCount++;

      // Считаем статистику для обновления
      if (badge === 'leader') leadersCount++;
      if (badge === 'new') newCount++;
    } else {
      item.classList.add('hidden');
    }
  });

  // Обновляем счётчики статистики
  document.getElementById('totalUsers').textContent = visibleCount;
  document.getElementById('totalLeaders').textContent = leadersCount;
  document.getElementById('totalNew').textContent = newCount;
}

// Переключение вкладок
filterTabs.forEach(tab => {
  tab.addEventListener('click', function() {
    filterTabs.forEach(t => t.classList.remove('active'));
    this.classList.add('active');
    filterUsers();
  });
});

// Поиск
searchInput.addEventListener('input', filterUsers);

// ========== СОРТИРОВКА ==========
const sortSelect = document.getElementById('sortSelect');
const usersList = document.getElementById('usersList');

sortSelect.addEventListener('change', function() {
  const sortValue = this.value;
  const items = Array.from(userItems);

  items.sort((a, b) => {
    const nameA = a.dataset.name;
    const nameB = b.dataset.name;
    const progressA = parseFloat(a.dataset.progress);
    const progressB = parseFloat(b.dataset.progress);
    const tasksA = parseInt(a.dataset.tasks);
    const tasksB = parseInt(b.dataset.tasks);

    switch (sortValue) {
      case 'name':
        return nameA.localeCompare(nameB);
      case 'progress-desc':
        return progressB - progressA;
      case 'progress-asc':
        return progressA - progressB;
      case 'tasks':
        return tasksB - tasksA;
      default:
        return 0;
    }
  });

  // Перемещаем отсортированные элементы
  items.forEach(item => usersList.appendChild(item));
});

// ========== КЛИК ПО ПОЛЬЗОВАТЕЛЮ ==========
userItems.forEach(item => {
  item.addEventListener('click', function() {
    const name = this.dataset.name;
    // Здесь можно добавить переход на страницу профиля
    // window.location.href = '/profile/' + encodeURIComponent(name);
    console.log('Переход к профилю:', name);
  });
});

// ========== ИНИЦИАЛИЗАЦИЯ ==========
// Обновляем статистику при загрузке
filterUsers();