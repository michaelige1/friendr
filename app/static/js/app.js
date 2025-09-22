// Global JavaScript utilities for Friendr Pet Matcher
document.addEventListener('DOMContentLoaded', function() {
    console.log('Friendr app loaded successfully!');
    
    // Initialize global functionality
    initializeGlobalFeatures();
    initializeFormEnhancements();
    initializeAnimations();
});

// Global utility functions
function initializeGlobalFeatures() {
    // Add smooth scrolling for anchor links
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
    
    // Add keyboard navigation shortcuts
    document.addEventListener('keydown', function(e) {
        // Press 'Escape' to close modals or overlays
        if (e.key === 'Escape') {
            closeAllModals();
        }
        
        // Press 'Ctrl+Enter' to submit forms
        if (e.key === 'Enter' && e.ctrlKey) {
            const submitButton = document.querySelector('button[type="submit"]:not([disabled])');
            if (submitButton) {
                submitButton.click();
            }
        }
    });
    
    // Add loading state management
    window.showGlobalLoading = showGlobalLoading;
    window.hideGlobalLoading = hideGlobalLoading;
}

function initializeFormEnhancements() {
    // Add focus ring to form elements
    document.querySelectorAll('input, button, select, textarea').forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('focus-ring');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('focus-ring');
        });
    });
    
    // Add hover effects to interactive elements
    document.querySelectorAll('.choice-card, .pet-card, .btn-primary').forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.classList.add('hover-active');
        });
        
        element.addEventListener('mouseleave', function() {
            this.classList.remove('hover-active');
        });
    });
}

function initializeAnimations() {
    // Add fade-in animation to elements as they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate in
    document.querySelectorAll('.question-section, .choice-card, .pet-card').forEach(element => {
        observer.observe(element);
    });
}

// Quiz-specific functionality (moved to quiz.html template)

// Global utility functions
function showGlobalLoading(message = 'Loading...') {
    const loadingHtml = `
        <div id="globalLoadingOverlay" class="loading-overlay">
            <div class="loading-content">
                <div class="spinner"></div>
                <p class="mt-4 text-gray-700">\${message}</p>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loadingHtml);
}

function hideGlobalLoading() {
    const overlay = document.getElementById('globalLoadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

function closeAllModals() {
    // Close any open modals or overlays
    document.querySelectorAll('.modal, .overlay, .notification').forEach(element => {
        element.remove();
    });
}

// HTMX integration functions (for when backend is ready)
window.submitQuizToAPI = function(quizData) {
    console.log('Submitting to API:', quizData);
    
    // This will be called by HTMX
    return fetch('/friendr/quiz/quick-match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(quizData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);
        return data;
    })
    .catch(error => {
        console.error('API Error:', error);
        throw error;
    });
};

// Landing page specific functions
function initializeLandingPage() {
    // Add hover effects to pet selection buttons
    document.querySelectorAll('.pet-selection-button').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('scale-110');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('scale-110');
        });
    });
}

// Results page specific functions (for future use)
function initializeResultsPage() {
    // Add functionality for pet cards, filtering, etc.
    console.log('Results page initialized');
}

// Export functions for global use
window.Friendr = {
    quizData,
    showGlobalLoading,
    hideGlobalLoading,
    closeAllModals,
    submitQuizToAPI,
    initializeLandingPage,
    initializeResultsPage
};

// Debug helpers (remove in production)
window.debugQuiz = function() {
    console.log('Current quiz state:', window.quizInstance?.answers);
};

console.log('Friendr JavaScript loaded successfully! 🐾');