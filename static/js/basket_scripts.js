window.onload = function () {
    console.log('DOM loaded');
    $('.basket_list').on('change', 'input[type=number]', function (event) {
        $.ajax({
            url: "/basket/update/" + event.target.name + "/" + event.target.value + "/",
            success: function (data) {
                if (data.result) {
                    $('.basket_list').html(data.result);
                }
            }
        });
    })
};