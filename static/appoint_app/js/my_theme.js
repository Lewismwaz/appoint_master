document.addEventListener("DOMContentLoaded", function() {
    const themeToggler = document.getElementById("theme-toggler");
    themeToggler.addEventListener("click", function() {
        const isDarkMode = document.body.classList.toggle("dark-theme");
        // Save the user's preference for dark mode
        localStorage.setItem("darkMode", isDarkMode);
        
        // Make an AJAX request to save the user's preference on the server
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        fetch("/toggle-dark-mode/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ darkMode: isDarkMode }),
        });
    });

    // Check if the user has previously set dark mode
    const darkMode = localStorage.getItem("darkMode") === "true";
    if (darkMode) {
        document.body.classList.add("dark-theme");
    }
});
