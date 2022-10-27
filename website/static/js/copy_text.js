function copyToClipboard(TextToCopy) {
    //var text = document.getElementById('yourtext')
    var TempText = document.createElement("textarea");

    TempText.innerHTML = TextToCopy
    //TempText.value = TextToCopy;
    //console.log(TextToCopy)
    document.body.appendChild(TempText);
    TempText.select();
    document.execCommand('copy');

    //alert("Copied the text: " + TempText.value);
}
/**
var buttons = document.getElementsByClassName('btn btn-outline-secondary btn-sm');
for(var i=0; i<buttons.length; i++){
    buttons[i].addEventListener("click", function handleClick(){ 
        this.innerHTML='Copied'
    })
}**/
// add url when someone copied text
document.addEventListener('copy', function (e) {
    var selection = window.getSelection();
    e.clipboardData.setData('text/plain', $('<div/>').html(selection + "").text() + "\n\n" + 'Source: ' +
        document.location.href);
    e.clipboardData.setData('text/html', selection + '<br /><br /><a href="' + document.location.href +
        '">Source</a>');
    e.preventDefault();
});
$(document).ready(function () {
    $('[data-bs-toggle="tooltip"]').hover(function () {
        $(this).tooltip('show')
    });
    $('[data-bs-toggle="tooltip"]').on('click', function () {
        $(this).attr('title', 'Copied').tooltip('dispose').tooltip('show')
    });
});