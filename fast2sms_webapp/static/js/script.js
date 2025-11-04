// Fast2SMS Bulk Sender - Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });

    // Add close button to flash messages
    flashMessages.forEach(function(message) {
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = 'float: right; cursor: pointer; font-size: 1.5rem; line-height: 1; margin-left: 1rem;';
        closeBtn.onclick = function() {
            message.style.transition = 'opacity 0.3s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        };
        message.insertBefore(closeBtn, message.firstChild);
    });

    // Table search functionality
    const tables = document.querySelectorAll('.templates-table, .preview-table, .results-table');
    tables.forEach(function(table) {
        // Add search box above table
        const searchBox = document.createElement('input');
        searchBox.type = 'text';
        searchBox.placeholder = 'Search table...';
        searchBox.className = 'form-control';
        searchBox.style.marginBottom = '1rem';

        table.parentNode.insertBefore(searchBox, table);

        // Search functionality
        searchBox.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });

    // Smooth scroll to top button
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #4a90e2;
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        display: none;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        transition: all 0.3s;
    `;

    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });

    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    scrollBtn.addEventListener('mouseenter', function() {
        this.style.background = '#357abd';
        this.style.transform = 'scale(1.1)';
    });

    scrollBtn.addEventListener('mouseleave', function() {
        this.style.background = '#4a90e2';
        this.style.transform = 'scale(1)';
    });

    // Confirmation dialogs for destructive actions
    const resetLinks = document.querySelectorAll('a[href*="reset"]');
    resetLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to reset? This will clear your current session.')) {
                e.preventDefault();
            }
        });
    });

    // Copy to clipboard functionality for request IDs
    const requestIds = document.querySelectorAll('.request-id');
    requestIds.forEach(function(element) {
        if (element.textContent.trim()) {
            element.style.cursor = 'pointer';
            element.title = 'Click to copy';

            element.addEventListener('click', function() {
                const text = this.textContent;
                navigator.clipboard.writeText(text).then(function() {
                    const originalText = element.textContent;
                    element.textContent = 'Copied!';
                    element.style.color = '#50c878';

                    setTimeout(function() {
                        element.textContent = originalText;
                        element.style.color = '';
                    }, 2000);
                }).catch(function(err) {
                    console.error('Failed to copy:', err);
                });
            });
        }
    });

    // Progress animation for results page
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        const targetWidth = progressFill.style.width;
        progressFill.style.width = '0%';

        setTimeout(function() {
            progressFill.style.width = targetWidth;
        }, 300);
    }

    // Table row highlighting
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
            this.style.transition = 'all 0.2s';
        });

        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'none';
        });
    });

    // Card animations
    const cards = document.querySelectorAll('.card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.5s ease-out';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(function(card) {
        observer.observe(card);
    });

    // Add CSS animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);

    // Mobile menu toggle (if needed in future)
    const navLinks = document.querySelector('.nav-links');
    if (navLinks && window.innerWidth < 768) {
        const menuToggle = document.createElement('button');
        menuToggle.innerHTML = '☰';
        menuToggle.className = 'menu-toggle';
        menuToggle.style.cssText = `
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
        `;

        if (window.innerWidth < 768) {
            menuToggle.style.display = 'block';
            navLinks.style.display = 'none';
        }

        menuToggle.addEventListener('click', function() {
            if (navLinks.style.display === 'none') {
                navLinks.style.display = 'flex';
            } else {
                navLinks.style.display = 'none';
            }
        });
    }

    // Print functionality for results page
    if (document.querySelector('.results-table')) {
        const printBtn = document.createElement('button');
        printBtn.textContent = '🖨️ Print Results';
        printBtn.className = 'btn btn-secondary';
        printBtn.style.marginLeft = '1rem';

        printBtn.addEventListener('click', function() {
            window.print();
        });

        const downloadBtn = document.querySelector('a[href*="download_log"]');
        if (downloadBtn && downloadBtn.parentNode) {
            downloadBtn.parentNode.appendChild(printBtn);
        }
    }

    // Tooltip functionality
    const tooltips = document.querySelectorAll('[title]');
    tooltips.forEach(function(element) {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.textContent = this.getAttribute('title');
            tooltip.className = 'custom-tooltip';
            tooltip.style.cssText = `
                position: absolute;
                background: #2c3e50;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                font-size: 0.875rem;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
            `;

            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';

            this.setAttribute('data-original-title', this.getAttribute('title'));
            this.removeAttribute('title');
        });

        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.custom-tooltip');
            if (tooltip) {
                tooltip.remove();
            }
            if (this.getAttribute('data-original-title')) {
                this.setAttribute('title', this.getAttribute('data-original-title'));
                this.removeAttribute('data-original-title');
            }
        });
    });

    console.log('Fast2SMS Bulk Sender - Web App Loaded Successfully! 🚀');
});
