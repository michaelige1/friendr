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

// Quiz-specific functionality
function quizData() {
    return {
        answers: {
            dogsImportance: 2,
            dogIntroduction: null,
            catsImportance: 2,
            catBehavior: null,
            kidsImportance: 2,
            kidsBehavior: null,
            strangersImportance: 2,
            strangersBehavior: null
        },
        
        isFormValid() {
            const requiredAnswers = [
                'dogIntroduction',
                'catBehavior', 
                'kidsBehavior',
                'strangersBehavior'
            ];
            
            return requiredAnswers.every(key => this.answers[key] !== null);
        },
        
        getProgress() {
            const total = 8;
            const completed = Object.values(this.answers).filter(val => val !== null).length;
            return `\${completed}/\${total}`;
        },
        
        getProgressPercentage() {
            const total = 8;
            const completed = Object.values(this.answers).filter(val => val !== null).length;
            return Math.round((completed / total) * 100);
        },
        
        submitQuiz() {
            if (!this.isFormValid()) {
                this.showValidationError();
                return;
            }
            
            console.log('Quiz answers:', this.answers);
            
            // Convert answers to API format
            const quizData = this.formatQuizData();
            
            // Show loading state
            this.showLoading();
            
            // Simulate API call (replace with real HTMX call later)
            this.simulateAPICall(quizData);
        },
        
        formatQuizData() {
            return {
                dogs: this.answers.dogIntroduction,
                cats: this.answers.catBehavior,
                kids: this.answers.kidsBehavior,
                energy: 3, // Default values for now
                affection: 3,
                training: 3,
                // Include importance ratings
                meta: {
                    dogsImportance: this.answers.dogsImportance,
                    catsImportance: this.answers.catsImportance,
                    kidsImportance: this.answers.kidsImportance,
                    strangersImportance: this.answers.strangersImportance
                }
            };
        },
        
        simulateAPICall(data) {
            // Simulate network delay
            setTimeout(() => {
                this.hideLoading();
                
                // For now, show success message
                this.showSuccessMessage(data);
                
                // In real implementation, redirect to results page
                // window.location.href = '/friendr/results?data=' + encodeURIComponent(JSON.stringify(data));
            }, 2000);
        },
        
        showValidationError() {
            const firstUnanswered = this.getFirstUnansweredQuestion();
            
            // Show error message
            this.showNotification('Please answer all questions before submitting!', 'error');
            
            // Scroll to first unanswered question
            if (firstUnanswered) {
                this.scrollToQuestion(firstUnanswered);
            }
        },
        
        getFirstUnansweredQuestion() {
            const requiredAnswers = [
                'dogIntroduction',
                'catBehavior', 
                'kidsBehavior',
                'strangersBehavior'
            ];
            
            return requiredAnswers.find(key => this.answers[key] === null);
        },
        
        scrollToQuestion(questionKey) {
            const element = document.querySelector(`[x-model="answers.\${questionKey}"]`);
            if (element) {
                const questionSection = element.closest('.question-section');
                if (questionSection) {
                    questionSection.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                    
                    // Add highlight effect
                    questionSection.classList.add('highlight-question');
                    setTimeout(() => {
                        questionSection.classList.remove('highlight-question');
                    }, 2000);
                }
            }
        },
        
        showLoading() {
            const loadingHtml = `
                <div id="quizLoadingOverlay" class="loading-overlay">
                    <div class="loading-content">
                        <div class="spinner"></div>
                        <h3 class="text-xl font-semibold text-gray-800 mt-4">Finding Your Perfect Matches</h3>
                        <p class="text-gray-600 mt-2">Analyzing your preferences...</p>
                        <div class="progress-bar mt-4 w-64">
                            <div class="progress-fill" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', loadingHtml);
            
            // Animate progress bar
            this.animateProgressBar();
        },
        
        animateProgressBar() {
            const progressFill = document.querySelector('#quizLoadingOverlay .progress-fill');
            if (progressFill) {
                let width = 0;
                const interval = setInterval(() => {
                    width += Math.random() * 15;
                    if (width >= 100) {
                        width = 100;
                        clearInterval(interval);
                    }
                    progressFill.style.width = width + '%';
                }, 200);
            }
        },
        
        hideLoading() {
            const overlay = document.getElementById('quizLoadingOverlay');
            if (overlay) {
                overlay.classList.add('fade-out');
                setTimeout(() => overlay.remove(), 300);
            }
        },
        
        showSuccessMessage(data) {
            const message = `
                <div class="success-message">
                    <h3>Quiz Completed Successfully! 🎉</h3>
                    <p>We found some great matches for you based on your preferences.</p>
                    <div class="quiz-summary">
                        <h4>Your Preferences:</h4>
                        <ul>
                            <li>Dogs: Level \${data.dogs}</li>
                            <li>Cats: Level \${data.cats}</li>
                            <li>Kids: Level \${data.kids}</li>
                        </ul>
                    </div>
                </div>
            `;
            
            this.showNotification(message, 'success', 5000);
        },
        
        showNotification(message, type = 'info', duration = 3000) {
            const notification = document.createElement('div');
            notification.className = `notification notification-\${type}`;
            notification.innerHTML = `
                <div class="notification-content">
                    \${message}
                    <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            // Auto-remove after duration
            if (duration > 0) {
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, duration);
            }
        },
        
        resetQuiz() {
            if (confirm('Are you sure you want to reset the quiz? All your answers will be lost.')) {
                this.answers = {
                    dogsImportance: 2,
                    dogIntroduction: null,
                    catsImportance: 2,
                    catBehavior: null,
                    kidsImportance: 2,
                    kidsBehavior: null,
                    strangersImportance: 2,
                    strangersBehavior: null
                };
                
                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
                
                this.showNotification('Quiz has been reset!', 'info');
            }
        },
        
        // Helper method to check if a specific question is answered
        isQuestionAnswered(questionKey) {
            return this.answers[questionKey] !== null;
        },
        
        // Method to get completion status for progress indicators
        getQuestionCompletionStatus() {
            return {
                dogs: this.isQuestionAnswered('dogIntroduction'),
                cats: this.isQuestionAnswered('catBehavior'),
                kids: this.isQuestionAnswered('kidsBehavior'),
                strangers: this.isQuestionAnswered('strangersBehavior')
            };
        }
    }
}

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