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

    $('.dataTable').on('click', 'tbody td', function() {
		//get textContent of the TD
		console.log('TD cell textContent : ', this.textContent)
		console.log(this.parentNode.id);
	})
});
