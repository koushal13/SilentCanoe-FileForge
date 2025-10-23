// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background change on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.project-card, .service-card, .about-text');
    
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Add some interactive effects
document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
    });
});

// GitHub stats (you can replace this with actual GitHub API calls)
function updateGitHubStats() {
    // This is a placeholder - you can integrate with GitHub API
    const stats = {
        repos: '1+',
        commits: '50+',
        stars: 'Growing'
    };
    
    // Update stats in the hero section if needed
    console.log('GitHub stats loaded:', stats);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateGitHubStats();
    
    // Add loading animation completion
    document.body.classList.add('loaded');
});

// Contact form handling (if you add a contact form later)
function handleContactForm(event) {
    event.preventDefault();
    // Add your contact form handling logic here
    console.log('Contact form submitted');
}

// Typing effect for hero title (optional enhancement)
function typeEffect() {
    const title = document.querySelector('.hero-title');
    const text = title.innerHTML;
    title.innerHTML = '';
    
    let i = 0;
    const timer = setInterval(() => {
        if (i < text.length) {
            title.innerHTML += text.charAt(i);
            i++;
        } else {
            clearInterval(timer);
        }
    }, 50);
}

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Add click tracking for project links
document.querySelectorAll('.project-link').forEach(link => {
    link.addEventListener('click', (e) => {
        const projectName = e.target.closest('.project-card').querySelector('h3').textContent;
        console.log(`Project link clicked: ${projectName}`);
        // You can add analytics tracking here
    });
});

// Progressive enhancement for better UX
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // You can add a service worker here for offline functionality
        console.log('Service Worker support detected');
    });
}

// Dark mode toggle (future enhancement)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load dark mode preference
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
});

// Smooth reveal animations
const revealElements = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
        }
    });
}, { threshold: 0.15 });

revealElements.forEach(el => revealObserver.observe(el));