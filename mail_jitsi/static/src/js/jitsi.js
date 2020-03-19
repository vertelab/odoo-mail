odoo.define('mail.jitsi', function (require) {
"use strict";

/**
 * This module integerate meet.jit.si in discuss
 */

function makeid(length) {
   var result           = '';
   var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}


return 'https://meet.jit.si/' + makeid(32);

});
