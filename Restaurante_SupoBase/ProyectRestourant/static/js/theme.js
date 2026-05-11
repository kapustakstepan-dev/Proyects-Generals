// Manejo del tema (claro/oscuro)

document.addEventListener("DOMContentLoaded", function() {
    // Al cargar, aplicamos el tema guardado
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
});

// Función para alternar el tema
const toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
};

// Actualiza el icono del botón
const updateThemeIcon = (theme) => {
    const icon = document.getElementById('theme-icon');
    if (icon) icon.innerText = theme === 'dark' ? '☀️' : '🌙';
};

// Aplicación inmediata para evitar parpadeos
(function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
})();
