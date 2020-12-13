console.log("Load app")
console.log(initialData);
var app = new Vue({
	el: "#app",
	delimiters: ['[[', ']]'],
	data: {
		initialData: initialData,
		hargaBarang: null,
		hargaBarangPreview: ""
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
		}
	}
});
