document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.body;
    const collapseBtn = document.getElementById("sidebarCollapseBtn");

    if (!collapseBtn) return;

    const STORAGE_KEY = "nafi_sidebar_collapsed";

    // Apply collapsed / expanded state
    function setSidebarState(collapsed) {
        sidebar.classList.toggle("sidebar-collapsed", collapsed);

        collapseBtn.setAttribute(
            "aria-label",
            collapsed ? "Expand sidebar" : "Collapse sidebar"
        );

        collapseBtn.setAttribute(
            "title",
            collapsed ? "Expand sidebar" : "Collapse sidebar"
        );

        const icon = collapseBtn.querySelector("i");

        if (icon) {
            icon.className = collapsed
                ? "bi bi-chevron-right"
                : "bi bi-chevron-left";
        }

        try {
            localStorage.setItem(STORAGE_KEY, collapsed ? "true" : "false");
        } catch (error) {
            // Continue without saving the preference.
        }
    }

    // Restore previous sidebar state
    let savedState = false;

    try {
        savedState = localStorage.getItem(STORAGE_KEY) === "true";
    } catch (error) {
        savedState = false;
    }

    setSidebarState(savedState);

    // Toggle sidebar on button click
    collapseBtn.addEventListener("click", function () {
        const isCollapsed = sidebar.classList.contains("sidebar-collapsed");
        setSidebarState(!isCollapsed);
    });

    // Add tooltips to menu links for collapsed mode
    document.querySelectorAll(".sidebar-menu a").forEach(function (link) {
        const label = link.querySelector("span");

        if (label && label.textContent.trim()) {
            link.setAttribute("title", label.textContent.trim());
        }
    });

    // Profile and logout tooltips
    const profile = document.querySelector(".sidebar-profile");
    const profileName = document.querySelector(".sidebar-profile-name");

    if (profile && profileName) {
        profile.setAttribute("title", profileName.textContent.trim());
    }

    const logoutBtn = document.querySelector(".logout-btn");

    if (logoutBtn) {
        logoutBtn.setAttribute("title", "Logout");
    }
});