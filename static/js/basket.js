window.onload = function () {
    const basket_list = $('.basket_list');
    const products_content = $('.content');

    basket_list.on('click', 'input[type="number"]', function () {
        const t_href = event.target;

        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: function (data) {
                basket_list.html(data.result);
            }
        });
    });

    basket_list.on('click', '.trash-button', function () {
        const a_href = event.target;

        $.ajax({
            url: '/baskets/remove/' + a_href.id + '/',
            success: function (data) {
                basket_list.html(data.result);
            }
        });
    });

    products_content.on('click', '.btn', function () {
        const button = event.target;

        $.ajax({
            url: '/baskets/add/' + button.id + '/',
            success: function (data) {
                if (data.authenticated) {
                    products_content.html(data.result);
                } else {
                    window.location.pathname = data.redirect_url;
                }
            }
        });
    });
}