document.addEventListener('DOMContentLoaded', function() {
  // Handle submenu toggles
  const submenuToggles = document.querySelectorAll('[data-bs-toggle="collapse"]');
  
  submenuToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Get the target submenu
      const targetId = this.getAttribute('data-bs-target');
      const submenu = document.querySelector(targetId);
      
      // Toggle the collapsed class on the toggle button
      this.classList.toggle('collapsed');
      
      // Toggle the submenu visibility
      if (submenu) {
        submenu.classList.toggle('show');
      }
    });
  });

  // Handle submenu item clicks
  const submenuItems = document.querySelectorAll('.nav-content a');
  
  submenuItems.forEach(item => {
    item.addEventListener('click', function(e) {
      // Remove active class from all items
      submenuItems.forEach(i => i.classList.remove('active'));
      
      // Add active class to clicked item
      this.classList.add('active');
      
      // Add ripple effect
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      this.appendChild(ripple);
      
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      
      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${e.clientX - rect.left - size/2}px`;
      ripple.style.top = `${e.clientY - rect.top - size/2}px`;
      
      ripple.addEventListener('animationend', () => {
        ripple.remove();
      });
    });
  });
}); 