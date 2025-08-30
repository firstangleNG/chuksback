// const addItemButton = document.getElementById('add-item');
const itemsTable = document.querySelector('#invoice-items tbody');

// Auto-calculate totals
function calculateTotals() {
    let subtotal = 0;
    let totalTax = 0;

    document.querySelectorAll('#invoice-items tbody tr').forEach(row => {
        const quantity = parseFloat(row.querySelector('.quantity').value) || 0;
        const price = parseFloat(row.querySelector('.price').value) || 0;
        const tax = parseFloat(row.querySelector('.tax').value) || 0;

        const itemTotal = (quantity * price) + (quantity * price * tax / 100);
        row.querySelector('.total').textContent = (itemTotal).toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});

        subtotal += quantity * price;
        totalTax += (quantity * price * tax / 100);
    });

    document.getElementById('subtotal').textContent = subtotal.toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});
    document.getElementById('total-tax').textContent = totalTax.toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});
    document.getElementById('final-amount').textContent = (subtotal + totalTax).toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});
}


// Remove item row
itemsTable.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-item')) {
        e.target.closest('tr').remove();
        calculateTotals();
    }
});

// Recalculate on input change
itemsTable.addEventListener('input', calculateTotals);

calculateTotals();



// Helper function to calculate totals
const calculateTotal = (quantity, price, tax) => {
    const subtotal = quantity * price;
    const taxes = (tax / 100) * subtotal;
    return { subtotal, taxes, total: subtotal + taxes };
};




const form = document.getElementById('invoice-form');
form.addEventListener('submit', async function(event) {

    event.preventDefault(); // Prevent the default form submission

    // const ticket_id = document.getElementById('ticket_id').value; 
    const ticket_id = localStorage.getItem('current_ticket') // Get the ticket ID from localStorage
    const invoice = document.getElementById("invoice").value.trim();
    const payment_method = document.getElementById("payment-method").value.trim();
    const service_name = form.querySelector("input[name='service_name']").value;
    const description = form.querySelector("input[name='description']").value;
    const quantity = parseInt(form.querySelector("input[name='quantity']").value, 10);
    const price_per_unit = parseFloat(form.querySelector("input[name='price_per_unit']").value);
    const taxes = parseFloat(form.querySelector("input[name='tax']").value);

    const invoiceItemData = {
        ticket_id: ticket_id,
        invoice:invoice,
        payment_method:payment_method,
        service_name: service_name,
        description: description,
        quantity: quantity,
        price_per_unit: price_per_unit,
        taxes: taxes
    };

    try {
        const response = await fetch('/invoicing/repair-ticket/invoice/', {
            method: 'POST', // POST request to save the item
            headers: {
                'Content-Type': 'application/json', // Set the content type to JSON
            },
            body: JSON.stringify(invoiceItemData) // Use the correct object here
        });

        if (!response.ok) {
            // Handle server errors or invalid responses
            throw new Error('Error saving the invoice item');
        }

        // Parse the response as JSON if successful
        const data = await response.json();
        console.log('Invoice item saved:', data);
        form.reset()
        window.location.reload()
        // Optionally, you can display a success message or update the UI
    } catch (error) {
        console.error('Failed to save invoice item:', error);
        // Handle the error (e.g., show a message to the user)
    }
});




document.addEventListener("DOMContentLoaded", function() {
    const ticketId = localStorage.getItem('current_ticket'); 
    const invoice = document.getElementById("invoice").value.trim();
    const invoiceItemsContainer = document.querySelector("#invoice-items tbody");

    // Fetch invoice items using the ticket ID
    fetch(`/invoicing/ticket-invoices/${invoice}/`)
        .then(response => response.json())
        .then(responseData => {
            // Populate the form with the fetched data
            responseData.data.forEach((item,index) => {
                const row = document.createElement("tr");
                row.className = 'invoice-tr'
                row.dataset.id = item.id; // item.id corresponds to the primary key (itemId)
                row.innerHTML = `
               
                    <td><input type="text" name="service_name" value="${item.service_name}" required></td>
                    <td><input type="text" name="description" value="${item.description}"></td>
                    <td><input type="number" name="quantity" class="quantity" min="1" value="${item.quantity}" required></td>
                    <td><input type="number" name="price_per_unit" class="price" step="0.01" value="${item.price_per_unit}" required></td>
                    <td><input type="number" name="tax" class="tax" step="0.01" value="${item.taxes}"></td>
                    <td class="total">${item.total}</td>
                  
                    <td><button type="button" class="remove-item" id="${item.id}">Remove</button></td>
            
                `;

                // <td><button type="button" class="update-item" id="${item.id}">Update</button></td> 
                invoiceItemsContainer.appendChild(row);
            });
            updatePageMonetry(responseData.subtotal,responseData.final_tax,responseData.total_amount);
            // Add event listeners for Remove and Update buttons
            document.querySelectorAll('.remove-item').forEach(button => {
                button.addEventListener('click', async (e) => {
                    try {
                            const itemId = e.target.id
                        // Get the item ID from a data attribute (e.g., data-item-id)
                        // const itemId = button.dataset.itemId;
            
                        // Ensure itemId is present
                        // if (!itemId) throw new Error("Item ID is missing.");
            
                        // Make the DELETE request
                        const response = await fetch(`/invoicing/delete/ticket-item/${itemId}/`, {
                                    method: "DELETE",
                            headers: { "Content-Type": "application/json" }
                        });
            
                        // Check for a successful response
                        if (!response.ok) throw new Error("Error occurred while deleting invoice.");
                        
                        // Parse the response JSON 
                        const responseData = await response.json();
                        console.log("Deleted successfully:", responseData);
            
                        // Remove the item row from the table
                        button.closest('tr').remove();
                        alert("Invoice Item deleted successfully.");
                        window.location.reload()
                    } catch (error) {
                        console.error("Error:", error.message);
                        // alert("Failed to delete the invoice item.");
                    }
                });
            });

        });
});
// "subtotal":Decimal(total_amount)-Decimal(final_tax),
//             "total_amount": total_amount,
//             "final_tax": final_tax
function updatePageMonetry(subtotal,final_tax,total_amount){
    const subtotalElement = document.getElementById('subtotal')
    const totalTaxElement = document.getElementById('total-tax')
    const finalAmountElement = document.getElementById('final-amount')

    subtotalElement.textContent = parseFloat(subtotal).toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});
    
    totalTaxElement.textContent = parseFloat(final_tax).toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});

    finalAmountElement.textContent = (total_amount).toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});

}


// Collect input data and send via fetch
document.getElementById('update-invoice-btn').addEventListener('click', async () => {
    try {
        const invoice = document.getElementById("invoice").value.trim();
        if (!invoice) {
            alert('No invoice number found!');
            return;
        }
        document.querySelectorAll('.defaut-fields').forEach(el=>{
            el.style.display = "none"
        })

        // Get all rows in the invoice table (skip hidden rows)
        const rows = document.querySelectorAll('#invoice-items tbody tr');
       

        // Extract data only from visible rows and inputs
        const items = Array.from(rows).map(row => {
            // Skip rows with "display: none"
            if (window.getComputedStyle(row).display === 'none') {
                return null;
            }

            return {
                service_name: getVisibleInput(row, 'service_name'),
                description: getVisibleInput(row, 'description'),
                quantity: parseInt(getVisibleInput(row, 'quantity'), 10),
                price_per_unit: parseFloat(getVisibleInput(row, 'price_per_unit')),
                taxes: parseFloat(getVisibleInput(row, 'tax')) || 0
            };
        }).filter(item => item && item.service_name && item.quantity > 0);

        if (items.length === 0) {
            alert('No valid items to update!');
            return;
        }

        console.log('Data to send:', items);

        // Send data via fetch API
        const response = await fetch(`/invoicing/update/ticket-invoice/${invoice}/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error from server:', errorData);
            throw new Error('An error occurred while updating the  invoice');
        }

        alert('Invoice updated successfully');
        document.location.reload()
    } catch (err) {
        console.error('Update error:', err);
        alert(`Error: ${err.message}`);
    }
});

// Helper function to get value of visible input only
function getVisibleInput(row, name) {
    const input = row.querySelector(`input[name="${name}"]`);
    return input && window.getComputedStyle(input).display !== 'none' ? input.value : null;
}
