async function loadInventoryData(sku) {
    try {
        const response = await fetch(`/inventory/detail/${sku}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (!response.ok) throw new Error('Failed to fetch inventory data');

        const data = await response.json();

        // Populate the modal fields
        document.getElementById('part_name').value = data.part_name || '';
        document.getElementById('sku').value = data.sku || '';
        document.getElementById('barcode').value = data.barcode || '';
        document.getElementById('category').value = data.category || '';
        document.getElementById('supplier_name').value = data.supplier_name || '';
        document.getElementById('cost_price').value = data.cost_price || '';
        document.getElementById('selling_price').value = data.selling_price || '';
        document.getElementById('quantity').value = data.quantity_available || '';
        document.getElementById('low_stock_threshold').value = data.low_stock_threshold || '';
        document.getElementById('reorder_level').value = data.reorder_level || '';
        document.getElementById('location').value = data.location || '';
        document.getElementById('expiration_date').value = data.expiration_date || '';

        // Open the modal
        document.getElementById('inventory-modal').style.display = 'block';
    } catch (error) {
        console.error('Error loading inventory:', error);
        alert('Error loading inventory: ' + error.message);
    }
}
