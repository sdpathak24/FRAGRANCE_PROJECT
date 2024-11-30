function addToCart(productId, price) {
    const quantityInput = document.getElementById(`quantity-${productId}`);
    const quantity = parseInt(quantityInput.value);

    if (isNaN(quantity) || quantity <= 0) {
        alert("Please enter a valid quantity.");
        return;
    }

    fetch('/addToCart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include CSRF token for Django
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
            total_price: price * quantity
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Failed to add to cart.");
        }
    })
    .then(data => {
        alert(`${quantity} item(s) added to cart!`);
    })
    .catch(error => {
        console.error(error);
        alert("An error occurred while adding to the cart.");
    });
}

// Helper function to get the CSRF token from cookies
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null;
}
