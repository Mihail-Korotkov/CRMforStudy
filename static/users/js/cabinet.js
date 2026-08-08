// ========== УВЕДОМЛЕНИЯ ==========
function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  const toastMessage = document.getElementById('toastMessage');
  toastMessage.textContent = message;
  toast.className = 'toast' + (isError ? ' error' : '');
  toast.classList.add('show');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// ========== ЗАГРУЗКА АВАТАРА ==========
const avatarInput = document.getElementById('avatarInput');
const avatarPreview = document.getElementById('avatarPreview');

avatarInput.addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(event) {
      avatarPreview.innerHTML = `<img src="${event.target.result}" alt="Аватар" />`;
      showToast('Аватар обновлён');
    };
    reader.readAsDataURL(file);
  }
});

// ========== ИЗМЕНЕНИЕ ИМЕНИ ==========
const nameInput = document.getElementById('nameInput');
const displayName = document.getElementById('displayName');
const saveNameBtn = document.getElementById('saveNameBtn');

saveNameBtn.addEventListener('click', function() {
  const newName = nameInput.value.trim();
  if (newName) {
    displayName.textContent = newName;
    showToast('Имя обновлено');
  } else {
    showToast('Имя не может быть пустым', true);
  }
});

nameInput.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') saveNameBtn.click();
});

// ========== ИЗМЕНЕНИЕ РОЛИ ==========
const roleInput = document.getElementById('roleInput');
const displayRole = document.getElementById('displayRole');
const saveRoleBtn = document.getElementById('saveRoleBtn');

saveRoleBtn.addEventListener('click', function() {
  const newRole = roleInput.value.trim();
  if (newRole) {
    displayRole.textContent = newRole;
    showToast('Роль обновлена');
  } else {
    showToast('Роль не может быть пустой', true);
  }
});

roleInput.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') saveRoleBtn.click();
});

// ========== СМЕНА EMAIL ==========
const newEmailInput = document.getElementById('newEmailInput');
const confirmEmailInput = document.getElementById('confirmEmailInput');
const changeEmailBtn = document.getElementById('changeEmailBtn');
const currentEmail = document.getElementById('currentEmail');

changeEmailBtn.addEventListener('click', function() {
  const email = newEmailInput.value.trim();
  const confirm = confirmEmailInput.value.trim();

  if (!email || !email.includes('@')) {
    showToast('Введите корректный email', true);
    return;
  }
  if (email !== confirm) {
    showToast('Email не совпадают', true);
    return;
  }
  if (email === currentEmail.textContent) {
    showToast('Этот email уже используется', true);
    return;
  }

  currentEmail.textContent = email;
  newEmailInput.value = '';
  confirmEmailInput.value = '';
  showToast('Email успешно обновлён');
});

// ========== СМЕНА ПАРОЛЯ ==========
const newPasswordInput = document.getElementById('newPasswordInput');
const confirmPasswordInput = document.getElementById('confirmPasswordInput');
const changePasswordBtn = document.getElementById('changePasswordBtn');

changePasswordBtn.addEventListener('click', function() {
  const password = newPasswordInput.value.trim();
  const confirm = confirmPasswordInput.value.trim();

  if (password.length < 8) {
    showToast('Пароль должен содержать минимум 8 символов', true);
    return;
  }
  if (password !== confirm) {
    showToast('Пароли не совпадают', true);
    return;
  }

  newPasswordInput.value = '';
  confirmPasswordInput.value = '';
  showToast('Пароль успешно изменён');
});

// ========== ПОКАЗ/СКРЫТИЕ ПАРОЛЯ ==========
document.querySelectorAll('.toggle-pw').forEach(button => {
  button.addEventListener('click', function() {
    const input = this.closest('.password-wrapper').querySelector('input');
    const icon = this.querySelector('i');
    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
      input.type = 'password';
      icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
  });
});

// ========== СОЦИАЛЬНЫЕ СЕТИ ==========
document.querySelectorAll('.save-social').forEach(btn => {
  btn.addEventListener('click', function() {
    const field = this.dataset.field;
    const input = document.getElementById(field + 'Input');
    const url = input.value.trim();
    if (url) {
      showToast(`${field.charAt(0).toUpperCase() + field.slice(1)} ссылка сохранена`);
    } else {
      showToast('Введите ссылку', true);
    }
  });
});

// ========== УПРАВЛЕНИЕ ЗАДАЧАМИ ==========
const taskList = document.getElementById('taskList');
const taskInput = document.getElementById('taskInput');
const addTaskBtn = document.getElementById('addTaskBtn');

function addTask(taskName, status = 'pending') {
  if (!taskName.trim()) {
    showToast('Введите название задачи', true);
    return;
  }

  const taskItem = document.createElement('div');
  taskItem.className = `task-item ${status}`;

  const statusIcons = {
    done: '<i class="fas fa-check-circle"></i>',
    'in-progress': '<i class="fas fa-spinner fa-pulse"></i>',
    pending: '<i class="fas fa-hourglass-half"></i>'
  };

  const statusLabels = {
    done: 'Завершено',
    'in-progress': 'В процессе',
    pending: 'Ожидает выполнения'
  };

  taskItem.innerHTML = `
    <span class="task-icon">${statusIcons[status]}</span>
    <div class="task-info">
      <span class="task-name">${taskName}</span>
      <span class="task-date">${statusLabels[status]}</span>
    </div>
    <div class="task-actions">
      <button class="btn-start"><i class="fas fa-play"></i> Начать</button>
      <button class="btn-done"><i class="fas fa-check"></i> Выполнено</button>
      <button class="btn-delete"><i class="fas fa-trash"></i></button>
    </div>
  `;

  updateTaskButtons(taskItem, status);

  taskItem.querySelector('.btn-start').addEventListener('click', function() {
    const item = this.closest('.task-item');
    if (!item.classList.contains('in-progress')) {
      item.classList.remove('pending', 'done');
      item.classList.add('in-progress');
      updateTaskIconsAndDate(item, 'in-progress');
      updateTaskButtons(item, 'in-progress');
    }
  });

  taskItem.querySelector('.btn-done').addEventListener('click', function() {
    const item = this.closest('.task-item');
    if (!item.classList.contains('done')) {
      item.classList.remove('pending', 'in-progress');
      item.classList.add('done');
      updateTaskIconsAndDate(item, 'done');
      updateTaskButtons(item, 'done');
    }
  });

  taskItem.querySelector('.btn-delete').addEventListener('click', function() {
    this.closest('.task-item').remove();
    showToast('Задача удалена');
  });

  taskList.prepend(taskItem);
  taskInput.value = '';
  showToast('Задача добавлена');
}

function updateTaskIconsAndDate(item, status) {
  const icon = item.querySelector('.task-icon');
  const dateSpan = item.querySelector('.task-date');
  const icons = {
    done: '<i class="fas fa-check-circle"></i>',
    'in-progress': '<i class="fas fa-spinner fa-pulse"></i>',
    pending: '<i class="fas fa-hourglass-half"></i>'
  };
  const labels = {
    done: 'Завершено только что',
    'in-progress': 'В процессе',
    pending: 'Ожидает выполнения'
  };
  icon.innerHTML = icons[status];
  dateSpan.textContent = labels[status];
}

function updateTaskButtons(item, status) {
  const startBtn = item.querySelector('.btn-start');
  const doneBtn = item.querySelector('.btn-done');

  if (status === 'done') {
    startBtn.style.display = 'none';
    doneBtn.style.display = 'none';
  } else if (status === 'in-progress') {
    startBtn.style.display = 'none';
    doneBtn.style.display = 'inline-block';
  } else {
    startBtn.style.display = 'inline-block';
    doneBtn.style.display = 'none';
  }
}

addTaskBtn.addEventListener('click', function() {
  addTask(taskInput.value, 'pending');
});

taskInput.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    addTaskBtn.click();
  }
});

document.querySelectorAll('.task-item').forEach(item => {
  const classes = item.className;
  if (classes.includes('done')) {
    updateTaskButtons(item, 'done');
  } else if (classes.includes('in-progress')) {
    updateTaskButtons(item, 'in-progress');
  } else {
    updateTaskButtons(item, 'pending');
  }
});