// Открыть модальное окно
function openModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

// Закрыть модальное окно
function closeModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}

// Закрыть модальное окно при клике на крестик
var closeBtn = document.querySelector(".close");
if (closeBtn) {
  closeBtn.onclick = closeModal;
}

// Закрыть модальное окно при клике вне окна
window.onclick = function(event) {
  var modal = document.getElementById("myModal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// Добавьте обработчик события для кнопки "Контакты"
var contactBtn = document.querySelector("nav ul li a[href='#contact']");
if (contactBtn) {
  contactBtn.addEventListener("click", openModal);
}


