function request_test()
{
    var x_data = [0, 1, 2, 3, 4, 5];
    var y_data = [0, 1, 4, 9, 16, 25];

    $.ajax({
        type: "POST",
        url: "<URL OF FLACK FILE ON OTHER INSTANCE>/generate_plot",
        data: JSON.stringify({x_data: x_data, y_data: y_data}),
        contentType: "application/json; charset=utf-8",
        dataType: "binary",
        success: function(response)
        {
            var img_url = URL.createObjectURL(new Blob([response], {type: 'image/png'}));
            var img_elem = $('<img>').attr('src', img_url);
            $('#plot_container').append(img_elem);
        }
    });
}
