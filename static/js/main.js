// Form validation
(function () {
    'use strict'
    
    // Fetch all forms that need validation
    var forms = document.querySelectorAll('.needs-validation')
    
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                
                form.classList.add('was-validated')
            }, false)
        })
})()

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault()
        
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        })
    })
})

// Navbar scroll behavior
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar')
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled')
    } else {
        navbar.classList.remove('navbar-scrolled')
    }
})

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

// Initialize popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})

// Flash messages auto-hide
window.setTimeout(function() {
    document.querySelectorAll('.alert').forEach(function(alert) {
        if (!alert.classList.contains('alert-permanent')) {
            var bsAlert = new bootstrap.Alert(alert)
            bsAlert.close()
        }
    })
}, 5000)

// Form input masks
document.addEventListener('DOMContentLoaded', function() {
    var phoneInputs = document.querySelectorAll('input[type="tel"]')
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/)
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '')
        })
    })
})

// Animate on scroll
window.addEventListener('scroll', function() {
    document.querySelectorAll('.animate-fade-in').forEach(function(element) {
        if (isElementInViewport(element)) {
            element.style.opacity = '1'
            element.style.transform = 'translateY(0)'
        }
    })
})

function isElementInViewport(el) {
    var rect = el.getBoundingClientRect()
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    )
}

// Country statistics counter animation
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.stat-number')
    const speed = 200
    
    counters.forEach(counter => {
        const animate = () => {
            const value = +counter.getAttribute('data-target')
            const data = +counter.innerText
            
            const time = value / speed
            if (data < value) {
                counter.innerText = Math.ceil(data + time)
                setTimeout(animate, 1)
            } else {
                counter.innerText = value
            }
        }
        
        animate()
    })
})

// Career robot interaction
document.addEventListener('DOMContentLoaded', function() {
    const robot = document.querySelector('.career-robot')
    if (robot) {
        robot.addEventListener('mouseover', function() {
            this.classList.add('robot-hover')
        })
        
        robot.addEventListener('mouseout', function() {
            this.classList.remove('robot-hover')
        })
    }
}) 