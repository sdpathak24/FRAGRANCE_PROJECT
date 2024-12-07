document.addEventListener("DOMContentLoaded", function () {
  const submitButton = document.getElementById("checkout-button");
  const thankYouMessage = document.getElementById("thank-you");
  const formPayment = document.getElementById("paymentForm"); 
//   const submitPaymentButton = document.getElementById("submit-button");

  if (submitButton) {
    submitButton.addEventListener("click", function (e) {
      e.preventDefault();
      if (!paymentForm.checkValidity()) {
            console.log('Please fill in all required fields.');
            paymentForm.reportValidity(); 
        return;
        }
    console.log('Form is valid, proceeding with submission');

      fetch("/clearCart/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify({ action: "clearCart" }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            formPayment.style.display = "none";
            thankYouMessage.style.display = "block";
          } else {
            console.error("Failed to clear cart:", data.message);
          }
        })
        .catch((error) => {
          console.error("Error during cart clear:", error);
        });
    });
  }
});
