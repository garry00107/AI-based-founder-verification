// static/js/script.js

// This file is currently mostly for structure.
// The map initialization is handled directly in results.html
// because it needs data passed from Flask (the 'locations' variable).

document.addEventListener('DOMContentLoaded', function() {
    console.log("Founder Verifier JS Loaded");

    // Potential future enhancements could go here:
    // - Client-side validation for the search form
    // - Dynamic loading indicators during search
    // - More interactive UI elements (e.g., clickable sticky notes to show more detail)

    // Example: Add a subtle animation to cards on load
    const cards = document.querySelectorAll('.results-card');
    cards.forEach((card, index) => {
        card.style.opacity = 0;
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, index * 100); // Stagger the animation
    });

});