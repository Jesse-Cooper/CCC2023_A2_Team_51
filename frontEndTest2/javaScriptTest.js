function request_test()
{
    var x_data = [0, 1, 2, 3, 4, 5];
    var y_data = [0, 1, 4, 9, 16, 25];

    $.ajax({
        type: "POST",
        url: "http://172.26.136.42:5000/generate_plot",
        data: JSON.stringify({x: x_data, y: y_data}),
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
