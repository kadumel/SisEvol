(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
      
      // Responsive sidebar behavior
      const sidebar = select('#sidebar')
      const mainWrapper = select('.main-wrapper')
      
      if (window.innerWidth <= 992) {
        // Mobile behavior
        sidebar.classList.toggle('show')
        if (sidebar.classList.contains('show')) {
          // Add overlay
          const overlay = document.createElement('div')
          overlay.className = 'sidebar-overlay'
          overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1010;
            cursor: pointer;
          `
          document.body.appendChild(overlay)
          
          // Close sidebar when clicking overlay
          overlay.addEventListener('click', function() {
            sidebar.classList.remove('show')
            document.body.removeChild(overlay)
          })
        } else {
          // Remove overlay
          const overlay = select('.sidebar-overlay')
          if (overlay) {
            document.body.removeChild(overlay)
          }
        }
      } else {
        // Desktop behavior
        if (select('body').classList.contains('toggle-sidebar')) {
          mainWrapper.style.marginLeft = '70px'
          sidebar.style.width = '70px'
        } else {
          mainWrapper.style.marginLeft = '280px'
          sidebar.style.width = '280px'
        }
      }
    })
  }

  /**
   * Responsive sidebar behavior
   */
  function handleResize() {
    const sidebar = select('#sidebar')
    const mainWrapper = select('.main-wrapper')
    const overlay = select('.sidebar-overlay')
    
    if (window.innerWidth > 992) {
      // Desktop: remove mobile classes and overlay
      sidebar.classList.remove('show')
      if (overlay) {
        document.body.removeChild(overlay)
      }
      
      // Reset sidebar width based on toggle state
      if (select('body').classList.contains('toggle-sidebar')) {
        mainWrapper.style.marginLeft = '70px'
        sidebar.style.width = '70px'
      } else {
        mainWrapper.style.marginLeft = '280px'
        sidebar.style.width = '280px'
      }
    } else {
      // Mobile: ensure sidebar is hidden by default
      sidebar.classList.remove('show')
      mainWrapper.style.marginLeft = '0'
      sidebar.style.width = '100%'
      sidebar.style.maxWidth = '300px'
      
      if (overlay) {
        document.body.removeChild(overlay)
      }
    }
  }

  // Handle window resize
  window.addEventListener('resize', handleResize)
  
  // Initialize responsive behavior on load
  window.addEventListener('load', handleResize)

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */

  const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;
  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, ["All", -1]],
      columns: [{
          select: 2,
          sortSequence: ["desc", "asc"]
        },
        {
          select: 3,
          sortSequence: ["desc"]
        },
        {
          select: 4,
          cellClass: "green",
          headerClass: "red"
        }
      ]
    });
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar
    const toggleSidebarBtn = document.querySelector('.toggle-sidebar-btn');
    if (toggleSidebarBtn) {
      toggleSidebarBtn.addEventListener('click', function() {
        document.body.classList.toggle('toggle-sidebar');
      });
    }

    // Handle submenu active states
    const currentLocation = location.pathname;
    const menuItems = document.querySelectorAll('.nav-content a');
    const parentLinks = document.querySelectorAll('.nav-link[data-bs-toggle="collapse"]');

    // Add click handlers to submenu items
    menuItems.forEach(item => {
      item.addEventListener('click', function(e) {
        // Remove active class from all items
        menuItems.forEach(menuItem => menuItem.classList.remove('active'));
        // Add active class to clicked item
        this.classList.add('active');
      });
    });

    // Set initial active states
    menuItems.forEach(item => {
      const href = item.getAttribute('href');
      if (href && currentLocation.includes(href)) {
        item.classList.add('active');
        
        // Expand parent menu
        const collapse = item.closest('.nav-content');
        if (collapse) {
          collapse.classList.add('show');
          const trigger = document.querySelector(`[data-bs-target="#${collapse.id}"]`);
          if (trigger) {
            trigger.classList.remove('collapsed');
            trigger.setAttribute('aria-expanded', 'true');
          }
        }
      }
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize DataTables with modern styling
    if ($.fn.DataTable) {
      $('.datatable').DataTable({
        responsive: true,
        language: {
          search: "",
          searchPlaceholder: "Pesquisar...",
          lengthMenu: "Mostrar _MENU_ registros por página",
          info: "Mostrando _START_ até _END_ de _TOTAL_ registros",
          infoEmpty: "Mostrando 0 até 0 de 0 registros",
          infoFiltered: "(Filtrados de _MAX_ registros)",
          paginate: {
            first: "Primeiro",
            previous: "Anterior",
            next: "Próximo",
            last: "Último"
          }
        },
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rt<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
        pageLength: 10,
        order: [[0, 'desc']],
        drawCallback: function() {
          $('.dataTables_paginate > .pagination').addClass('pagination-sm');
        }
      });
    }

    // Back to top button
    const backToTop = document.querySelector('.back-to-top');
    if (backToTop) {
      window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
          backToTop.classList.add('active');
        } else {
          backToTop.classList.remove('active');
        }
      });

      backToTop.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }

    // Header scroll state
    const header = document.querySelector('.header');
    if (header) {
      window.addEventListener('scroll', function() {
        if (window.scrollY > 30) {
          header.classList.add('header-scrolled');
        } else {
          header.classList.remove('header-scrolled');
        }
      });
    }

    // Handle mobile navigation
    if (window.innerWidth <= 768) {
      document.body.classList.add('toggle-sidebar');
    }

    window.addEventListener('resize', function() {
      if (window.innerWidth <= 768) {
        document.body.classList.add('toggle-sidebar');
      }
    });
  });

})();