(function(jsGrid, $, undefined) {
    //用户自定义的浮点数列
    var NumberField = jsGrid.NumberField;

    function FloatNumberField(config) {
        NumberField.call(this, config);
    }

    FloatNumberField.prototype = new NumberField({

        filterValue: function() {
            var value = this.filterControl.val();
            if (value == "")
                return "";
            else
                return parseFloat(value);
        },

        insertValue: function() {
            var value = this.insertControl.val();
            if (value == "")
                return "";
            else
                return parseFloat(value);
        },

        editValue: function() {
            var value = this.editControl.val();
            if (value == "")
                return "";
            else
                return parseFloat(value);
        }
    });

    jsGrid.fields.floatNumber = FloatNumberField;

}(jsGrid, jQuery));
