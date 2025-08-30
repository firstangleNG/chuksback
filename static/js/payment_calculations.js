document.addEventListener("DOMContentLoaded", function () {
    const addPaymentBtn = document.getElementById("add-payment-btn");
    const paymentContainer = document.getElementById("payment-history-container");
    const paymentMethodInput = document.getElementById("payment-method");
    const paymentAmountInput = document.getElementById("payment-amount");
    const ticketId = localStorage.getItem("current_ticket");

    if (!ticketId) {
        alert("Error: Ticket ID is missing.");
        return;
    }

    // Get Current Date and Time
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleString("en-GB", {
            month: "2-digit",
            day: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            hour12: true
        });
    }

    // Update Invoice Amounts (Subtotal, Tax, Final Amount)
    function updateAmounts() {
        let subtotal = 0;
        let totalTax = 0;

        document.querySelectorAll("#invoice-items tbody tr").forEach(row => {
            const quantity = parseFloat(row.querySelector(".quantity").value) || 0;
            const price = parseFloat(row.querySelector(".price").value) || 0;
            const tax = parseFloat(row.querySelector(".tax").value) || 0;

            const itemTotal = quantity * price;
            const taxAmount = (itemTotal * tax) / 100;

            subtotal += itemTotal;
            totalTax += taxAmount;

            row.querySelector(".total").textContent = (itemTotal + taxAmount).toFixed(2);
        });

        const finalAmount = subtotal + totalTax;

        document.getElementById("subtotal").textContent = subtotal.toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});
        ;
        document.getElementById("total-tax").textContent = totalTax.toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});
        ;
        document.getElementById("final-amount").textContent = finalAmount.toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2});
        // const finalAmountConvertedToNumber= Number(finalAmount.replace(/,/g, ''))
        updateAmountDue(finalAmount);
    }
    

    // Update Amount Due and Handle Change Calculation
    function updateAmountDue(finalAmount) {
        // Calculate total payments made
        const payments = Array.from(paymentContainer.querySelectorAll(".payment-amount"))
            .map(el => parseFloat(el.textContent) || 0)
            .reduce((acc, amt) => acc + amt, 0);

        // Calculate amount due
        // const amountDue = parseFloat(finalAmount- payments) ;

        const amountDue = finalAmount - payments;


        // Handle "Give Change" message
        // const existingChange = document.getElementById("give-change");
        // if (amountDue < 0) {
        //     if (!existingChange) {
        //         const changeEl = document.createElement("p");
        //         changeEl.id = "give-change";
        //         paymentContainer.insertAdjacentElement("afterend", changeEl);
        //     }
        //     document.getElementById("give-change").textContent = `Give change: ${Math.abs(amountDue).toLocaleString('en-GB',{style:"currency",currency:"GBP",minimumFractionDigits:2,maximumFractionDigits:2})}`;

        // } else if (existingChange) {
        //     existingChange.remove();
        // }
    }

    // Save Payment to Backend
    async function savePayment(paymentData) {
        const ticketId = localStorage.getItem("current_ticket");
        try {
            const response = await fetch(`/repairs/payments/?ticket=${ticketId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(paymentData),
            });
            if (!response.ok) throw new Error("Failed to save payment");
            fetchPaymentHistory(); // Refresh payment history
        } catch (error) {
            console.error("Error saving payment:", error);
        }
    }

    // Fetch Payment History from Backend
    async function fetchPaymentHistory() {
        try {
            const response = await fetch(`/repairs/payments/?ticket=${ticketId}`);
            const responseData = await response.json();
            paymentContainer.innerHTML = "";
            responseData.payments.forEach(renderPayment);
            const total_paid_amount = responseData.total_paid_amount;
            const final_amount = parseFloat(document.getElementById("final-amount").textContent.replace(/[^\d.]/g, "")); // Remove currency symbols and commas
            
            const amount_due = document.getElementById("amount_due");
            if (amount_due) {
                amount_due.textContent = (final_amount - total_paid_amount).toLocaleString('en-GB', {
                    style: "currency",
                    currency: "GBP",
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
}



        } catch (error) {
            console.error("Error fetching payments:", error);
        }
    }

    // Delete Payment from Backend
    async function deletePayment(paymentId) {
        try {
            await fetch(`/repairs/payments/delete/${paymentId}/`, { method: "DELETE" });
            fetchPaymentHistory();
            updateAmounts();  // Update amounts after deleting a payment
        } catch (error) {
            console.error("Error deleting payment:", error);
        }
    }

    // Render Payment Entry in DOM
    function renderPayment(payment) {
        const paymentRow = document.createElement("div");
        paymentRow.className = "payment-record";

        paymentRow.innerHTML = `
            <div class="payments-details">
                    <span class="payment-time">${payment.payment_date}</span>-
           
                    <span class="payment-method">${payment.payment_type}</span>:
          
             
                    <span class="payment-amount">${parseFloat(payment.amount).toLocaleString("en-GB",{
                        style:"currency",
                        currency:"GBP",
                        minimumFractionDigits:2,
                        maximumFractionDigits:2
                    })}</span>
      
              
                    <button type="button" class="remove-payment" data-id="${payment.id}">Delete</button>
            </div>
        `;

        // paymentRow.innerHTML = `
        //     <div class="payments-details">
        //        <div class="payments-detail"> <span class="payment-time">${payment.payment_date}</span></div> -
        //          <div class="payments-detail"><span class="payment-method">${payment.payment_type}</span></div> : 
        //          <div class="payments-detail"><span class="payment-amount">${parseFloat(payment.amount).toFixed(2)}</span></div>
        //         <div class="payments-detail"><button type="button" class="remove-payment" data-id="${payment.id}">Delete</button><div>
        //     </div>
        // `;

        paymentContainer.appendChild(paymentRow);

        paymentRow.querySelector(".remove-payment").addEventListener("click", function () {
            deletePayment(payment.id);
        });
    }

    // Handle New Payment Addition
    addPaymentBtn.addEventListener("click", function (e) {
        e.preventDefault();

        const amount = parseFloat(paymentAmountInput.value) || 0;
        if (amount <= 0) return alert("Please enter a valid payment amount.");

        const paymentData = {
            ticket: ticketId,
            payment_type: paymentMethodInput.value,
            amount: amount
        };

        // Save the new payment to the backend
        savePayment(paymentData);

        // Clear input and update amounts
        paymentAmountInput.value = "";
        updateAmounts();
    });

    // Initial load of payment history and calculation
    updateAmounts();
    fetchPaymentHistory();
    updateAmountDueOnPageLoad()
});

// Function to fetch payment count and total amount for a specific ticket
async function updateAmountDueOnPageLoad() {
    const ticketId = localStorage.getItem("current_ticket");
    
    try {
        // Fetch data from the server
        const response = await fetch(`/repairs/payments/amount-due/${ticketId}/`);
        
        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response
        const data = await response.json();
       
        console.log('Payment Details:', data);
   
        const amount_due = parseFloat(data.amount_due);
        
           
        const amount_due_element = document.getElementById("amount_due");
         
            console.log("Amount due as fetched :",amount_due)
            // Update the amount_due element with the formatted result
            amount_due_element.textContent = amount_due.toLocaleString('en-GB', {
                style: "currency",
                currency: "GBP",
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        
    } catch (error) {
        // Handle errors (network issues, server issues, etc.)
        console.error('Error fetching payment details:', error);
    }
}

 


// // Function to fetch payment count and total amount for a specific ticket
// async function updateAmountDueOnPageLoad() {
//     const ticketId = localStorage.getItem("current_ticket")
//     try {
//         // Fetch data from the server
//         const response = await fetch(`/repairs/payments/count/${ticketId}/`);
        
//         // Check if the response is successful
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }

//         // Parse the JSON response
//         const data = await response.json();
       
//         console.log('Payment Details:', data);
//         const total_paid_amount = data.total_amount;
        
//         const final_amount = parseFloat(document.getElementById("final-amount").textContent.replace(/[^\d.]/g, "")); // Remove currency symbols and commas
            
//         const amount_due = document.getElementById("amount_due");
//         if (amount_due) {
//             amount_due.textContent = (final_amount - total_paid_amount).toLocaleString('en-GB', {
//                 style: "currency",
//                 currency: "GBP",
//                 minimumFractionDigits: 2,
//                 maximumFractionDigits: 2
//             });
// }

//     } catch (error) {
//         // Handle errors (network issues, server issues, etc.)
//         console.error('Error fetching payment details:', error);
//     }
// }







