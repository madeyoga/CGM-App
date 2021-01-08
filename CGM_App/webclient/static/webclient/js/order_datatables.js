$(document).ready(function() {
    var table = $('#table-ongoing-orders').DataTable();

    $('#table-ongoing-orders tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected')) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('.dataTable').on('doubletap', 'tbody td', function(e) { 
        app.selectedData = app.initialData.find((item) => item.id == this.parentNode.id);
        console.log(app.selectedData);

        // Show modal
        editApp.showModal(app.selectedData);
    });
});