document.addEventListener("DOMContentLoaded", function() {
    const elements = document.querySelectorAll('.format-number');
    
    elements.forEach(function(element) {
        const textContent = element.textContent.trim();
        const number = parseFloat(textContent.replace(/[^\d.-]/g, ''));

        if (!isNaN(number)) {
        element.textContent = number.toLocaleString('en-GB', { 
            style: 'currency', 
            currency: 'GBP', 
            minimumFractionDigits: 2, 
            maximumFractionDigits: 2 
        });
        }
    });
});