var progressUrl = "{% url 'celery_progress:task_status' task_id %}";

function customResult(resultElement, result) {
    $(resultElement).append(
        $('<p>').text('Sum of all seconds is ' + result)
    );
}

$(function () {
    CeleryProgressBar.initProgressBar(progressUrl, {
        onResult: customResult,
    })
});