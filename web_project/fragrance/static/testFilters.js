// Attach event listeners to the filter elements
document.getElementById('sort-filter').addEventListener('change', updateFilters);
document.getElementById('popularity-filter').addEventListener('change', updateFilters);
document.getElementById('sale-filter').addEventListener('change', updateFilters);

function updateFilters() {
    const category = document.getElementById('products-container').dataset.category;

    const priceSort = document.getElementById('sort-filter').value;
    const popularity = document.getElementById('popularity-filter').value;
    const sale = document.getElementById('sale-filter').checked ? 'onSale' : ''; // Sale filter checkbox

    // Construct the query string for the filters
    const queryString = new URLSearchParams({
        priceSort: priceSort,
        popularity: popularity,
        sale: sale
    }).toString();

    // Send an AJAX request to the server with the selected filters
    fetch(`/shop/${category}/?${queryString}`)
        .then(response => response.json())
        .then(data => {
            // Update the product list with the new data
            const productContainer = document.getElementById('products-container');
            productContainer.innerHTML = ''; // Clear the current products

            data.fragrance.forEach(frag => {
                const productHTML = `
                    <div class="col">
                        <div class="card" style="width: 18rem;">
                            <img src="${frag.img_url}" class="card-img-top" alt="${frag.name}">
                            <div class="card-body">
                                <h5 class="card-title">${frag.name}</h5>
                                <p class="card-text">
                                    ${frag.isOnSale 
                                        ? `<span style="text-decoration: line-through;">$${frag.price}</span> 
                                           <span style="color: red;">$${frag.sale_price}</span>`
                                        : `$${frag.price}`
                                    }
                                </p>
                                <a href="#" class="btn btn-primary">Add to Cart</a>
                            </div>
                        </div>
                    </div>
                `;
                productContainer.insertAdjacentHTML('beforeend', productHTML);
            });
        })
        .catch(error => {
            console.error('Error fetching filtered data:', error);
        });
}
