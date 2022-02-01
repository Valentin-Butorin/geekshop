window.onload = function () {
    const basket_list = $('.basket_list');
    const products_content = $('.products-content');
    const basketSum = $('.basket-total-sum');
    const basketQuantity = $('.basket-total-quantity');
    const basketNavMenuSum = $('.basket-nav-sum');

    basket_list.on('click', 'input[type="number"]', function () {
        const t_href = event.target;

        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: function (data) {
                basket_list.html(data.result);
                basketSum.innerText = data.total_sum;
                basketNavMenuSum.innerText = basketSum.innerText;
                console.log(basketSum.innerText);
                console.log(basketNavMenuSum.innerText);
                basketQuantity.innerText = data.total_quantity;
            }
        });
    });

    basket_list.on('click', '.trash-button', function () {
        const a_href = event.target;

        $.ajax({
            url: '/baskets/remove/' + a_href.id + '/',
            success: function (data) {
                basket_list.html(data.result);
                basketSum.innerText = data.total_sum;
                basketNavMenuSum.innerText = basketSum.innerText;
                basketQuantity.innerText = data.total_quantity;
            }
        });
    });

    products_content.on('click', '.btn', function () {
        const button = event.target;

        if (button.classList.contains('btn-outline-success')) {
            $.ajax({
                url: '/baskets/add/' + button.id + '/',
                success: function (data) {
                    if (data.authenticated) {
                        button.classList.toggle('btn-outline-success');
                        button.classList.toggle('btn-outline-danger');
                        button.innerText = 'Уже в корзине';
                        basketSum.innerText = data.total_sum;
                        basketNavMenuSum.innerText = basketSum.innerText;
                    } else {
                        window.location.pathname = data.redirect_url;
                    }
                }
            });
        }
    });
}