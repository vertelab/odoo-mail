function clicked(e) {
    if(!confirm) {
        e.preventDefault();
    }
}


document.onkeydown = function(evt) {
    let isEscape;
    if ("key" in evt) {
        isEscape = evt.key == "Escape" || evt.key == "Esc";
    } else {
        isEscape = evt.keyCode == 27;
    }
    if (isEscape) {
        closeDialog("unsubscribe");
    }
};

$(document).ready(function() {
    $("#other_reason").hide();
    let radio_button = document.getElementsByClassName('opt')
    $(".opt").change(function(){
        if(radio_button[5].checked)
        {
            $("#other_reason").show();
        }
        else
        {
            $("#other_reason").hide();
        }
    });
});

function openDialog(e){
    e.preventDefault()
    let btnID = "unsubscribe"
    let body = document.getElementsByTagName("body");
    let landmarks = document.querySelectorAll("header, main");
    let overlay = document.getElementById("overlay");
    let dialog = document.getElementById("dialog");
    let closeBtn = document.getElementById("dialogClose");
    let submitBtn = document.getElementById("dialogSubmit");
    let focusElm = document.getElementById("dialogSubmit");

    for (let i = 0; i < landmarks.length; i++) {
        landmarks[i].setAttribute("aria-hidden","true");
    }

    body[0].style.overflow = "hidden";
    overlay.style.display = "block";
    overlay.setAttribute("onclick","closeDialog('" + btnID + "');");
    dialog.setAttribute("aria-modal","true");
    dialog.removeAttribute("hidden");
    closeBtn.setAttribute("onclick","closeDialog('" + btnID + "');");
    submitBtn.setAttribute("onclick", "closeDialog('" + btnID + "', true)");
    focusElm.focus();
}

function closeDialog(eID, submit= false) {
    let body = document.getElementsByTagName("body");
    let landmarks = document.querySelectorAll("header, main");
    let overlay = document.getElementById("overlay");
    let dialog = document.getElementById("dialog");
    let triggerBtn = document.getElementById(eID);
    let form = document.getElementById("reason_form");
    let radio_buttons = document.getElementsByClassName('opt');
    let radio = document.querySelectorAll('input[type="radio"]:checked');
    let text_area = document.getElementById("other_reason_textfield");

    for (let i = 0; i < landmarks.length; i++) {
        landmarks[i].removeAttribute("aria-hidden");
    }

    body[0].style.overflow = "auto";
    overlay.style.display = "none";
    dialog.removeAttribute("aria-modal");
    dialog.removeAttribute("data-id");
    dialog.setAttribute("hidden","");
    triggerBtn.focus();

    if (submit){
        if(radio.length === 0){
            radio_buttons[0].checked = "checked";
        }
        else if(radio_buttons[5].checked && text_area.value.length === 0){
            text_area.value = " ";
        }
        form.submit();
    }
}