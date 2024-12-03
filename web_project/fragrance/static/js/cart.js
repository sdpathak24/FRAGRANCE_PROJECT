document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('submit-payment');
    const thankYouMessage = document.getElementById('thank-you');
    const formPayment = document.getElementById('paymentForm');
    
    if (submitButton) {
        submitButton.addEventListener('click', function (e) {
            e.preventDefault(); 
            if (!paymentForm.checkValidity()) {
                console.log('Please fill in all required fields.');
                paymentForm.reportValidity(); 
                return;
            }
            console.log('Form is valid, proceeding with submission');

            // Simulate cart clearing via AJAX 
            fetch('/fragrance/clearCart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({ action: 'clearCart' })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Cart cleared:', data);

                formPayment.style.display = 'none';
                thankYouMessage.style.display = 'block';
                console.log('Thank you message displayed');
            })
            .catch(error => {
                console.error('Error clearing cart:', error);
            });
        });
    }
});
