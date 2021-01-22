var app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
        listOfItems: []
    },
    methods: {
        addItem: function() {
            this.listOfItems.push({"barang": null, "merek": null, "harga": null});
            this.$nextTick(() => {
                $(".listitems").autocomplete({
                    source: availableItems
                });
                $(".listbrands").autocomplete({
                    source: availableBrands
                });
            });
        },
        removeItem: function(index) {
            if (index > -1) {
                this.listOfItems.splice(index, 1);
            }
        }
    }
});