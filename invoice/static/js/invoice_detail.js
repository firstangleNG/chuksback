// document.addEventListener("DOMContentLoaded",()=>{
//     const subtotal = document.getElementById("subtotal").textContent;
//     const total_tax = document.getElementById("total_tax").textContent;
//     const finat_amount = document.getElementById("final_amount").textContent;

//     const subtotal_new_value = document.getElementById("subtotal");
//     subtotal_new_value.textContent = parseFloat(subtotal).toLocaleString('en-us',{
//         currency:"GBP",
//         style:"currency",
//         maximumSignificantDigits:2,
//         maximumFractionDigits:2
//     })
// })



document.addEventListener("DOMContentLoaded", () => {
    const subtotalElement = document.getElementById("subtotal");
    const total_taxElement = document.getElementById("total_tax");
    const finat_amountElement = document.getElementById("final_amount");

    // Extract numeric value and clean up any unwanted characters
    let subtotal = parseFloat(subtotalElement.textContent.replace(/[^0-9.]/g, ""));
     // Extract numeric value and clean up any unwanted characters
     let total_tax = parseFloat(total_taxElement.textContent.replace(/[^0-9.]/g, ""));
       // Extract numeric value and clean up any unwanted characters
       let final_amount  = parseFloat(finat_amountElement.textContent.replace(/[^0-9.]/g, ""));
    
    if (!isNaN(subtotal)) { 
        subtotalElement.textContent = subtotal.toLocaleString("en-GB", {
            style: "currency",
            currency: "GBP",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }


    if (!isNaN(total_tax)) { 
        total_taxElement.textContent = total_tax.toLocaleString("en-GB", {
            style: "currency",
            currency: "GBP",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    if (!isNaN(final_amount)) { 
        finat_amountElement.textContent = final_amount.toLocaleString("en-GB", {
            style: "currency",
            currency: "GBP",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }


  const invoice_id = document.getElementById("invoice-id").textContent;
  fetchCustomerEmail(invoice_id)
});





const payment_method_select  = document.getElementById("payment-method")
payment_method_select.addEventListener("change",async ()=>{
    const new_payment_method = document.getElementById("payment-method").value;
    const invoice_id = document.getElementById("invoice-id").textContent;
    console.log("payment-method  :",new_payment_method)
    console.log("invoice  :",invoice_id)
    try {
        const response = await fetch('/invoicing/update-payment-method/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                },
            body: JSON.stringify({
                invoice_id: invoice_id,
                payment_method: new_payment_method
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert('Payment method updated successfully!');
            window.location.reload();  // forces DOM to refresh
            console.log('pdated Invoice:', data);
        } else {
            alert('Error: ' + data.message);
            console.warn('Response:', data);
        }

    } catch (error) {
        console.error('Request failed:', error);
        alert('Something went wrong. Check console for details.');
    }
})





const payment_select_element = document.getElementById("payment-status")
payment_select_element.addEventListener("change",async ()=>{
    const new_payment_status = document.getElementById("payment-status").value;
    const invoice_id = document.getElementById("invoice-id").textContent;
    try {
        const response = await fetch('/invoicing/update-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                },
            body: JSON.stringify({
                invoice_id: invoice_id,
                status: new_payment_status
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert('Payment status updated successfully!');
            window.location.reload();  // forces DOM to refresh
            console.log('Updated Invoice:', data);
        } else {
            alert('Error: ' + data.message);
            console.warn('Response:', data);
        }

    } catch (error) {
        console.error('Request failed:', error);
        alert('Something went wrong. Check console for details.');
    }
})




// Function To EMail Invoice to Customer 


const email_messages = document.getElementById('email-messages')
document.getElementById("email-form").addEventListener("submit",async (e)=>{
    e.preventDefault();
   
    const invoice = document.getElementById("re-email-invoice").value.trim();
    const email = document.getElementById("customer_email").value.trim();
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    const response = await fetch(`/invoicing/email-invoice/${email}/${invoice}/`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        }
    });
    const data = await response.json();

    
    if (response.ok) {
        email_messages.style.color = "green";
        email_messages.textContent = "Email sent successfully. The customer  will recieve the email in a while.";
        } else {
     
        email_messages.textContent = `Email not sent. Error occured.${data.error} `
    }
});





// AJAX to get Customer email using the invoice id

async function fetchCustomerEmail(invoiceId) {
    try {
        const response = await fetch('/invoicing/get-customer-email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ invoice_id: invoiceId })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            console.log("Customer Email:", data.customer_email);
            // You can display it or set it in an input:
            document.getElementById("re-email-invoice").value = invoiceId
            document.getElementById("customer_email").value = data.customer_email || "No Email Provided"; 
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Fetch failed:', error);
        alert('Something went wrong');
    }
}



// document.getElementById('print-invoice').addEventListener("click",()=>{
//     const invoiceId = document.getElementById("invoice-id").textContent;
//     getInvoiceItems(invoiceId)
// })

// async function getInvoiceItems(invoiceId) {
//     try {
//         const response = await fetch(`/invoicing/invoice-items/${invoiceId}/`);
//         if (!response.ok) {
//             throw new Error('Failed to fetch invoice items');
//         }
//         const data = await response.json();
        
//         // Process the data
//         console.log(data);  // You can render this data to the DOM or use it elsewhere
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }


// async function getInvoiceItemDetails(itemId) {
//     const serviceNameField = document.getElementById("edit-service-name");
//     const descriptionField = document.getElementById("edit-description");
//     const quantityField = document.getElementById("edit-quantity");
//     const priceField = document.getElementById("edit-price");
//     const taxesField = document.getElementById("edit-taxes");

//     // const itemId = document.getElementById('edit-invoice-id').value.trim();

//     try { 
//         const response = await fetch(`/invoicing/invoice-items/${itemId}/`, {  
//             method: "GET",
//             headers: {
//                 "Content-Type": "application/json",
//             }
//         });

//         openModal('spinner');

//         const data = await response.json(); // Parse JSON response
//         console.log(data)

//         if (response.ok) {
//             closeModal();
//             openModal('edit-invoice');
//             serviceNameField.value = data.service_name;
//             descriptionField.value = data.description;
//             quantityField.value = data.quantity;
//             priceField.value = data.price_per_unit;
//             taxesField.value = data.taxes;
//         } else {
//             alert(`Error: ${data.message || "Something went wrong!"}`);
//         }

//     } catch (error) {
//         console.error("Error fetching invoice item:", error);
//         closeModal();
//         alert("Failed to fetch invoice item. Please try again.");
//     }
// }



async function getInvoiceItemDetails(itemId) {
    const serviceNameField = document.getElementById("edit-service-name");
    const descriptionField = document.getElementById("edit-description");
    const quantityField = document.getElementById("edit-quantity");
    const priceField = document.getElementById("edit-price");
    const taxesField = document.getElementById("edit-taxes");
    const totalField = document.getElementById("edit-total");

    try { 
        const response = await fetch(`/invoicing/invoice-item/${itemId}/`, {  
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        openModal('spinner');

        const data = await response.json(); // Parse JSON response
        console.log(data);

        if (response.ok) {
            closeModal();
            openModal('edit-invoice');

            // Populate form fields with the fetched data
            serviceNameField.value = data.service_name;
            descriptionField.value = data.description;
            quantityField.value = data.quantity;
            priceField.value = data.price_per_unit;
            localStorage.setItem("current-id-of-editing-item",data.id)
            // Handle taxes field (select)
            // const taxOption = data.taxes > 0 ? "taxed" : "not-taxed";
            // taxesField.value = taxOption;
            const taxOption = parseFloat(data.taxes) > 0 ? "20.0" : "0.0";
            taxesField.value = taxOption;


            totalField.value = data.total;
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }

    } catch (error) {
        console.error("Error fetching invoice item:", error);
        closeModal();
        alert("Failed to fetch invoice item. Please try again.");
    }
}




async function updateInvoiceItem() {
    const serviceNameField = document.getElementById("edit-service-name");
    const descriptionField = document.getElementById("edit-description");
    const quantityField = document.getElementById("edit-quantity");
    const priceField = document.getElementById("edit-price");
    const taxesField = document.getElementById("edit-taxes");
    const totalField = document.getElementById("edit-total");

    const itemId = localStorage.getItem("current-id-of-editing-item")


    const selectedTax = taxesField.value;

    //  Check if a tax option is selected
    if (!selectedTax) {
        alert("Please select a tax option.");
        return;
    }
    // Get the form data
    const formData = {
        service_name: serviceNameField.value,
        description: descriptionField.value,
        quantity: quantityField.value,
        price_per_unit: priceField.value,
        taxes: taxesField.value,
        total: totalField.value
    };

    try {
        // Send PUT request to update the invoice item
        const response = await fetch(`/invoicing/invoice-items/${itemId}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message); // Success message
            closeModal(); // Close modal after successful update
           
        } else {
            alert(`Error: ${data.message}`);
        }

    } catch (error) {
        console.error("Error updating invoice item:", error);
        alert("Failed to update invoice item. Please try again.");
    }
}






async function deleteInvoiceItemDetails(itemId) {
    // Show the modal
    const modal = document.getElementById('deleteConfirmModal');
    modal.style.display = 'block';

    // Get the confirmation and cancellation buttons
    const cancelBtn = document.getElementById('cancelBtn');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    // Close the modal if the user clicks the close button (X) or cancel button
    document.getElementById('closeModal').onclick = closeModal;
    cancelBtn.onclick = closeModal;

    // Handle the confirmation when the user clicks "Yes, Delete"
    confirmDeleteBtn.onclick = async function() {
        try {
            const response = await fetch(`/invoicing/invoice-items/${itemId}/delete/`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                }
            });

            const data = await response.json();
            console.log(data);

            if (response.ok) {
                // If successful, reload the page
                document.location.reload();
            } else {
                alert(`Error: ${data.message || "Something went wrong!"}`);
            }

        } catch (error) {
            console.error('Error during the delete operation:', error);
            alert("An unexpected error occurred. Please try again later.");
        }

        // Close the modal after confirming
        closeModal();
    };

    // Close the modal
    function closeModal() {
        modal.style.display = 'none';
    }
}

async function getCustomerName() {
    const invoiceItemId = document.getElementById("invoice-id").textContent.trim();
    const customerNameField = document.getElementById("edit-customer-name");
    try { 
        // Send GET request to fetch the customer name using the invoice item ID
        const response = await fetch(`/invoicing/invoice-item/${invoiceItemId}/customer-name/`, {  
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        openModal('spinner');  // Display loading spinner

        const data = await response.json(); // Parse JSON response
        console.log(data);

        if (response.ok) {
            closeModal(); // Hide spinner
            openModal('edit-customer-name-modal'); // Open modal for editing

            // Populate customer name field with fetched data
            customerNameField.value = data.customer_name;
        } else {
            alert(`Error: ${data.message || "Something went wrong!"}`);
        }

    } catch (error) {
        console.error("Error fetching customer name:", error);
        closeModal();
        alert("Failed to fetch customer name. Please try again.");
    }
}


document.getElementById("edit-customer-name-form").addEventListener("submit", async () => {
    // Get the updated customer name from the input field
    const customerNameFieldValue = document.getElementById("edit-customer-name").value;
    const invoiceId = document.getElementById("invoice-id").textContent.trim();
 
    // Log the values received
    console.log("Submitting customer name update:");
    console.log("Customer Name:", customerNameFieldValue);
    console.log("Invoice ID:", invoiceId);
 
    // Ensure the customer name is not empty
    if (!customerNameFieldValue) {
        alert("Customer name cannot be empty.");
        console.warn("Attempted to submit with an empty customer name.");
        return;
    }
 
    try {
        // Log the request being made
        console.log("Sending request to update customer name...");
        
        // Send PUT request to update the customer name
        const response = await fetch(`/invoicing/invoice-item/${invoiceId}/update-customer-name/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_name: customerNameFieldValue
            })
        });

        const data = await response.json();
        
        // Log the response data
        console.log("Response received:", data);
 
        if (response.ok) {
            alert(data.message || "Customer name updated successfully!"); // Success message
            console.log("Customer name update successful.");
            closeModal(); // Close the modal after successful update
            document.location.reload()
        } else {

            alert(`Error: ${data.message || "Something went wrong!"}`);
            console.error("Error updating customer name:", data.message || "Unknown error");
        }
 
    } catch (error) {
        console.error("Error updating customer name:", error);
        alert("Failed to update customer name. Please try again.");
    }
});


   