document.addEventListener('DOMContentLoaded', function() {
    let themeIcon = document.getElementById('theme-icon');
    let navbar = document.getElementById('mainNav');
    let footer = document.getElementById('mainFooter');

    if (!themeIcon || !navbar || !footer) {
        console.error("Theme elements not found in the DOM.");
        return; // Exit if elements are not found
    }

    function setTheme(theme) {
        let body = document.body;

        body.classList.remove('dark-theme');
        navbar.classList.remove('navbar-dark', 'bg-dark', 'navbar-light', 'bg-light');
        footer.classList.remove('bg-dark', 'bg-light');

        if (theme === 'dark') {
            body.classList.add('dark-theme');
            navbar.classList.add('navbar-dark', 'bg-dark');
            footer.classList.add('bg-dark');
            footer.querySelector('span').classList.add('text-light');
            themeIcon.className = "bi bi-moon-stars-fill";
        } else if (theme === 'light') {
            navbar.classList.add('navbar-light', 'bg-light');
            footer.classList.add('bg-light');
            footer.querySelector('span').classList.remove('text-light');
            themeIcon.className = "bi bi-sun-fill";
        } else if (theme === 'system') {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                body.classList.add('dark-theme');
                navbar.classList.add('navbar-dark', 'bg-dark');
                footer.classList.add('bg-dark');
                footer.querySelector('span').classList.add('text-light');
                themeIcon.className = "bi bi-moon-stars-fill";
            } else {
                navbar.classList.add('navbar-light', 'bg-light');
                footer.classList.add('bg-light');
                footer.querySelector('span').classList.remove('text-light');
                themeIcon.className = "bi bi-sun-fill";
            }
        }
        localStorage.setItem('theme', theme);
        document.documentElement.setAttribute('data-bs-theme', theme);
    }

    function toggleTheme() {
        let currentTheme = localStorage.getItem('theme') || 'system';
        let newTheme;

        if (currentTheme === 'system') {
            newTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark';
        } else if (currentTheme === 'dark') {
            newTheme = 'light';
        } else {
            newTheme = 'system';
        }
        setTheme(newTheme);
    }

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        setTheme('system');
    }

    themeIcon.addEventListener('click', toggleTheme);
    themeIcon.addEventListener('mouseover', function() {
        themeIcon.style.cursor = 'pointer';
    });
});