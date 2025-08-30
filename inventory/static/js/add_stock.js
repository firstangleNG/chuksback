document.addEventListener("DOMContentLoaded", function() {
    const partNameInput = document.getElementById("part_name");
    const suggestionsList = document.getElementById("suggestions");
    const itemStatus = document.getElementById("item-status");
    const lowStockThreshold = document.getElementById("low_stock_threshold");

    // 🔹 Fetch item suggestions when typing
    partNameInput.addEventListener("input", function() {
        let query = partNameInput.value.trim();
        if (query.length > 1) {
            fetch(`/api/inventory/search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsList.innerHTML = "";
                    if (data.length > 0) {
                        data.forEach(item => {
                            let listItem = document.createElement("li");
                            listItem.textContent = item.part_name;
                            listItem.dataset.threshold = item.low_stock_threshold;
                            listItem.addEventListener("click", function() {
                                partNameInput.value = item.part_name;
                                lowStockThreshold.value = item.low_stock_threshold;
                                itemStatus.textContent = `Existing item - Current stock: ${item.quantity_available}`;
                                itemStatus.classList.remove("hidden");
                                suggestionsList.innerHTML = "";
                            });
                            suggestionsList.appendChild(listItem);
                        });
                        suggestionsList.classList.remove("hidden");
                    } else {
                        suggestionsList.classList.add("hidden");
                    }
                })
                .catch(error => console.error("Error:", error));
        } else {
            suggestionsList.classList.add("hidden");
        }
    });

    // Hide suggestions when clicking outside
    document.addEventListener("click", function(event) {
        if (!partNameInput.contains(event.target) && !suggestionsList.contains(event.target)) {
            suggestionsList.classList.add("hidden");
        }
    });
});
