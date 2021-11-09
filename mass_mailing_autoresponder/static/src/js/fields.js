odoo.define('mass_mailing_autoresponder.fields', function (require) {

var FieldTextHtml = require('web_editor.backend').FieldTextHtml;

FieldTextHtml.include({

    /**
     * Set the value when the widget is fully loaded (content + editor).
     *
     * @override
     */
     /**
     * Do not re-render this field if it was the origin of the onchange call.
     *
     * @override
     */
    reset: function (record, event) {
        this._reset(record, event);
        if (!event || event.target !== this) {
            if (this.mode === 'edit') {
                this.$body.find("#editable_area").html(this.value);
            }
        }
        return $.when();
    },
});

});
