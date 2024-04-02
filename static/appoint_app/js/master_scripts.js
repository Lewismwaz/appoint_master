document.addEventListener('DOMContentLoaded', function () {
    const sideMenu = document.querySelector("aside");
    const menuBtn = document.querySelector("#menu-btn");
    const closeBtn = document.querySelector("#close-btn");
    const themeToggler = document.querySelector(".theme-toggler");
    const logo = document.querySelector(".logo");

    // Function to toggle the theme
    function toggleTheme() {
        // Toggle between dark and light theme
        const currentTheme = document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // Save the new theme preference to localStorage
        localStorage.setItem('theme', newTheme);

        // Remove the current theme class and add the new one
        document.body.classList.remove(currentTheme + '-theme-variables');
        document.body.classList.add(newTheme + '-theme-variables');

        // Toggle the active class for the theme toggler button
        themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
        themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');

        // Update the logo based on the new theme
        if (newTheme === 'dark') {
            logo.innerHTML = ''; // Clear previous content
            const img = document.createElement('img');
            img.src = "/static/appoint_app/images/appoint-master-logo-dark.png"; // Adjust the URL accordingly
            logo.appendChild(img);

            const h2 = document.createElement('h2');
            h2.innerHTML = '<span class="logo-name">Appoint</span>Master';
            logo.appendChild(h2);
        } else {
            logo.innerHTML = ''; // Clear previous content
            const img = document.createElement('img');
            img.src = "/static/appoint_app/images/appoint-master-logo.png"; // Adjust the URL accordingly
            logo.appendChild(img);

            const h2 = document.createElement('h2');
            h2.innerHTML = '<span class="logo-name">Appoint</span>Master';
            logo.appendChild(h2);
        }

        console.log('Theme toggled to:', newTheme);
    }

    // Check if a theme preference is saved in localStorage
    const savedTheme = localStorage.getItem('theme');

    // If a theme preference is saved, apply it to the page
    if (savedTheme) {
        document.body.classList.add(savedTheme + '-theme-variables');
        console.log('Saved theme:', savedTheme);
        // Update the logo based on the saved theme
        if (savedTheme === 'dark') {
            logo.innerHTML = ''; // Clear previous content
            const img = document.createElement('img');
            img.src = "/static/appoint_app/images/appoint-master-logo-dark.png"; // Adjust the URL accordingly
            logo.appendChild(img);

            const h2 = document.createElement('h2');
            h2.innerHTML = '<span class="logo-name">Appoint</span>Master';
            logo.appendChild(h2);
        } else {
            logo.innerHTML = ''; // Clear previous content
            const img = document.createElement('img');
            img.src = "/static/appoint_app/images/appoint-master-logo.png"; // Adjust the URL accordingly
            logo.appendChild(img);

            const h2 = document.createElement('h2');
            h2.innerHTML = '<span class="logo-name">Appoint</span>Master';
            logo.appendChild(h2);
        }
    } else {
        // Default to light theme if no preference is saved
        document.body.classList.add('light-theme-variables');
        // Default logo for light theme
        logo.innerHTML = ''; // Clear previous content
        const img = document.createElement('img');
        img.src = "/static/appoint_app/images/appoint-master-logo.png"; // Adjust the URL accordingly
        logo.appendChild(img);

        const h2 = document.createElement('h2');
        h2.innerHTML = '<span class="logo-name">Appoint</span>Master';
        logo.appendChild(h2);
    }

    menuBtn.addEventListener('click', () => {
        sideMenu.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        sideMenu.style.display = 'none';
    });

    themeToggler.addEventListener('click', toggleTheme);
});
