document.getElementById('inventory-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from traditional submission

    // Collect form data
    const form = document.getElementById('inventory-form');
    const formData = new FormData(form);

    // Get the CSRF token from the form
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        // Send form data using fetch
        const response = await fetch('/inventory/new-item/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken, 
            },
        });

        const data = await response.json();

        // Handle server response
        if (response.ok) {
            alert('Inventory updated successfully!');
            form.reset(); // Clear the form
        } else {
            alert('Error: ' + (data.error || 'Unable to update inventory.'));
        }
    } catch (error) {
        alert('Request failed: ' + error.message);
    }
});
