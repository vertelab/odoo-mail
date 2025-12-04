import { Message } from "@mail/core/common/message_model";
import { Record } from "@mail/core/common/record";

import { patch } from "@web/core/utils/patch";
//import { SESSION_STATE } from "@mail/core/common/livechat_service";

patch(Message.prototype, {

//    canAddReaction(thread) {
//        return (
//            super.canAddReaction(thread) &&
//            (thread?.channel_type !== "livechat" ||
//                this.store.env.services["im_livechat.livechat"].state === SESSION_STATE.PERSISTED)
//        );
//    },
    canReplyTo(thread) {
        console.log("==========")
        return (
            super.canReplyTo(thread) &&
            (
                thread?.channel_type !== "livechat" ||
                this.store.env.services["im_livechat.chatbot"].inputEnabled
            )
        );
    },
});
