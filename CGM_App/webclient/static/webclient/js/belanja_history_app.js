var app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
        listOfItems: []
    },
    methods: {
        addItem: function() {
            this.listOfItems.push({"barang": null, "harga": null});
        },
        removeItem: function(index) {
            if (index > -1) {
                this.listOfItems.splice(index, 1);
            }
        }
    }
});