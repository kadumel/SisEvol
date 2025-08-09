"// Modern Sidebar JavaScript" 

document.addEventListener('DOMContentLoaded', function() {
  console.log('Modern sidebar script loaded');
  
  // Initialize sidebar functionality
  initSidebar();
  
  // Initialize submenu functionality
  initSubmenus();
  
  // Initialize responsive behavior
  initResponsive();
});

function initSidebar() {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.querySelector('.toggle-sidebar-btn');
  const mainWrapper = document.querySelector('.main-wrapper');
  
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Toggle sidebar visibility
      sidebar.classList.toggle('show');
      
      // Add overlay for mobile
      if (window.innerWidth <= 992) {
        toggleOverlay();
      }
    });
  }
  
  // Close sidebar when clicking overlay
  document.addEventListener('click', function(e) {
    if (window.innerWidth <= 992 && 
        !sidebar.contains(e.target) && 
        !toggleBtn.contains(e.target) && 
        sidebar.classList.contains('show')) {
      sidebar.classList.remove('show');
      removeOverlay();
    }
  });
}

function initSubmenus() {
  const submenuToggles = document.querySelectorAll('.submenu-toggle');
  const submenuLinks = document.querySelectorAll('.submenu-link');
  
  // Handle submenu toggle clicks
  submenuToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('data-bs-target');
      const submenu = document.querySelector(targetId);
      
      if (submenu) {
        // Close other submenus if needed
        const otherSubmenus = document.querySelectorAll('.submenu.show');
        otherSubmenus.forEach(menu => {
          if (menu !== submenu) {
            menu.classList.remove('show');
            const otherToggle = document.querySelector(`[data-bs-target="#${menu.id}"]`);
            if (otherToggle) {
              otherToggle.setAttribute('aria-expanded', 'false');
            }
          }
        });
        
        // Toggle current submenu
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !isExpanded);
        
        if (isExpanded) {
          submenu.classList.remove('show');
        } else {
          submenu.classList.add('show');
        }
      }
    });
  });
  
  // Handle submenu link clicks
  submenuLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Remove active class from all submenu links
      submenuLinks.forEach(l => l.classList.remove('active'));
      
      // Add active class to clicked link
      this.classList.add('active');
      
      // Add ripple effect
      addRippleEffect(this, e);
      
      // Close sidebar on mobile after clicking
      if (window.innerWidth <= 992) {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
          setTimeout(() => {
            sidebar.classList.remove('show');
            removeOverlay();
          }, 300);
        }
      }
    });
  });
  
  // Set initial active states
  setInitialActiveStates();
}

function initResponsive() {
  function handleResize() {
    const sidebar = document.getElementById('sidebar');
    const mainWrapper = document.querySelector('.main-wrapper');
    
    if (window.innerWidth > 992) {
      // Desktop: show sidebar by default
      sidebar.classList.remove('show');
      removeOverlay();
      
      if (mainWrapper) {
        mainWrapper.style.marginLeft = '280px';
      }
    } else {
      // Mobile: hide sidebar by default
      sidebar.classList.remove('show');
      removeOverlay();
      
      if (mainWrapper) {
        mainWrapper.style.marginLeft = '0';
      }
    }
  }
  
  // Handle window resize
  window.addEventListener('resize', handleResize);
  
  // Initialize on load
  handleResize();
}

function setInitialActiveStates() {
  const currentPath = window.location.pathname;
  const submenuLinks = document.querySelectorAll('.submenu-link');
  const navLinks = document.querySelectorAll('.nav-link');
  
  // Set active state for submenu links
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
          toggle.setAttribute('aria-expanded', 'true');
        }
      }
    }
  });
  
  // Set active state for main nav links
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href) && !link.classList.contains('submenu-toggle')) {
      link.classList.add('active');
    }
  });
}

function addRippleEffect(element, event) {
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
  
  const rect = element.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  const x = event.clientX - rect.left - size / 2;
  const y = event.clientY - rect.top - size / 2;
  
  ripple.style.width = ripple.style.height = size + 'px';
  ripple.style.left = x + 'px';
  ripple.style.top = y + 'px';
  
  element.appendChild(ripple);
  
  // Remove ripple after animation
  setTimeout(() => {
    if (ripple.parentNode) {
      ripple.parentNode.removeChild(ripple);
    }
  }, 600);
}

function toggleOverlay() {
  if (!document.querySelector('.sidebar-overlay')) {
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      z-index: 999;
      cursor: pointer;
      transition: opacity 0.3s ease;
    `;
    
    overlay.addEventListener('click', function() {
      const sidebar = document.getElementById('sidebar');
      if (sidebar) {
        sidebar.classList.remove('show');
      }
      removeOverlay();
    });
    
    document.body.appendChild(overlay);
    
    // Add animation
    setTimeout(() => {
      overlay.style.opacity = '1';
    }, 10);
  }
}

function removeOverlay() {
  const overlay = document.querySelector('.sidebar-overlay');
  if (overlay) {
    overlay.style.opacity = '0';
    setTimeout(() => {
      if (overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
      }
    }, 300);
  }
}

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
