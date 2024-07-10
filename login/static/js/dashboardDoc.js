let profileDropdownList = document.querySelector(".navbar-list");
let btn = document.querySelector(".profile-dropdown-btn");

let classList = profileDropdownList.classList;

const toggle = () => classList.toggle("active");

window.addEventListener("click", function (e) {
    if (!btn.contains(e.target)) classList.remove("active");
});


document.addEventListener('DOMContentLoaded', (event) => {
  const items = document.querySelectorAll('.profile-dropdown-list-item');

  items.forEach(item => {
    item.addEventListener('mouseenter', () => {
      // Eliminar la clase hover de todos los items
      items.forEach(i => i.classList.remove('hover'));
      // Añadir la clase hover al item actual
      item.classList.add('hover');
    });
  });
});

document.addEventListener('DOMContentLoaded', (event) => {
  const items = document.querySelectorAll('.profile-dropdown-list-item');

  items.forEach(item => {
    let timer;
    
    item.addEventListener('mouseenter', () => {
      clearTimeout(timer);
      // Añadir la clase hover al item actual
      item.classList.add('hover');
    });

    item.addEventListener('mouseleave', () => {
      // Configurar el temporizador para eliminar la clase hover después de 2 segundos
      timer = setTimeout(() => {
        item.classList.remove('hover');
      }, 800);
    });
  });
});

const profileDropdownBtn = document.querySelector('.profile-dropdown-btn');

profileDropdownBtn.addEventListener('click', toggleCaption);

function toggleCaption() {
  profileDropdownBtn.classList.toggle('show-caption');
}

document.addEventListener('click', (event) => {
  const isClickInside = profileDropdownBtn.contains(event.target);
  if (!isClickInside) {
    profileDropdownBtn.classList.remove('show-caption');
  }
});
