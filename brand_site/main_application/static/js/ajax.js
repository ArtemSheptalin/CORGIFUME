$(function() {
    $('.addCartClass').on('submit', function(e){ 
        e.preventDefault();
        let product_id = $(this).find('[name="product_id"]').attr('id').split('_')[1];
        console.log(product_id, 'pr_id');
        $.ajax({
            url: '/add-certain-amount/',
            type: 'post',
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
            if (response.success) {
                console.log(response);
                let value = $('#quantityID_' + product_id).text();
                $('#quantityID_' + product_id).text(Number(value) + 1);
                let amount = $('#productAmount_' + product_id).text().split(' ')[0];
                $('#productAmount_' + product_id).text(Number(amount) + 1 + ' шт.');
                console.log(response)
                console.log(value);         
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
        console.log(product_id, 'pr_id');
        $.ajax({
            url: '/remove/',
            type: 'post',
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
            if (response.success) {
                console.log(response);
                let value = $('#quantityID_' + product_id).text();
                $('#quantityID_' + product_id).text(Number(value) - 1);
                let amount = $('#productAmount_' + product_id).text().split(' ')[0];
                $('#productAmount_' + product_id).text(Number(amount) - 1 + ' шт.');
                console.log(response)
                console.log(value);         
            } else {
                console.log(response);
            }
        }
     });     
  });
});

$(function() {
    $('.CardForm').on('submit', function(e){ 
        e.preventDefault();
        var product_id = $(this).find('[name="card_product_id"]').attr('id');

        console.log(product_id, 'another_form');

        $.ajax({
            url: '/add-to-cart/',
            type: 'post',
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
                if (response.success) {
                    
                } else {
                    console.log(response);
                }
        }
     });     
  });
});



// Страница Корзины


