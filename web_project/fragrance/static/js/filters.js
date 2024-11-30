document.addEventListener('DOMContentLoaded', function () {
    const sortFilter = document.getElementById('sort-filter');
    const dealsFilter = document.getElementById('deals-filter');

    function updateProducts() {
        const sort = sortFilter.value;
        const deals = dealsFilter.value;
        const category = document.querySelector('#products-container').dataset.category;

        fetch(`/shop/${category}/?sort=${sort}&sale=${deals}`)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('products-container');
                container.innerHTML = '';

            
                data.fragrance.forEach(frag => {
                    const productHTML = `
                        <div class="col">
                            <div class="card" style="width: 18rem;">
                                <img src="${frag.img}" class="card-img-top" alt="${frag.name}">
                                <div class="card-body">
                                    <h5 class="card-title">${frag.name}</h5>
                                    ${
                                        frag.isOnSale
                                            ? `<p class="card-text"><span style="text-decoration: line-through;">$${frag.price}</span>
                                                <span style="color: red;">$${frag.salePrice}</span></p>`
                                            : `<p class="card-text">$${frag.price}</p>`
                                    }
                                    <a href="#" class="btn btn-primary">Add to Cart</a>
                                </div>
                            </div>
                        </div>
                    `;
                    container.insertAdjacentHTML('beforeend', productHTML);
                });
            })
            .catch(error => console.error('Error fetching products:', error));
    }

    sortFilter.addEventListener('change', updateProducts);
    dealsFilter.addEventListener('change', updateProducts);
});
