$(document).ready(function () {
    var calling_rss_api = function(rss) {
        console.log('calling rss server api');
        $.get('http://localhost:7000/get_rss_feed', { 'rss': rss } , function (data) {
        $('#feed-table tbody').empty();
        headlines = data
        for (var i = 0; i < headlines.length; i++) {
            var tableRow = $('<tr/>');
            var tableData = $('<td/>');
            var new_link = $('<a/>');
            new_link.text(headlines[i]['title']);
            new_link.attr('href', headlines[i]['link']);
            new_link.attr('target', "_blank");
            tableData.append(new_link);
            tableRow.append(tableData);
            $('#feed-table tbody').append(tableRow);
        }
        },'json');
    }
    var refreshing_rss_api = function (rss) {
        console.log('calling rss server api');
        $.get('http://localhost:7000/refresh_rss_feed', { 'rss': rss }, function (data) {
            $('#feed-table tbody').empty();
            headlines = data['headlines'];
            refreshTime =   data['refresh'];
            $('#refresh').text('Last refresh time: ' + refreshTime);
            for (var i = 0; i < headlines.length; i++) {
                var tableRow = $('<tr/>');
                var tableData = $('<td/>');
                var new_link = $('<a/>');
                new_link.text(headlines[i]['title']);
                new_link.attr('href', headlines[i]['link']);
                new_link.attr('target', "_blank");
                tableData.append(new_link);
                tableRow.append(tableData);
                $('#feed-table tbody').append(tableRow);
            }
        }, 'json');
    }
    var selectedRss = $('#list-of-rss').find(":selected").val();
    calling_rss_api(selectedRss);
    //need to code the refresh button
    $('#refresh-button').on('click', function() {
        selectedRss = $('#list-of-rss').find(":selected").val();
        refreshing_rss_api(selectedRss); 
    });
    
    $('#list-of-rss').on('change', function() {
        selectedRss = $('#list-of-rss').find(":selected").val();
        calling_rss_api(selectedRss);
    });
    /*
    $.ajax({
            type: "POST",
            url: "http://localhost:7001/add_user",
            data: JSON.stringify({
                user: $('#user').val()
            }),
            dataType: 'json',
            contentType: 'application/json',*/
});
