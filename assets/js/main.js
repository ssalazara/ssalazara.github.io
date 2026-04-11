/**
 * Main JavaScript for github-page
 * Handles mobile menu, language preference, and accessibility enhancements
 */

(function() {
  'use strict';

  // ============================================================================
  // MOBILE MENU
  // ============================================================================

  function initMobileMenu() {
    var toggle = document.querySelector('.header__menu-toggle');
    var menu = document.getElementById('mobile-menu');
    var backdrop = document.querySelector('.header-backdrop');

    if (!toggle || !menu) return;

    function openMenu() {
      toggle.setAttribute('aria-expanded', 'true');
      menu.classList.add('is-open');
      if (backdrop) backdrop.classList.add('is-visible');
      document.body.style.overflow = 'hidden';
      trapFocus(menu);
    }

    function closeMenu() {
      toggle.setAttribute('aria-expanded', 'false');
      menu.classList.remove('is-open');
      if (backdrop) backdrop.classList.remove('is-visible');
      document.body.style.overflow = '';
      toggle.focus();
    }

    toggle.addEventListener('click', function() {
      var isOpen = toggle.getAttribute('aria-expanded') === 'true';
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    if (backdrop) {
      backdrop.addEventListener('click', closeMenu);
    }

    document.addEventListener('click', function(event) {
      if (menu.classList.contains('is-open') &&
          !toggle.contains(event.target) &&
          !menu.contains(event.target) &&
          (!backdrop || !backdrop.contains(event.target))) {
        closeMenu();
      }
    });

    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && menu.classList.contains('is-open')) {
        closeMenu();
      }
    });
  }

  // ============================================================================
  // FOCUS TRAP
  // ============================================================================

  function trapFocus(element) {
    var focusableElements = element.querySelectorAll(
      'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    var firstFocusable = focusableElements[0];
    var lastFocusable = focusableElements[focusableElements.length - 1];

    firstFocusable.focus();

    element.addEventListener('keydown', function(event) {
      if (event.key !== 'Tab') return;

      if (event.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus();
          event.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus();
          event.preventDefault();
        }
      }
    });
  }

  // ============================================================================
  // LANGUAGE PREFERENCE
  // ============================================================================

  function initLanguagePreference() {
    if (!window.localStorage) return;

    var currentLang = document.documentElement.lang || 'en';
    var storedLang = localStorage.getItem('preferredLanguage');

    if (!storedLang) {
      var browserLang = (navigator.language || '').split('-')[0];

      if (browserLang === 'es' && currentLang === 'en') {
        localStorage.setItem('preferredLanguage', 'es');
        var currentPath = window.location.pathname;
        var newPath = '/es' + (currentPath === '/' ? '/' : currentPath);
        window.location.href = newPath;
        return;
      }
    }

    localStorage.setItem('preferredLanguage', currentLang);
  }

  // ============================================================================
  // LAZY LOADING FALLBACK
  // ============================================================================

  function initLazyLoading() {
    if ('loading' in HTMLImageElement.prototype) return;

    var images = document.querySelectorAll('img[loading="lazy"]');

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            var img = entry.target;
            img.src = img.dataset.src || img.src;
            img.classList.add('loaded');
            observer.unobserve(img);
          }
        });
      });

      images.forEach(function(img) { observer.observe(img); });
    } else {
      images.forEach(function(img) {
        img.src = img.dataset.src || img.src;
      });
    }
  }

  // ============================================================================
  // SMOOTH SCROLL
  // ============================================================================

  function initSmoothScroll() {
    var anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        var targetId = link.getAttribute('href');
        if (targetId === '#') return;

        var targetElement = document.querySelector(targetId);
        if (targetElement) {
          event.preventDefault();
          targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          targetElement.setAttribute('tabindex', '-1');
          targetElement.focus({ preventScroll: true });
        }
      });
    });
  }

  // ============================================================================
  // INIT
  // ============================================================================

  function init() {
    initMobileMenu();
    initLanguagePreference();
    initLazyLoading();
    initSmoothScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
