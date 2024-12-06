document.addEventListener("DOMContentLoaded", function () {
  const submitButton = document.getElementById("checkout-button");
  const thankYouMessage = document.getElementById("thank-you");
  const formPayment = document.getElementById("paymentForm");

  if (submitButton) {
    submitButton.addEventListener("click", function (e) {
      e.preventDefault();

      // Simulate cart clearing via AJAX
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
            // Hide the checkout form and show the thank you message
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
