console.log("Load app")
console.log(initialData);
var app = new Vue({
	el: "#app",
	delimiters: ['[[', ']]'],
	data: {
		initialData: initialData,
		hargaBarang: null,
		hargaBarangPreview: "",
		selectedData: null
	},
	methods: {
		processNumber: function() {
			var number_string = this.hargaBarang.toString();
			var	sisa = number_string.length % 3;
			var	rupiah = number_string.substr(0, sisa);
			var	ribuan = number_string.substr(sisa).match(/\d{3}/g);

			if (ribuan) {
				separator = sisa ? '.' : '';
				rupiah += separator + ribuan.join('.');
			}
			this.hargaBarangPreview = rupiah;
		},
		refreshData: function() {
			var button = document.getElementById("refresh-button");
			
			// Disable
			button.disabled = true;

			fetch("/api/items/")
			.then((response) => response.json())
			.then(function (data) {
				console.log(data);
				app.initialData = data;
			}).catch(function (err) {
				console.warn('Something went wrong.', err);
			});

			// Enable after 6 seconds.
			setTimeout(() => {button.disabled = false;}, 6000);
		},
	}
});

var editApp = new Vue({
	el: "#edit_app",
	delimiters: ['[[', ']]'],
	data: {
		hargaBarang: null,
		hargaBarangPreview: "",
		idBarang: null,
		namaBarang: null,
		namaMerek: null,
		partNomerBarang: null,
		quantity: null,
		deleteUrl: null,
		location: null,
		previewImage: null,
	},
	methods: {
		processNumber: function() {
			var number_string = this.hargaBarang.toString();
			var	sisa = number_string.length % 3;
			var	rupiah = number_string.substr(0, sisa);
			var	ribuan = number_string.substr(sisa).match(/\d{3}/g);

			if (ribuan) {
				separator = sisa ? '.' : '';
				rupiah += separator + ribuan.join('.');
			}
			this.hargaBarangPreview = rupiah;
		},
		showModal: function(selectedData) {
			this.idBarang = selectedData.id;
			this.namaBarang = selectedData.nama_barang;
			this.namaMerek = selectedData.merek__nama_merek;
			this.hargaBarang = selectedData.harga;
			this.hargaBarangPreview = selectedData.harga_preview;
			this.partNomerBarang = selectedData.part_nomor_barang;
			this.quantity = selectedData.quantity;
			this.deleteUrl = "/webclient/delete_item/" + selectedData.id;
			this.location = selectedData.location;
			if (selectedData.preview_image != '-' && selectedData.preview_image != '' && selectedData.preview_image != null) {
				this.previewImage = "/media/" + selectedData.preview_image;
			}
			else {
				this.previewImage = null;
			}
			document.getElementById('upload_filename_modal').innerHTML = 'Choose File';

			$('#edit_modal').modal('show');
		},
		closeModal: function() {
			$("#edit_modal").modal("hide");
		},
	}
});

$("#preview_image").change(function(){
	readURL(this, '#live_preview');
	document.getElementById("upload_filename").innerHTML = this.value;
});

$("#live_preview").click(function() {
	$('#preview_image').trigger('click');
});

$("#preview_image_modal").change(function(){
	readURL(this, '#live_preview_modal');
	document.getElementById("upload_filename_modal").innerHTML = this.value;
});

function readURL(input, previewElementId) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(previewElementId).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}
