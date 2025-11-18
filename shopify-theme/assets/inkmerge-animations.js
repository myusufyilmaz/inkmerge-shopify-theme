/**
 * InkMerge Smooth Animations & Interactions
 * Scroll animations, hover effects, and micro-interactions
 */

(function() {
  'use strict';
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  function init() {
    initScrollAnimations();
    initStickyHeader();
    initSmoothScroll();
    initButtonRippleEffect();
    initParallaxEffect();
    initCardAnimations();
  }
  
  /**
   * Scroll Animations - Fade in elements as they come into view
   */
  function initScrollAnimations() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          // Unobserve after animation to improve performance
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
    
    // Observe all elements with animation classes
    const animatedElements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
    animatedElements.forEach(el => observer.observe(el));
    
    // Auto-add fade-in class to sections
    const sections = document.querySelectorAll('section:not(.hero-section)');
    sections.forEach((section, index) => {
      if (!section.classList.contains('fade-in')) {
        section.classList.add('fade-in');
        section.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(section);
      }
    });
  }
  
  /**
   * Sticky Header - Add shadow on scroll
   */
  function initStickyHeader() {
    const header = document.querySelector('.page__header, header');
    if (!header) return;
    
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
      const currentScroll = window.pageYOffset;
      
      if (currentScroll > 100) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
      
      // Hide header on scroll down, show on scroll up
      if (currentScroll > lastScroll && currentScroll > 500) {
        header.style.transform = 'translateY(-100%)';
      } else {
        header.style.transform = 'translateY(0)';
      }
      
      lastScroll = currentScroll;
    }, { passive: true });
  }
  
  /**
   * Smooth Scroll for Anchor Links
   */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }
  
  /**
   * Button Ripple Effect
   */
  function initButtonRippleEffect() {
    const buttons = document.querySelectorAll('.button, .btn, button');
    
    buttons.forEach(button => {
      button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
      });
    });
    
    // Add ripple CSS
    const style = document.createElement('style');
    style.textContent = `
      .button, .btn, button {
        position: relative;
        overflow: hidden;
      }
      .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
      }
      @keyframes ripple-animation {
        to {
          transform: scale(4);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);
  }
  
  /**
   * Parallax Effect for Hero Section
   */
  function initParallaxEffect() {
    const hero = document.querySelector('.hero-section, .section__slider');
    if (!hero) return;
    
    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;
      const rate = scrolled * 0.5;
      
      if (hero) {
        hero.style.transform = `translate3d(0, ${rate}px, 0)`;
      }
    }, { passive: true });
  }
  
  /**
   * Product Card Animations
   */
  function initCardAnimations() {
    const cards = document.querySelectorAll('.product-card, .card, .collection__item');
    
    cards.forEach((card, index) => {
      // Stagger animation on load
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';
      
      setTimeout(() => {
        card.style.transition = 'all 0.6s ease';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, index * 100);
      
      // Add tilt effect on mouse move
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
      });
    });
  }
  
  /**
   * Add to Cart Animation
   */
  function initAddToCartAnimation() {
    const addToCartButtons = document.querySelectorAll('.product__form--atc, [name="add"]');
    
    addToCartButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        // Add success animation
        const original = this.innerHTML;
        this.innerHTML = '✓ Added!';
        this.style.background = 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)';
        
        setTimeout(() => {
          this.innerHTML = original;
          this.style.background = '';
        }, 2000);
      });
    });
  }
  
  /**
   * Number Counter Animation
   */
  function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target.toLocaleString();
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current).toLocaleString();
      }
    }, 16);
  }
  
  /**
   * Initialize counter animations when visible
   */
  function initCounterAnimations() {
    const counters = document.querySelectorAll('[data-counter]');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = parseInt(entry.target.dataset.counter);
          animateCounter(entry.target, target);
          observer.unobserve(entry.target);
        }
      });
    });
    
    counters.forEach(counter => observer.observe(counter));
  }
  
  /**
   * Mobile Menu Smooth Toggle
   */
  function initMobileMenu() {
    const menuToggle = document.querySelector('.mobile-menu-toggle, .hamburger');
    const mobileMenu = document.querySelector('.mobile-menu, .sidebar');
    
    if (!menuToggle || !mobileMenu) return;
    
    menuToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
    });
  }
  
  /**
   * Add to Cart Animation
   */
  function initAddToCartAnimation() {
    const addToCartButtons = document.querySelectorAll('.product__form--atc, [name="add"], button[type="submit"][form*="product"]');
    
    addToCartButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        const form = this.closest('form');
        if (!form || !form.action.includes('/cart/add')) return;
        
        // Add success animation
        const original = this.innerHTML;
        const originalBg = this.style.background;
        
        // Wait for add to cart to complete
        setTimeout(() => {
          this.innerHTML = '✓ Added to Cart!';
          this.style.background = 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)';
          this.style.pointerEvents = 'none';
          
          setTimeout(() => {
            this.innerHTML = original;
            this.style.background = originalBg;
            this.style.pointerEvents = '';
          }, 2000);
        }, 300);
      });
    });
  }
  
  // Initialize additional features
  initAddToCartAnimation();
  initCounterAnimations();
  initMobileMenu();
})();
