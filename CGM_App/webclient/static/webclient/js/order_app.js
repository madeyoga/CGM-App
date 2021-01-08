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
        onClickSaveButton: function(buttonElement) {
            var dataIndex = buttonElement.parentNode.parentNode.rowIndex - 1;
            console.log(dataIndex);
        },
        onClickRemoveButton: function(buttonElement) {
            var dataIndex = buttonElement.parentNode.parentNode.rowIndex - 1;
            this.ongoingOrders.splice(dataIndex, 1);
            console.log(this.ongoingOrders);
        }
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
		deleteUrl: null
    },
    methods: {
        showModal: function(selectedData) {
            this.idOrder = selectedData.id;
            this.tanggalOrder = moment(selectedData.tanggal_order).format('YYYY-MM-DD\THH:mm');
            this.namaBarang = selectedData.nama_barang;
            this.jumlahBarang = selectedData.jumlah;
            this.hargaBarang = selectedData.harga;
            $('#edit_modal').modal('show');
        },
        closeModal: function() {
			$("#edit_modal").modal("hide");
		},
    }
})
