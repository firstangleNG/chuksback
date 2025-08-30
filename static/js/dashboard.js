document.addEventListener("DOMContentLoaded",()=>{
    const total_revenue = document.getElementById("total_revenue");
    const pending_payments = document.getElementById("pending_payments");
    
    total_revenue.textContent = parseFloat(total_revenue.textContent).toLocaleString("en-GB",{
        style:"currency",
        currency:"GBP",
        minimumFractionDigits:2,
        maximumFractionDigits:2
    })

    pending_payments.textContent = parseFloat(pending_payments.textContent).toLocaleString("en-GB",{
        style:"currency",
        currency:"GBP",
        minimumFractionDigits:2,
        maximumFractionDigits:2
    })

})