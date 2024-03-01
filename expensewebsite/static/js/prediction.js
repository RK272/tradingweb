function updateProgress() {
    $.ajax({
        url: '/prediction/',
        type: 'POST',
        data: {
            startDate: $('#startDate').val(),
            endDate: $('#endDate').val(),
            symbol: $('#symbol').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            // Update the UI with the received progress data
            console.log('Training progress:', data.progress);
            // Update your UI with the progress information
            $('#progress').text('Training Progress: ' + data.progress + '%');
        }
    });
}

// Call updateProgress every 5 seconds (for example)
setInterval(updateProgress, 5000);