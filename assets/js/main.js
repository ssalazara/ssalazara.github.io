/**
 * Main JavaScript for github-page
 * Handles mobile menu toggle, language preference, and accessibility
 */

(function() {
  'use strict';

  // ============================================================================
  // MOBILE MENU TOGGLE
  // ============================================================================

  function initMobileMenu() {
    const toggle = document.querySelector('.site-nav__toggle');
    const menu = document.querySelector('.site-nav__menu');

    if (!toggle || !menu) return;

    toggle.addEventListener('click', function() {
      const isOpen = toggle.getAttribute('aria-expanded') === 'true';
      
      // Toggle ARIA state
      toggle.setAttribute('aria-expanded', !isOpen);
      
      // Toggle menu visibility
      menu.classList.toggle('is-open');

      // Trap focus when menu is open
      if (!isOpen) {
        trapFocus(menu);
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      if (!toggle.contains(event.target) && !menu.contains(event.target)) {
        toggle.setAttribute('aria-expanded', 'false');
        menu.classList.remove('is-open');
      }
    });

    // Close menu on Escape key
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && menu.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        menu.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  // ============================================================================
  // FOCUS TRAP (for mobile menu accessibility)
  // ============================================================================

  function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
      'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length === 0) return;

    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', function(event) {
      if (event.key !== 'Tab') return;

      if (event.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus();
          event.preventDefault();
        }
      } else {
        // Tab
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus();
          event.preventDefault();
        }
      }
    });
  }

  // ============================================================================
  // LANGUAGE PREFERENCE (localStorage)
  // ============================================================================

  function initLanguagePreference() {
    const currentLang = document.documentElement.lang || 'en';
    
    // Store current language preference
    if (localStorage) {
      localStorage.setItem('preferredLanguage', currentLang);
    }

    // Detect browser language on first visit (if no stored preference)
    if (localStorage && !localStorage.getItem('preferredLanguage')) {
      const browserLang = navigator.language || navigator.userLanguage;
      const langCode = browserLang.split('-')[0]; // Get 'en' from 'en-US'
      
      // Redirect to appropriate language if different from current
      if (langCode === 'es' && currentLang === 'en') {
        const currentPath = window.location.pathname;
        const newPath = currentPath.replace('/en/', '/es/').replace(/^\/$/, '/es/');
        window.location.href = newPath;
      }
    }
  }

  // ============================================================================
  // LAZY LOADING IMAGES (enhanced)
  // ============================================================================

  function initLazyLoading() {
    // Modern browsers support native lazy loading
    // This is just a fallback for older browsers
    if ('loading' in HTMLImageElement.prototype) {
      return; // Native lazy loading is supported
    }

    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src || img.src;
            img.classList.add('loaded');
            imageObserver.unobserve(img);
          }
        });
      });

      images.forEach(function(img) {
        imageObserver.observe(img);
      });
    } else {
      // Fallback for browsers without IntersectionObserver
      images.forEach(function(img) {
        img.src = img.dataset.src || img.src;
      });
    }
  }

  // ============================================================================
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ============================================================================

  function initSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        const targetId = link.getAttribute('href');
        
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
          event.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
          
          // Update focus for accessibility
          targetElement.focus();
        }
      });
    });
  }

  // ============================================================================
  // INITIALIZE ON DOM READY
  // ============================================================================

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    initMobileMenu();
    initLanguagePreference();
    initLazyLoading();
    initSmoothScroll();
  }

})();
