function request_test()
{
    var x_data = [0, 1, 2, 3, 4, 5];
    var y_data = [0, 1, 4, 9, 16, 25];

    $.ajax({
        type: "POST",
        url: "<URL OF FLACK FILE ON OTHER INSTANCE>/generate_plot",
        data: JSON.stringify({x_data: x_data, y_data: y_data}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response)
        {
            var img = new Image();
            img.src = 'data:image/png;base64,' + response.image;
            document.getElementById('plot_container').appendChild(img);
        },
        error: function(_, _, error)
        {
            console.error('Error:', error);
        }
    });

}
