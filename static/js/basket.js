window.onload = function () {
    const basket_list = $('.basket_list');
    const products_content = $('.products-content');
    const basketSum = $('.basket-total-sum');
    const basketQuantity = $('.basket-total-quantity');

    basket_list.on('click', 'input[type="number"]', function () {
        const t_href = event.target;

        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: function (data) {
                basket_list.html(data.result);
                var basketNavMenuSum = document.querySelector('.basket-nav-sum');
                var basketSum = document.querySelector('.basket-total-sum');
                basketNavMenuSum.innerText = basketSum.innerText;
            }
        });
    });

    basket_list.on('click', '.trash-button', function () {
        const a_href = event.target;

        $.ajax({
            url: '/baskets/remove/' + a_href.id + '/',
            success: function (data) {
                basket_list.html(data.result);
                var basketNavMenuSum = document.querySelector('.basket-nav-sum');
                var basketSum = document.querySelector('.basket-total-sum');
                basketNavMenuSum.innerText = basketSum.innerText;
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
                        var basketNavMenuSum = document.querySelector('.basket-nav-sum');
                        basketNavMenuSum.innerText = data.total_sum;
                    } else {
                        window.location.pathname = data.redirect_url;
                    }
                }
            });
        }
    });
}