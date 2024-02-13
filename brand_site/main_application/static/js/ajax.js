$(function() {
    $('.addProductClass').on('submit', function(e){ 
        e.preventDefault();
        let product_id = $(this).find('[name="product_id"]').attr('id').split('_')[1];
        
        $.ajax({
            url: '/add-product/',
            type: 'post',
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
                if (response.success) {
                    let value = $('#quantityID_' + product_id).text();
                    $('#quantityID_' + product_id).text(Number(value) + 1);
                    if ((response.cart_quantity) < 1) {
                        $('#icon_ID').html('<p>Моя корзина</p>');
                    } else {
                        $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                        $('#item_total_price_' + product_id).html('<p>' + (response.price * response.product_amount) + ',00 RUB</p>');
                        $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                        $('#product_bonuses_ID').html('<p>' + (response.product_bonuses) + '</p>');
                    }
                } else {
                    console.log(response);
                }
            }
        });     
    });
});

$(function() {
    $('.removeCartClass').on('submit', function(e){ 
        e.preventDefault();
        let product_id = $(this).find('[name="product_id"]').attr('id').split('_')[1];
        $.ajax({
            url: '/remove/',
            type: 'post',
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
            if (response.success) {
                let value = $('#quantityID_' + product_id).text();
                let result_value = Number(value) - 1
                let current_price = $('#item_total_price_' + product_id).text().split(',')[0];
                
                $('#quantityID_' + product_id).text(result_value);
                if ((response.cart_quantity) < 1) {
                    $('#icon_ID').html('<p>Моя корзина</p>');
                    $('#quantityID_' + product_id).text(0);
                    
                } else {
                    $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                    $('#quantityID_' + product_id).text(result_value);
                    $('#item_total_price_' + product_id).html('<p>' + (current_price - response.price) + ',00 RUB</p>');
                    $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                }
            } else {
                console.log(response);
            }
        }
    });     
  });
});


// Страница Корзины

$(function() {
    $('.addCartClass').on('submit', function(e){ 
        e.preventDefault();
        let product_id = $(this).find('[name="product_id"]').attr('id').split('_')[1];
        let current_price = $('#item_total_price_' + product_id).text().split(',')[0];
        $.ajax({
            url: '/add-certain-amount/',
            type: 'post',
            data: {
                product_id: product_id,
                current_price: current_price,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
                if (response.success) {
                    let value = $('#quantityID_' + product_id).text();
                    $('#quantityID_' + product_id).text(Number(value) + 1);
                    if ((response.cart_quantity) < 1) {
                        $('#icon_ID').html('<p>Моя корзина</p>');
                    } else {
                        $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                        $('#item_total_price_' + product_id).html('<p>' + (response.price * response.product_amount) + ',00 RUB</p>');
                        $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                        $('#bonuses_ID').html('<p>' + (response.bonuses) + '</p>');
                        $('#product_bonuses_ID').html('<p>' + (response.product_bonuses) + '</p>');
                    }
                } else {
                    console.log(response);
                }
            }
        });     
    });
});

$(function() {
    $('.removeCartClass__second').on('submit', function(e){ 
        e.preventDefault();
        let product_id = $(this).find('[name="product_id"]').attr('id').split('_')[1];
        let current_price = $('#item_total_price_' + product_id).text().split(',')[0];
        
        $.ajax({
            url: '/remove_second/',
            type: 'post',
            data: {
                product_id: product_id,
                current_price: current_price,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
            if (response.success) {
                let value = $('#quantityID_' + product_id).text();
                let result_value = Number(value) - 1
                
                $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                $('#quantityID_' + product_id).text(result_value);
                $('#item_total_price_' + product_id).html('<p>' + (current_price - response.price) + ',00 RUB</p>');
                $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                $('#bonuses_ID').html('<p>' + (response.bonuses) + '</p>');
                $('#product_bonuses_ID').html('<p>' + (response.product_bonuses) + '</p>');
            
            } else {
                console.log(response);
            }
        }
    });     
  });
});


$(function() {
    $('.removeProductLink').on('click', function(e){ 
        e.preventDefault();
        let product_id = $(this).attr('id').split('_')[1]; 
        
        let deleteUrl = $(this).attr('href');
        $.ajax({
            url: deleteUrl,
            type: 'GET',
            data: {
                product_id: product_id,
            },
            success: function (response) {
            if (response.success) {
                let current_price = $('#item_total_price_' + product_id).text().split(',')[0];
                if (response.cart_quantity >= 1) {
                    $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                    $('#product_row__' + product_id).remove();
                    $('#item_total_price_' + product_id).html('<p>' + (current_price - response.price) + ',00 RUB</p>');
                    $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                    
                } else {
                    $('#icon_ID').html('<p>Моя корзина</p>');
                    $('#product_row__' + product_id).remove();
                    $('#cart__header').remove();
                    $('#cart__body').remove();
                    $('#cart__message').html('<p>В настоящий момент в корзине нет товаров...</p>').css({
                        'display': 'block',
                        'margin-top': '50px',
                        'text-align': 'center'
                      });                      
                }
            } else {
                console.log(response);
            }
        }
    });     
  });
});


$(function() {
    $('.delete__all').on('submit', function(e){ 
        e.preventDefault();
        $.ajax({
            url: '/delete-cart/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
            if (response.success) {
                $('#icon_ID').html('<p>Моя корзина</p>');
                $('#cart__header').remove();
                $('#cart__body').remove();
                $('#cart__message').html('<p>В настоящий момент в корзине нет товаров...</p>').css({
                    'display': 'block',
                    'margin-top': '50px',
                    'text-align': 'center'
                }); 
            
            } else {
                console.log(response);
            }
        }
    });     
  });
});

// Проверка бонусов в форме при формировании заказа

$(function() {
    $('#orderForm').on('submit', function(e){ 
        
        e.preventDefault();
        let input_data = $('#bonuses_formID').val();
        // Добавьте эту строку для проверки значения input_data
        console.log(input_data);

        $.ajax({
            url: "/check-bonuses/",
            type: 'POST',
            data: {
                input_data: input_data,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
            if (response.success) {
                $('#bonuses_formID').addClass('promocode_ok');
            } else {
                console.log(input_data);
                $('#bonuses_formID').addClass('promocode_error');
            }
        },
    });     
  });
});

