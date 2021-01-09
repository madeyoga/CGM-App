var app = new Vue({
    el: "#app",
	delimiters: ['[[', ']]'],
    data: {
        ongoingOrders: initialData,
        selectedData: null
    },
    methods: {
        addNewOrderField: function() {
            this.ongoingOrders.push({});
        },
    }
});

var editApp = new Vue({
    el: "#edit_app",
    delimiters: ['[[', ']]'],
    data: {
        idOrder: null,
        tanggalOrder: new Date(),
		namaBarang: null,
        hargaBarang: null,
        jumlahBarang: null,
        note: null,
        tanggalDatang: null,
		deleteUrl: null
    },
    methods: {
        showModal: function(selectedData) {
            this.idOrder = selectedData.id;
            this.tanggalOrder = moment(selectedData.tanggal_order).format('YYYY-MM-DD\THH:mm');
            this.namaBarang = selectedData.nama_barang;
            this.jumlahBarang = selectedData.jumlah;
            this.hargaBarang = selectedData.harga;
            this.note = selectedData.note;

            var tempCompleteDate = selectedData.tanggal_datang;
            if (tempCompleteDate == null) {
                this.tanggalDatang = "";
            }
            else {
                this.tanggalDatang = moment(tempCompleteDate).format('YYYY-MM-DD\THH:mm');
            }

            this.deleteUrl = "/webclient/delete_order/" + selectedData.id;
            $('#edit_modal').modal('show');
        },
        closeModal: function() {
			$("#edit_modal").modal("hide");
		},
    }
})
