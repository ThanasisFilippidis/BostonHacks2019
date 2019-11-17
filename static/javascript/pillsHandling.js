function ajaxSetup() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function add(){

}


$(document).ready(function () {

    $('.cellPills').on('click', function (event) {
        alert("hi")
        // moreView(this);

    });

    $('#selected').on('click', '.deletion', function (event) {
        // remove(this);
    });

    $('#cellPills').on('click', '.addition', function (event) {
        // add(this)
    });


});