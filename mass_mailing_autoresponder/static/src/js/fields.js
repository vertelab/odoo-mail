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

odoo.define('mass_mailing.BasicView', function (require) {
    "use strict";

    let session = require('web.session');
    let BasicView = require('web.BasicView');
    BasicView.include({
        init: function(viewInfo, params) {
            let self = this;
            this._super.apply(this, arguments);
            let model = self.controllerParams.modelName in ['mass_mailing','mail'] ? 'True' : 'False';
            if(model) {
                session.user_has_group('af_security.af_newsletter_manual').then(function(has_group) {
                    if(!has_group) {
                        self.controllerParams.archiveEnabled = 'False' in viewInfo.fields;
                    }
                });
            }
        },
    });
});
