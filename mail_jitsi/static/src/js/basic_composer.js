odoo.define('mail.composer.Basic.Jitsi', function (require) {
"use strict";

var jitsi = require('mail.jitsi');


var config = require('web.config');
var core = require('web.core');
var data = require('web.data');
var dom = require('web.dom');
var session = require('web.session');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;

var BasicComposer = Widget.extend({
    template: "mail.Composer",
    events: {
        'click .o_composer_button_jitsi': '_onJitsiButtonClick',
    },
    // RPCs done to fetch the mention suggestions are throttled with the
    // following value
    MENTION_THROTTLE: 200,

    init: function (parent, options) {
        this._super.apply(this, arguments);
        this.options = _.defaults(options || {}, {
            commandsEnabled: true,
            context: {},
            inputMinHeight: 28,
            mentionFetchLimit: 8,
            // set to true to only suggest prefetched partners
            mentionPartnersRestricted: false,
            sendText: _t("Send"),
            defaultBody: '',
            defaultMentionSelections: {},
            isMobile: config.device.isMobile
        });
        this.context = this.options.context;





    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------


    /**
     * Called when the jitsi button is clicked -> adds jitsi-link.
     * Also, this method is in charge of the rendering of this panel the first
     * time it is opened.
     *
     * @private
     */
    _onJitsiButtonClick: function () {
	alert('Hejsan');
	console.log('hekk');
        this.$input.val(this.$input.val() + " " + $(ev.currentTarget).data('jitsi') + " ");
    },
    /**

});

return BasicComposer;

});
