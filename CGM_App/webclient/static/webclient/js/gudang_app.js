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
		}
	}
});
