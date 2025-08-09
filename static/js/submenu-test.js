// Modern Submenu JavaScript
document.addEventListener('DOMContentLoaded', function() {
  console.log('Modern submenu script loaded');
  
  // Get all submenu elements
  const submenus = document.querySelectorAll('.submenu');
  const submenuToggles = document.querySelectorAll('.submenu-toggle');
  const submenuLinks = document.querySelectorAll('.submenu-link');
  
  console.log('Found submenus:', submenus.length);
  console.log('Found toggles:', submenuToggles.length);
  console.log('Found links:', submenuLinks.length);
  
  // Handle submenu toggle clicks
  submenuToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      console.log('Submenu toggle clicked');
      
      // Get the target submenu
      const targetId = this.getAttribute('data-bs-target');
      const submenu = document.querySelector(targetId);
      
      if (submenu) {
        // Toggle the collapsed class on the toggle button
        this.classList.toggle('collapsed');
        
        // Add smooth animation class
        submenu.classList.add('transitioning');
        
        // Remove animation class after transition
        setTimeout(() => {
          submenu.classList.remove('transitioning');
        }, 300);
      }
    });
  });
  
  // Handle submenu link clicks
  submenuLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      console.log('Submenu link clicked:', this.textContent.trim());
      
      // Remove active class from all submenu links
      submenuLinks.forEach(l => l.classList.remove('active'));
      
      // Add active class to clicked link
      this.classList.add('active');
      
      // Add ripple effect
      const ripple = document.createElement('span');
      ripple.classList.add('ripple-effect');
      ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
      `;
      
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      
      this.appendChild(ripple);
      
      // Remove ripple after animation
      setTimeout(() => {
        if (ripple.parentNode) {
          ripple.parentNode.removeChild(ripple);
        }
      }, 600);
    });
  });
  
  // Set initial active states based on current URL
  const currentPath = window.location.pathname;
  submenuLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href)) {
      link.classList.add('active');
      
      // Expand parent submenu
      const submenu = link.closest('.submenu');
      if (submenu) {
        submenu.classList.add('show');
        const toggle = document.querySelector(`[data-bs-target="#${submenu.id}"]`);
        if (toggle) {
          toggle.classList.remove('collapsed');
          toggle.setAttribute('aria-expanded', 'true');
        }
      }
    }
  });
  
  // Add CSS animation for ripple effect
  if (!document.querySelector('#ripple-styles')) {
    const style = document.createElement('style');
    style.id = 'ripple-styles';
    style.textContent = `
      @keyframes ripple {
        to {
          transform: scale(4);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);
  }
}); 