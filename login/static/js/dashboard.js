let profileDropdownList = document.querySelector(".profile-dropdown-list");
let btn = document.querySelector(".profile-dropdown-btn");

let classList = profileDropdownList.classList;

const toggle = () => classList.toggle("active");

window.addEventListener("click", function (e) {
    if (!btn.contains(e.target)) classList.remove("active");
});

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth'
    });

    calendar.render();
});
document.addEventListener("DOMContentLoaded", function() {
    const sections = document.querySelectorAll('.section');
    
    sections.forEach(section => {
        section.addEventListener('click', () => {
            alert(`seleccionaste ${section.querySelector('h2').textContent}`);
        });
    });
});
