$(document).ready(function() {
    var table = $('#table-items').DataTable();

    $('#table-items tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('.dataTable').on('dblclick', 'tbody td', function() {
        app.selectedData = app.initialData.find((item) => item.id == this.parentNode.id);
        console.log(app.selectedData);

        // Show modal
	})
});
