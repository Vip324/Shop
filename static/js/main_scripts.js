$( document ).on( 'click' , '.top a' , function(event) {
    if (event.target.hasAttribute('href')) {
        var link = event.target.href + 'ajax/';
        var link_array = link.split('/');
        if (link_array[3] == 'catalog') {
            $.ajax({
                url: link,
                success: function (data) {
                    $('.top').html(data.result);
                },
            });

            event.preventDefault();
        }
    }
});
