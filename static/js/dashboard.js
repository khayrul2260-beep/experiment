"use strict";

/* ==========================================
   DOM READY
========================================== */

document.addEventListener("DOMContentLoaded", () => {
  sidebarToggle();

  activeMenu();

  searchBox();

  counterAnimation();
});

/* ==========================================
   SIDEBAR TOGGLE
========================================== */

function sidebarToggle() {
  const sidebar = document.querySelector(".sidebar");

  const toggle = document.querySelector(".sidebar-toggle");

  if (!sidebar || !toggle) return;

  toggle.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });
}

/* ==========================================
   ACTIVE MENU
========================================== */

function activeMenu() {
  const menuItems = document.querySelectorAll(".sidebar-menu li");

  menuItems.forEach((item) => {
    item.addEventListener("click", () => {
      menuItems.forEach((menu) => {
        menu.classList.remove("active");
      });

      item.classList.add("active");
    });
  });
}

/* ==========================================
   SEARCH BOX
========================================== */

function searchBox() {
  const searchInput = document.querySelector(".search-box input");

  if (!searchInput) return;

  searchInput.addEventListener("keyup", function () {
    console.log("Search :", this.value);
  });
}

/* ==========================================
   COUNTER ANIMATION
========================================== */

function counterAnimation() {
  const counters = document.querySelectorAll(".stat-content h2");

  counters.forEach((counter) => {
    const text = counter.innerText;

    const number = parseInt(text.replace(/\D/g, ""));

    if (isNaN(number)) return;

    let current = 0;

    const increment = Math.ceil(number / 80);

    const prefix = text.startsWith("$") ? "$" : "";

    const update = () => {
      current += increment;

      if (current >= number) {
        counter.innerText = prefix + number.toLocaleString();
      } else {
        counter.innerText = prefix + current.toLocaleString();

        requestAnimationFrame(update);
      }
    };

    update();
  });
}

/* ==========================================
   WINDOW RESIZE
========================================== */

window.addEventListener("resize", () => {
  if (window.innerWidth > 992) {
    document.querySelector(".sidebar")?.classList.remove("active");
  }
});

/* ==========================================
   END
========================================== */
