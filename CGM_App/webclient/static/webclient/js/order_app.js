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
