// Function to toggle between light and dark modes
function toggleDarkMode() {
  const currentTheme = localStorage.getItem('theme');
  
  // If the current theme is 'dark'
  if (currentTheme === 'dark') {
    // Switch to light theme
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
  } else {
    // Switch to dark theme
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  }
}

// Set the initial theme based on user's preference
function setInitialTheme() {
  // Check if user has a saved preference
  const savedTheme = localStorage.getItem('theme');
  
  if (savedTheme) {
    // Apply saved theme
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Update checkbox if it's dark mode
    if (savedTheme === 'dark') {
      const themeToggle = document.getElementById('theme-toggle');
      if (themeToggle) {
        themeToggle.checked = true;
      }
    }
  } else {
    // Check for system preference
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    if (prefersDarkScheme.matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      
      const themeToggle = document.getElementById('theme-toggle');
      if (themeToggle) {
        themeToggle.checked = true;
      }
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
    }
  }
}

// Run when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Set initial theme
  setInitialTheme();
  
  // Add event listener to toggle
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('change', toggleDarkMode);
  }
});