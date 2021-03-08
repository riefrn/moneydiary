var $ = jQuery.noConflict();

function getParameterByName(name, url) {
    if (!url) {
        url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return '';
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('.pickdate').datepicker({
        autoclose: true
    });

    $('.popupdate').datepicker({
        format: "dd-M-yyyy",
        changeMonth: true,
        changeYear: true,
        autoclose: true,
        startDate: '1800-01-01'
    });

    $('.datepopup').datepicker({
        format: "dd-M-yyyy",
        changeMonth: true,
        changeYear: true,
        startDate: new Date(),
    });

    $('.popupdatetime').datetimepicker({
        format: 'DD-MMM-YYYY hh:mm A'
    });

    $('#datetimepopup').datetimepicker({
        format: 'DD-MMM-YYYY HH:mm'
    });

    $('#datetimepopupsecond').datetimepicker({
        format: 'DD-MMM-YYYY HH:mm'
    });

    $('.popupdatetimerange').daterangepicker({
        timePicker: true,
        locale: {
            format: 'DD MMM YYYY hh:mm A'
        }
    });

    $('#popuptime').datetimepicker({
        format: 'HH:mm'
    });

    $('#popuptimepicker').datetimepicker({
        format: 'HH:mm'
    });

    $('#popuppaymentduetime').datetimepicker({
        format: 'HH:mm'
    });


    $("#example1").DataTable();
    $("#example2").DataTable({
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf'
        ]
    });

    $('#weekly_expenses').select2({
        placeholder: "Select weekly expenses",
        allowClear: true
    });

    $("#form-add-weekly-expenses").validationEngine();
    $("#form-edit-weekly-expenses").validationEngine();
    $("#form-add-transaction-index").validationEngine();
    $("#form-form-add-note").validationEngine();
    $("#form-form-edit-note").validationEngine();
    $("#form-filter-date").validationEngine();
    $('#spending').change(function () {
        var spending = $(this).val();
        console.log(spending);
        $("#weekly_expenses").select2({
            ajax: {
                type: "post",
                beforeSend: function (xhr, settings) {
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                },
                url: "/filter-weekly-expenses/",
                delay: 250,
                dataType: 'json',
                data: function (params) {
                    return {
                        spending: spending,
                        q: params.term, // search term
                        page: params.page,
                    };
                },
                processResults: function (data, params) {
                    return {
                        results: $.map(data, function (item) {
                            return {
                                text: item.weekly_expenses_name,
                                id: item.weekly_expenses_id
                            }
                        })
                    };
                },
                cache: true
            },
            placeholder: "Select weekly expenses",
            allowClear: true
        });
    });

});
