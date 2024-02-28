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
    $('.addOneProduct').on('submit', function(e){ 
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
                    window.location.href = 'https://1f24-192-109-241-91.ngrok-free.app/cart/';
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
    $('.addCartClass__first_instance').on('submit', function(e){ 
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
                    let value = $('#quantityID_mobile_' + product_id).text();
                    $('#quantityID_mobile_' + product_id).text(Number(value) + 1);
                    if ((response.cart_quantity) < 1) {
                        $('#icon_ID').html('<p>Моя корзина</p>');
                    } else {
                        $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                        $('#item_total_price_' + product_id).html('<p>' + (response.price * response.product_amount) + ',00 RUB</p>');
                        $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                        $('#bonuses_ID').html('<p>' + (response.bonuses) + '</p>');
                        $('#bonusesID__' + product_id).html('<div>' + (response.product_bonuses) + '</div>');
                    }
                } else {
                    console.log(response);
                }
            }
        });     
    });
});

$(function() {
    $('.removeCartClass__first_instance').on('submit', function(e){ 
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
                let value = $('#quantityID_mobile_' + product_id).text();
                let result_value = Number(value) - 1
                let current_price = $('#item_total_price_' + product_id).text().split(',')[0];
                
                $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                $('#quantityID_mobile_' + product_id).text(result_value);
                $('#item_total_price_' + product_id).html('<p>' + (current_price - response.price) + ',00 RUB</p>');
                $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                $('#bonuses_ID').html('<p>' + (response.bonuses) + '</p>');
                $('#bonusesID__' + product_id).html('<div>' + (response.product_bonuses) + '</div>');
            
            } else {
                console.log(response);
            }
        }
    });     
  });
});

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
                        $('#bonusesID__' + product_id).html('<div>' + (response.product_bonuses) + '</div>');
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
                let current_price = $('#item_total_price_' + product_id).text().split(',')[0];
                
                $('#icon_ID').html('<p>Моя корзина (' + (response.cart_quantity) + ')</p>');
                $('#quantityID_' + product_id).text(result_value);
                $('#item_total_price_' + product_id).html('<p>' + (current_price - response.price) + ',00 RUB</p>');
                $('#total_price').html('<p>' + (response.total_price) + 'RUB</p>');
                $('#bonuses_ID').html('<p>' + (response.bonuses) + '</p>');
                $('#bonusesID__' + product_id).html('<div>' + (response.product_bonuses) + '</div>');
            
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
                    $('#basket__bottom').remove();
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
                $('#basket__bottom').remove();
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
    $('.making__form').on('submit', function(e){ 
        e.preventDefault();
        let bonuses = $('#bonuses_formID').val();
        let promo = $('#promo_formID').val();
        let delivery = $('#delivery-moscow').val();
        let shipment_type = $('#way1').val();
        let city = $('#city_ID').val();
        let index = $('#index_ID').val();
        let street = $('#street_ID').val();
        let house = $('#house_ID').val();
        let corp = $('#corp_ID').val();
        let room = $('#room_ID').val();
        let shipment_date = $('#shipment_date_ID').val()
        let order_price = $('#res_price_ID').text();
        let comment = $('#comment_ID').val()

        $.ajax({
            url: "/order/check-bonuses/",
            type: 'POST',
            data: {
                input_bonuses: bonuses,
                input_promo: promo,
                delivery: delivery,
                shipment_type: shipment_type,
                city: city,
                index: index,
                street: street,
                house: house,
                corp: corp,
                room: room,
                shipment_date: shipment_date,
                order_price: order_price,
                comment: comment,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
            if (response.success && response.both_correct) {
                $('#promo_formID').addClass('promocode_ok');
                $('#bonuses_formID').addClass('promocode_ok');
                window.location.href = 'https://1f24-192-109-241-91.ngrok-free.app/order/tinkoff-kassa/';
            } else if (response.success && response.promocode && response.bonuses === false) {
                $('#promo_formID').addClass('promocode_ok');
                $('#bonuses_formID').addClass('promocode_error');
            } else if (response.success && response.promocode === false && response.bonuses) {
                $('#promo_formID').addClass('promocode_error');
                $('#bonuses_formID').addClass('promocode_ok');
            } else {
                $('#promo_formID').addClass('promocode_error');
                $('#bonuses_formID').addClass('promocode_error');
                
            }
        },
    });     
  });
});

