if (typeof (window['$']) == "undefined") {
    setUpAnpCommon();
}

function setUpAnpCommon() {
    if (document != undefined && document != null) {
        document.body.onkeydown = function () {
            var e = arguments[0];
            return CancelEnter(e);
        }
    }
}

String.prototype.trim = function () {
    return this.replace(/^\s*/, "").replace(/\s*$/, "");
}

function CancelEnter(e) {
    var intKeyCode = 0;
    var strTagName = "";
    var inputType = "";
    var blnSubmitForm = true; // Assume No
    // Which browser?
    if (document.all) { // IE
        intKeyCode = event.keyCode;
        strTagName = event.srcElement.tagName;
        inputType = event.srcElement.type;
    } else { // Non IE
        intKeyCode = e.which;
        strTagName = e.target.tagName;
        inputType = e.target.type;
    } // Is this enter?
    if ((intKeyCode != null && intKeyCode == 13)) { // Yes it was enter, only submit if we wasnt in a text area
        if (strTagName.toLowerCase() == "input" && (inputType.toLowerCase() == "text" || inputType.toLowerCase() == "radio" || inputType.toLowerCase() == "checkbox")) {
            return false;
        }
    }
    return true;
} //A method to fire the event handlers contained in an array.
function FireEventHandlers(eventHandlerArray, sender, args) {
    for (var i = 0; i < eventHandlerArray.length; i++) {
        if ("function" == eval("typeof(" + eventHandlerArray[i] + ")")) eval(eventHandlerArray[i] + '(sender, args)');
    }
} //A method to invoke methods dynamically with parameters, if any.
function InvokeMethod(methodName, parameters) {
    if ("function" == eval("typeof(" + methodName + ")")) eval(methodName + "(" + parameters + ");");
    else if ("function" == eval("typeof(window.parent.window." + methodName + ")")) eval("window.parent.window." + methodName + "(" + parameters + ");");
} //A method to get the dimensions of the inner area of a browser.
function GetBrowserDimensions() {
    var height = 0;
    var width = 0;
    if (typeof (window.innerWidth) == 'number') {
        height = window.innerHeight;
        width = window.innerWidth;
    } else if (document.documentElement && (document.documentElement.clientWidth || document.documentElement.clientHeight)) {
        height = document.documentElement.clientHeight;
        width = document.documentElement.clientWidth;
    } else if (document.body && (document.body.clientWidth || document.body.clientHeight)) {
        height = document.body.clientHeight;
        width = document.body.clientWidth;
    }
    return {
        Width: parseInt(width),
        Height: parseInt(height)
    };
}
function GetBrowserScroll() {
    var scrollLeft = 0,
    scrollTop = 0;
    if (typeof (window.pageYOffset) == 'number') {
        scrollLeft = window.pageXOffset;
        scrollTop = window.pageYOffset;
    } else if (document.body && (document.body.scrollLeft || document.body.scrollTop)) {
        scrollLeft = document.body.scrollLeft;
        scrollTop = document.body.scrollTop;
    } else if (document.documentElement && (document.documentElement.scrollLeft || document.documentElement.scrollTop)) {
        scrollLeft = document.documentElement.scrollLeft;
        scrollTop = document.documentElement.scrollTop;
    }
    return {
        Left: scrollLeft,
        Top: scrollTop
    };
}
if ('undefined' != typeof (Sys)) {
    //Ajax event handler initializer
    Sys.Application.add_init(__AppInit);
    //MS Ajax Library Function Patches For FF 3.0
    Sys.UI.DomElement._getCurrentStyle = function Sys$UI$DomElement$_getCurrentStyle(element) {
        if (element.nodeName != "#text") {
            var w = (element.ownerDocument ? element.ownerDocument : element.documentElement).defaultView;
            return ((w && (element !== w) && w.getComputedStyle) ? w.getComputedStyle(element, null) : element.style);
        } else {
            return null;
        }
    }
    // Javascript moved from safari-3ajax-hack.js
    //Safari has issues with asp.net clientside fields validators. This is being used to fix that issue
    Sys.Browser.WebKit = {}; //Safari 3 is considered WebKit
    if (navigator.userAgent.indexOf('WebKit/') > -1) {
        Sys.Browser.agent = Sys.Browser.WebKit;
        Sys.Browser.version = parseFloat(navigator.userAgent.match(/WebKit\/(\d+(\.\d+)?)/)[1]);
        Sys.Browser.name = 'WebKit';
    }
}
var __pageManager; //Ajax event handlers
function __AppInit() {
    if (typeof (Sys.WebForms) !== 'undefined')
        __pageManager = Sys.WebForms.PageRequestManager.getInstance();
    if (__pageManager) {
        __pageManager.add_initializeRequest(__InitializeRequest);
        __pageManager.add_pageLoading(__PageLoading);
        __pageManager.add_pageLoaded(__PageLoaded);
        __pageManager.add_endRequest(__EndRequest);
    }
}
var rqstSts = 0, prcBrSts = 0, pbtid;
//Ajax initialize request handler.
function __InitializeRequest(sender, args) {
    rqstSts = 1;
    prcBrSts = 0;
    //if ("undefined" == typeof(__showAjaxProcessingLoader) || ("undefined" != typeof(__showAjaxProcessingLoader) && __showAjaxProcessingLoader)) InvokeMethod("ToggleModalWindow", "'divLoader', 0, true");
    pbtid = window.setTimeout(function () { checkForProcess() }, 4997);
    if ("undefined" != typeof (__initializeRequestHandlerArray)) FireEventHandlers(__initializeRequestHandlerArray, sender, args);
}
function checkForProcess() {
    if (rqstSts == 1) {
        prcBrSts = 1;
        if ("undefined" == typeof (__showAjaxProcessingLoader) || ("undefined" != typeof (__showAjaxProcessingLoader) && __showAjaxProcessingLoader)) InvokeMethod("ToggleModalWindow", "'divLoader', 0, true");
    }
}
//Ajax page loading request handler.
function __PageLoading(sender, args) {
    if ("undefined" != typeof (__pageLoadingHandlerArray)) FireEventHandlers(__pageLoadingHandlerArray, sender, args);
} //Ajax page loaded handler.
function __PageLoaded(sender, args) {
    if ("undefined" != typeof (__pageLoadedHandlerArray)) FireEventHandlers(__pageLoadedHandlerArray, sender, args);
    InvokeMethod("SetFocus", "");
} //Ajax end request handler.
function __EndRequest(sender, args) {
    if ("undefined" != typeof (__defaultFired)) __defaultFired = false; //To reset the variable after an ajax postback, and let the enter key press event fire again.
    rqstSts = 0;
    window.clearTimeout(pbtid);
    if (prcBrSts == 1) {
        prcBrSts = 0;
        if ("undefined" == typeof (__showAjaxProcessingLoader) || ("undefined" != typeof (__showAjaxProcessingLoader) && __showAjaxProcessingLoader)) InvokeMethod("ToggleModalWindow", "'divLoader', 0, false");
    }
    var error = args.get_error();
    if (null != error) {
        if (error.httpStatusCode == 0) args.set_errorHandled(true);
        else {
            alert(_asyncErrorText);
            args.set_errorHandled(false);
        }
    } else {
        if ("undefined" != typeof (__endRequestHandlerArray)) FireEventHandlers(__endRequestHandlerArray, sender, args); InvokeMethod("SetFocus", "");
    }
} //Displays the specified message and then redirects user to url specified.
function ShowMessageAndRedirect(message, url) {
    if (null != message) alert(message);
    if (null != url) window.location.href = url;
} //Displays the specified message and then redirects user.
function ShowMessageAndRefreshOpener(message) {
    if (null != message) alert(message);
    window.opener.location.href = window.opener.location.href;
    window.close();
} //A method to generate a random byte for the creation of a GUID.
function GUIDByte() {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
} //A method to generate a GUID.
function GenerateGUID() {
    return (GUIDByte() + GUIDByte() + "-" + GUIDByte() + "-" + GUIDByte() + "-" + GUIDByte() + "-" + GUIDByte() + GUIDByte() + GUIDByte());
} //A method to clear a control.
function ClearControl(controlId, param) {
    var control = document.getElementById(controlId);
    if (param == "ChangeDdlList") {
        if (_ddlLastDayAction != null) {
            var lbldiv = document.getElementById(_divLastDayLabel);
            if (_ddlLastDayAction.options[1] != null)
                if (_ddlLastDayAction.options[1].selected == true) {
                    var div = document.getElementById(_divLastDayActionUrl);
                    var rfv = document.getElementById(_rfvLastDayRedirect);
                    var rev = document.getElementById(_revLastDayRedirectUrl);
                    div.style.display = "none";
                    ValidatorEnable(rfv, false);
                    ValidatorEnable(rev, false);
                    lbldiv.style.display = "none";
                }
            var opt = document.createElement("option");
            _ddlLastDayAction.length = 0;
            _ddlLastDayAction.options.add(opt);
            opt.text = _ddlNoLastDayText;
            opt.value = _ddlNoLastDayValue;
            _ddlLastDayAction.options[0].selected = true;
            lbldiv.style.display = "none";
        }
    }
    control.value = '';
    return false;
}

function TextBoxValueChanged(textBoxSender, param2) {
    var txt = document.getElementById(textBoxSender._element.id);
    if (txt != null) {
        if (txt.value != "") {
            _ddlLastDayAction.length = 0;
            var opt1 = document.createElement("option");
            var opt2 = document.createElement("option");
            _ddlLastDayAction.options.add(opt1);
            _ddlLastDayAction.options.add(opt2);
            opt1.text = _ddlLastPageText;
            opt1.value = _ddlLastPageValue;
            opt2.text = _ddlRedirectText;
            opt2.value = _ddlRedirectValue;
            _ddlLastDayAction.options[0].selected = true;
            var div = document.getElementById(_divLastDayActionUrl);
            var rfv = document.getElementById(_rfvLastDayRedirect);
            var rev = document.getElementById(_revLastDayRedirectUrl);
            var lbldiv = document.getElementById(_divLastDayLabel);
            div.style.display = "none";
            ValidatorEnable(rfv, false);
            ValidatorEnable(rev, false);
            lbldiv.style.display = "block";
        }
        return false;
    }
}

//A method to open a popup window.
function PopupWindow(windowUrl, windowWidth, windowHeight, windowName, windowPrefs) {
    if ("undefined" == typeof (windowWidth)) windowWidth = null;
    if ("undefined" == typeof (windowHeight)) windowHeight = null;
    if ("undefined" == typeof (windowName)) windowName = null;
    if ("undefined" == typeof (windowPrefs)) windowPrefs = null;
    var left = (screen.availWidth - (windowWidth == null ? screen.availWidth : windowWidth)) / 2;
    var top = (screen.availHeight - (windowHeight == null ? screen.availHeight : windowHeight)) / 2;
    if (isNaN(left)) left = 0;
    if (isNaN(top)) top = 0;
    var popupWindow = null;
    if (null != windowWidth && null != windowHeight) {
        if (null == windowPrefs) windowPrefs = "location=no, menubar=no, personalbar=no, resizable=yes, scrollbars=yes, status=no, toolbar=no, height=" + windowHeight + ", width=" + windowWidth + ", left=" + left + ", top=" + top;
        else windowPrefs = windowPrefs + ", height=" + windowHeight + ", width=" + windowWidth + ", left=" + left + ", top=" + top;
    } else {
        if (null == windowPrefs) windowPrefs = "location=no, menubar=no, personalbar=no, resizable=yes, scrollbars=yes, status=no, toolbar=no";
    }
    if (null == windowName) windowName = "_blank";
    popupWindow = window.open(windowUrl, windowName, windowPrefs);
    if (null == popupWindow) alert(_popupWindowBlockedText);
    return popupWindow;
}
function SearchFocus(e, searchBtnId, searchUniqueId) {
    var intKeyCode = 0;
    var strTagName = "";
    var blnSubmitForm = true; // Assume No
    // Which browser?
    if (document.all) { // IE
        intKeyCode = event.keyCode;
        strTagName = event.srcElement.tagName;
        inputType = event.srcElement.type;
    } else { // Non IE
        intKeyCode = e.which;
        strTagName = e.target.tagName;
        inputType = e.target.type;
    } // Is this enter?
    if ((intKeyCode != null && intKeyCode == 13)) { // Yes it was enter, only submit if we wasnt in a text area
        if (strTagName.toLowerCase() == "input" && (inputType.toLowerCase() == "text" || inputType.toLowerCase() == "radio" || inputType.toLowerCase() == "checkbox")) {
            var btnSearch = document.getElementById(searchBtnId);
            if (null != searchBtnId && "undefined" != btnSearch) {
                btnSearch.focus();
                if (document.all) {
                    btnSearch.click();
                } else {
                    triggerSearch(searchUniqueId);
                }
            }
            return false;
        }
    }
    return true;
}
function triggerSearch(searchBtnUniqueId) {
    __doPostBack(searchBtnUniqueId, '');
}
function checkIfBoxIsRightOrLeft() {
    var ulLeftPanel;
    var ulRightPanel;
    var __parentDocument = window.parent.document;
    if (__parentDocument != null && __parentDocument != "undefined") {
        if (__parentDocument.getElementsByTagName('ul').length > 0) {
            for (count = 0; count < __parentDocument.getElementsByTagName('ul').length; count++) {
                if (__parentDocument.getElementsByTagName('ul')[count].id.indexOf('ulLeftSec') != -1) {
                    ulLeftPanel = __parentDocument.getElementsByTagName('ul')[count];
                } else if (__parentDocument.getElementsByTagName('ul')[count].id.indexOf('ulRightSec') != -1) {
                    ulRightPanel = __parentDocument.getElementsByTagName('ul')[count];
                }
            }
            if (null != ulLeftPanel && ulLeftPanel != "undefined") {
                if (ulLeftPanel.getElementsByTagName('iframe').length > 0) {
                    for (count = 0; count < ulLeftPanel.getElementsByTagName('iframe').length; count++) {
                        if (ulLeftPanel.getElementsByTagName('iframe')[count] != null && ulLeftPanel.getElementsByTagName('iframe')[count] != "undefined") {
                            if (ulLeftPanel.getElementsByTagName('iframe')[count].id == iFrameId) {
                                return '1';
                            }
                        }
                    }
                }
            }
            if (null != ulRightPanel && ulRightPanel != "undefined") {
                if (ulRightPanel.getElementsByTagName('iframe').length > 0) {
                    for (count = 0; count < ulRightPanel.getElementsByTagName('iframe').length; count++) {
                        if (ulRightPanel.getElementsByTagName('iframe')[count] != null && ulRightPanel.getElementsByTagName('iframe')[count] != "undefined") {
                            if (ulRightPanel.getElementsByTagName('iframe')[count].id == iFrameId) {
                                return '0';
                            }
                        }
                    }
                }
            }
        }
    }
    __parentDocument = null;
    return '1';
}

var iFrameVisible = false;
var modalWindow = null;
var opaqueDiv = document.getElementById("divOpaque");
if (opaqueDiv == null) {
    opaqueDiv = window.parent.window.document.getElementById("divOpaque");
    window.parent.window.visible = false;
}

var opaqueDiv2 = document.getElementById("divOpaque2");
if (opaqueDiv2 == null) {
    opaqueDiv2 = window.parent.window.document.getElementById("divOpaque2");
}

function ToggleModalWindow(windowContainer, type, show) {
    if (document.getElementById("divImageGalleryAccount") != null)
        windowContainer = "divImageGalleryAccount";
    var counter4Enter = 2;
    if (1 == type) {
        iFrameVisible = true;
    }
    if (null == modalWindow) {
        counter4Enter = 1;
        modalWindow = document.getElementById(windowContainer);
    }
    else if (modalWindow.id != windowContainer) {
        counter4Enter = 1;
        modalWindow = document.getElementById(windowContainer);
    }
    var ddlElements = document.getElementsByTagName("select");
    if (show) {
        if (null == window.onscroll && null == window.onresize)
            window.onscroll = window.onresize = function () {
                ToggleModalWindow(windowContainer, type, true);
            };
        if (iFrameVisible) {
            if (navigator.userAgent.indexOf("MSIE 6.0") != -1) {
                for (var counter = 0; counter < ddlElements.length; counter++) {
                    ddlElements[counter].style.display = "none";
                }
            }
        }
        if (!modalWindow) {
            return;
        }
        var browserDimensions = GetBrowserDimensions();
        var browserScroll = GetBrowserScroll();
        var modalWindowWidth = modalWindow.clientWidth;
        var modalWindowHeight = modalWindow.clientHeight;

        if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)) {
            modalWindow.style.left = parseInt(((browserDimensions.Width - modalWindowWidth) / 2) + browserScroll.Left) + "px";
        }
        else {
            modalWindow.style.left = parseInt(((browserDimensions.Width - modalWindowWidth) / 2) + browserScroll.Left - 12) + "px";
        }
        // modalWindow.style.top = parseInt(((browserDimensions.Height - modalWindowHeight) / 2) + browserScroll.Top) + "px";
        if (parseInt((browserDimensions.Height - modalWindowHeight) / 2) > 0) {
            modalWindow.style.top = parseInt(((browserDimensions.Height - modalWindowHeight) / 2) + browserScroll.Top) + "px";
        } else {
            if (counter4Enter == 1) {
                modalWindow.style.top = parseInt(browserScroll.Top) + "px";
            }
        }
        modalWindow.style.display = "";

        var divOpaqueFromPopup = document.getElementById("divOpaqueFromPopup");

        if (!divOpaqueFromPopup) {
            opaqueDiv.style.width = browserDimensions.Width + "px";
            opaqueDiv.style.height = browserDimensions.Height + "px";
            opaqueDiv.style.top = browserScroll.Top + "px";
            opaqueDiv.style.left = browserScroll.Left + "px";
            opaqueDiv.style.display = "";
        }
        else {
            opaqueDiv = window.parent.window.document.getElementById("divOpaque");
            opaqueDiv2 = window.parent.window.document.getElementById("divOpaque2");

            if (screen.width > 1024) {
                divOpaqueFromPopup.style.width = (browserDimensions.Width - 30) + "px";
            }
            else {
                divOpaqueFromPopup.style.width = browserDimensions.Width + "px";
            }
            divOpaqueFromPopup.style.height = browserDimensions.Height + "px";
            divOpaqueFromPopup.style.top = browserScroll.Top + "px";
            divOpaqueFromPopup.style.left = browserScroll.Left + "px";
            divOpaqueFromPopup.style.display = "";

            opaqueDiv2.style.width = opaqueDiv.style.width;
            opaqueDiv2.style.height = opaqueDiv.style.height;
            opaqueDiv2.style.top = opaqueDiv.style.top;
            opaqueDiv2.style.left = opaqueDiv.style.left;
            opaqueDiv2.style.display = "";
        }
    } else {
        if (1 == type) {
            iFrameVisible = false; //modalWindow.src = "";
        }
        var divOpaqueFromPopup = document.getElementById("divOpaqueFromPopup");;
        if (!iFrameVisible) {
            window.onscroll = window.onresize = null;
            if (divOpaqueFromPopup) {
                divOpaqueFromPopup.style.display = "none";
                opaqueDiv2.style.display = "none";
            }
            else {
                opaqueDiv.style.display = "none";
            }
            if (navigator.userAgent.indexOf("MSIE 6.0") != -1) for (var counter = 0; counter < ddlElements.length; counter++) ddlElements[counter].style.display = "";
        }
        if (modalWindow) {
            modalWindow.style.display = "none";
            modalWindow.style.left = "-10000px";
            modalWindow.style.top = "-10000px";
        }

        if (1 == type) {
            modalWindow.style.width = "1px";
            modalWindow.style.height = "1px";
        }
        if (modalWindow)
            modalWindow.style.display = "";
    }
}

function ToggleModal(windowContainer, type, show) {
    if (1 == type) iFrameVisible = true;
    if (null == modalWindow) modalWindow = document.getElementById(windowContainer);
    else if (modalWindow.id != windowContainer) modalWindow = document.getElementById(windowContainer);
    var ddlElements = document.getElementsByTagName("select");
    if (show) {
        document.body.scroll = "no";
        if (iFrameVisible) {
            if (navigator.userAgent.indexOf("MSIE 6.0") != -1) for (var counter = 0; counter < ddlElements.length; counter++) ddlElements[counter].style.display = "none";
        }
        var browserDimensions = GetBrowserDimensions();
        var browserScroll = GetBrowserScroll();
        var modalWindowWidth = modalWindow.clientWidth;
        var modalWindowHeight = modalWindow.clientHeight;
        modalWindow.style.display = "none";
        if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)) {
            modalWindow.style.left = parseInt(((browserDimensions.Width - modalWindowWidth) / 2) + browserScroll.Left) + "px";
        }
        else {
            modalWindow.style.left = parseInt(((browserDimensions.Width - modalWindowWidth) / 2) + browserScroll.Left - 12) + "px";
        }
        modalWindow.style.top = parseInt(((browserDimensions.Height - modalWindowHeight) / 2) + browserScroll.Top) + "px";
        opaqueDiv.style.width = browserDimensions.Width + "px";
        opaqueDiv.style.height = browserDimensions.Height + "px";
        opaqueDiv.style.top = browserScroll.Top + "px";
        opaqueDiv.style.left = browserScroll.Left + "px";
        opaqueDiv.style.display = modalWindow.style.display = "";

    } else {
        document.body.scroll = "";
        if (1 == type) {
            iFrameVisible = false; //modalWindow.src = "";
        }
        if (!iFrameVisible) {
            opaqueDiv.style.display = "none";
            if (navigator.userAgent.indexOf("MSIE 6.0") != -1) for (var counter = 0; counter < ddlElements.length; counter++) ddlElements[counter].style.display = "";
        }
        modalWindow.style.display = "none";
        modalWindow.style.left = "-10000px";
        modalWindow.style.top = "-10000px";

        if (1 == type) {
            modalWindow.style.width = "1px";
            modalWindow.style.height = "1px";
        }
        modalWindow.style.display = "";
    }
}

function CloseWindow(iFrameId) {
    window.parent.window.ToggleModal(iFrameId, 1, false);
}

function SetFocus() {
    var focusElement = null;
    for (var counter = 0; counter < __focusIdsArray.length; counter++) {
        try {
            focusElement = document.getElementById(__focusIdsArray[counter]);
            if (null != focusElement) {
                focusElement.focus();
                focusElement.select();
            }
        } catch (e) { }
    }
}
function ShowError() {
    alert(__errorMessage);
    __endRequestHandlerArray = [];
}

function OpenDmarcSupportWindow(baseUrl) {
    if (!baseUrl) {
        baseUrl = '..';
    } else if (!/\/$/.test(baseUrl)) {
        baseUrl += '/';
    }

    PopupCenter(baseUrl + 'dmarc.anp/support', 'SupportArticle', 850, 685);
    return false;
}

function PopupCenter(url, title, w, h) {
    // Fixes dual-screen position                         Most browsers      Firefox
    var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
    var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;

    var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
    var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

    var left = ((width / 2) - (w / 2)) + dualScreenLeft;
    var top = ((height / 2) - (h / 2)) + dualScreenTop;
    var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);

    // Puts focus on the newWindow
    if (window.focus) {
        newWindow.focus();
    }
}

// Following is a fix about the "__flash__removeCallback" error.
if ((navigator.userAgent.toLowerCase().indexOf('msie') != -1) && (navigator.userAgent.toLowerCase().indexOf('opera') == -1)) {
    window.attachEvent('onunload', function () { window['__flash__removeCallback'] = function (instance, name) { try { if (instance) { instance[name] = null; } } catch (flashEx) { } }; });
}

/*** Following is the fix for IE 6 - 7 Activation Issue for Flash objects ***/
function activateFlashObjects() {
    theObjects = document.getElementsByTagName("object");
    for (var i = 0; i < theObjects.length; i++) {
        theObjects[i].outerHTML = theObjects[i].outerHTML;
    }
    theObjects = document.getElementsByTagName("embed");
    for (var i = 0; i < theObjects.length; i++) {
        theObjects[i].outerHTML = theObjects[i].outerHTML;
    }
    theObjects = null;
}//Related to Firefox for working of panel's defaultbutton in multiline textbox
function WebForm_FireDefaultButton(event, target) {
    var element = event.target || event.srcElement;
    if (event.keyCode == 13 &&
        !(element &&
        element.tagName.toLowerCase() == "textarea")) {
        var defaultButton;
        if (__nonMSDOMBrowser) {
            defaultButton = document.getElementById(target);
        }
        else {
            defaultButton = document.all[target];
        }
        if (defaultButton && typeof defaultButton.click != "undefined") {
            defaultButton.click();
            event.cancelBubble = true;
            if (event.stopPropagation) {
                event.stopPropagation();
            }
            return false;
        }
    }
    return true;
}

function displayProperties(obj) {
    var str = "";
    var prop;
    if (typeof (obj.length) != "undefined" && typeof (obj[0]) != "undefined") {
        for (prop = 0; prop < obj.length; prop++) {
            str += "\n" + prop + "=" + obj[prop];
        }
    }
    else {
        for (prop in obj) {
            try {
                str += "\n" + prop + "=" + eval("obj." + prop);
            } catch (e) { }
        }
    }
    alert(str);
}

function displayPropertiesExpHTML(obj) {
    var str = "";
    var prop;
    if (typeof (obj.length) != "undefined" && typeof (obj[0]) != "undefined") {
        for (prop = 0; prop < obj.length; prop++) {
            str += "\n" + prop + "=" + obj[prop];
        }
    }
    else {
        for (prop in obj) {
            if ((prop == "innerHTML") || (prop == "outerHTML") || (prop == "innerText") || (prop == "outerText")) continue;
            try {
                str += "\n" + prop + "=" + eval("obj." + prop);
            } catch (e) { }
        }
    }
    alert(str);
}
function delay(timeInMilliS) {
    var date = new Date();
    var curDate = null;
    do { curDate = new Date(); }
    while (curDate - date < timeInMilliS);
}



// Javascript moved from image-gallery.js



// Flash Player Version Detection - Rev 1.6
// Detect Client Browser type
// Copyright(c) 2005-2006 Adobe Macromedia Software, LLC. All rights reserved.
var isIE = (navigator.appVersion.indexOf("MSIE") != -1) ? true : false;
var isWin = (navigator.appVersion.toLowerCase().indexOf("win") != -1) ? true : false;
var isOpera = (navigator.userAgent.indexOf("Opera") != -1) ? true : false;
// -----------------------------------------------------------------------------
// Major version of Flash required
var requiredMajorVersion = 9;
// Minor version of Flash required
var requiredMinorVersion = 0;
// Minor version of Flash required
var requiredRevision = 28;
// -----------------------------------------------------------------------------
function ControlVersion() {
    var version;
    var axo;
    var e;

    // NOTE : new ActiveXObject(strFoo) throws an exception if strFoo isn't in the registry

    try {
        // version will be set for 7.X or greater players
        axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");
        version = axo.GetVariable("$version");
    } catch (e) {
    }

    if (!version) {
        try {
            // version will be set for 6.X players only
            axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");

            // installed player is some revision of 6.0
            // GetVariable("$version") crashes for versions 6.0.22 through 6.0.29,
            // so we have to be careful. 

            // default to the first public version
            version = "WIN 6,0,21,0";

            // throws if AllowScripAccess does not exist (introduced in 6.0r47)		
            axo.AllowScriptAccess = "always";

            // safe to call for 6.0r47 or greater
            version = axo.GetVariable("$version");

        } catch (e) {
        }
    }

    if (!version) {
        try {
            // version will be set for 4.X or 5.X player
            axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
            version = axo.GetVariable("$version");
        } catch (e) {
        }
    }

    if (!version) {
        try {
            // version will be set for 3.X player
            axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
            version = "WIN 3,0,18,0";
        } catch (e) {
        }
    }

    if (!version) {
        try {
            // version will be set for 2.X player
            axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
            version = "WIN 2,0,0,11";
        } catch (e) {
            version = -1;
        }
    }

    return version;
}

// JavaScript helper required to detect Flash Player PlugIn version information
function GetSwfVer() {
    // NS/Opera version >= 3 check for Flash plugin in plugin array
    var flashVer = -1;

    if (navigator.plugins != null && navigator.plugins.length > 0) {
        if (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]) {
            var swVer2 = navigator.plugins["Shockwave Flash 2.0"] ? " 2.0" : "";
            var flashDescription = navigator.plugins["Shockwave Flash" + swVer2].description;
            var descArray = flashDescription.split(" ");
            var tempArrayMajor = descArray[2].split(".");
            var versionMajor = tempArrayMajor[0];
            var versionMinor = tempArrayMajor[1];
            var versionRevision = descArray[3];
            if (versionRevision == "") {
                versionRevision = descArray[4];
            }
            if (versionRevision[0] == "d") {
                versionRevision = versionRevision.substring(1);
            } else if (versionRevision[0] == "r") {
                versionRevision = versionRevision.substring(1);
                if (versionRevision.indexOf("d") > 0) {
                    versionRevision = versionRevision.substring(0, versionRevision.indexOf("d"));
                }
            } else if (versionRevision[0] == "b") {
                versionRevision = versionRevision.substring(1);
            }
            var flashVer = versionMajor + "." + versionMinor + "." + versionRevision;
        }
    }
        // MSN/WebTV 2.6 supports Flash 4
    else if (navigator.userAgent.toLowerCase().indexOf("webtv/2.6") != -1) flashVer = 4;
        // WebTV 2.5 supports Flash 3
    else if (navigator.userAgent.toLowerCase().indexOf("webtv/2.5") != -1) flashVer = 3;
        // older WebTV supports Flash 2
    else if (navigator.userAgent.toLowerCase().indexOf("webtv") != -1) flashVer = 2;
    else if (isIE && isWin && !isOpera) {
        flashVer = ControlVersion();
    }
    return flashVer;
}

// When called with reqMajorVer, reqMinorVer, reqRevision returns true if that version or greater is available
function DetectFlashVer(reqMajorVer, reqMinorVer, reqRevision) {
    versionStr = GetSwfVer();
    if (versionStr == -1) {
        return false;
    } else if (versionStr != 0) {
        if (isIE && isWin && !isOpera) {
            // Given "WIN 2,0,0,11"
            tempArray = versionStr.split(" "); 	// ["WIN", "2,0,0,11"]
            tempString = tempArray[1];			// "2,0,0,11"
            versionArray = tempString.split(",");	// ['2', '0', '0', '11']
        } else {
            versionArray = versionStr.split(".");
        }
        var versionMajor = versionArray[0];
        var versionMinor = versionArray[1];
        var versionRevision = versionArray[2];

        // is the major.revision >= requested major.revision AND the minor version >= requested minor
        if (versionMajor > parseFloat(reqMajorVer)) {
            return true;
        } else if (versionMajor == parseFloat(reqMajorVer)) {
            if (versionMinor > parseFloat(reqMinorVer))
                return true;
            else if (versionMinor == parseFloat(reqMinorVer)) {
                if (versionRevision >= parseFloat(reqRevision))
                    return true;
            }
        }
        return false;
    }
}

function AC_AddExtension(src, ext) {
    var qIndex = src.indexOf('?');
    if (qIndex != -1) {
        // Add the extention (if needed) before the query params
        var path = src.substring(0, qIndex);
        if (path.length >= ext.length && path.lastIndexOf(ext) == (path.length - ext.length))
            return src;
        else
            return src.replace(/\?/, ext + '?');
    }
    else {
        // Add the extension (if needed) to the end of the URL
        if (src.length >= ext.length && src.lastIndexOf(ext) == (src.length - ext.length))
            return src;  // Already have extension
        else
            return src + ext;
    }
}

function AC_Generateobj(objAttrs, params, embedAttrs) {
    var str = '';
    if (isIE && isWin && !isOpera) {
        str += '<object ';
        for (var i in objAttrs)
            str += i + '="' + objAttrs[i] + '" ';
        str += '>';
        for (var i in params)
            str += '<param name="' + i + '" value="' + params[i] + '" /> ';
        str += '</object>';
    } else {
        str += '<embed ';
        for (var i in embedAttrs)
            str += i + '="' + embedAttrs[i] + '" ';
        str += '> </embed>';
    }

    document.write(str);
}

function AC_FL_RunContent() {
    var ret =
      AC_GetArgs
      (arguments, ".swf", "movie", "clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
       , "application/x-shockwave-flash"
      );
    AC_Generateobj(ret.objAttrs, ret.params, ret.embedAttrs);
}

function AC_GetArgs(args, ext, srcParamName, classid, mimeType) {
    var ret = new Object();
    ret.embedAttrs = new Object();
    ret.params = new Object();
    ret.objAttrs = new Object();
    for (var i = 0; i < args.length; i = i + 2) {
        var currArg = args[i].toLowerCase();

        switch (currArg) {
            case "classid":
                break;
            case "pluginspage":
                ret.embedAttrs[args[i]] = args[i + 1];
                break;
            case "src":
            case "movie":
                args[i + 1] = AC_AddExtension(args[i + 1], ext);
                ret.embedAttrs["src"] = args[i + 1];
                ret.params[srcParamName] = args[i + 1];
                break;
            case "onafterupdate":
            case "onbeforeupdate":
            case "onblur":
            case "oncellchange":
            case "onclick":
            case "ondblClick":
            case "ondrag":
            case "ondragend":
            case "ondragenter":
            case "ondragleave":
            case "ondragover":
            case "ondrop":
            case "onfinish":
            case "onfocus":
            case "onhelp":
            case "onmousedown":
            case "onmouseup":
            case "onmouseover":
            case "onmousemove":
            case "onmouseout":
            case "onkeypress":
            case "onkeydown":
            case "onkeyup":
            case "onload":
            case "onlosecapture":
            case "onpropertychange":
            case "onreadystatechange":
            case "onrowsdelete":
            case "onrowenter":
            case "onrowexit":
            case "onrowsinserted":
            case "onstart":
            case "onscroll":
            case "onbeforeeditfocus":
            case "onactivate":
            case "onbeforedeactivate":
            case "ondeactivate":
            case "type":
            case "codebase":
                ret.objAttrs[args[i]] = args[i + 1];
                break;
            case "id":
            case "width":
            case "height":
            case "align":
            case "vspace":
            case "hspace":
            case "class":
            case "title":
            case "accesskey":
            case "name":
            case "tabindex":
                ret.embedAttrs[args[i]] = ret.objAttrs[args[i]] = args[i + 1];
                break;
            default:
                ret.embedAttrs[args[i]] = ret.params[args[i]] = args[i + 1];
        }
    }
    ret.objAttrs["classid"] = classid;
    if (mimeType) ret.embedAttrs["type"] = mimeType;
    return ret;
}

function methodFromFlex(ImageUrl, SereverPath, physicalLocation, ImageName, ImageWidth, ImageHeight, GalleryItemId, GalleryItemType) {

    var FinalImageUrl;
    var DecodedPhysicalPath;

    DecodedPhysicalLocation = unescape(physicalLocation);
    DecodedPhysicalLocation = DecodedPhysicalLocation.replace('\\', '/');
    FinalImageUrl = SereverPath + "/" + DecodedPhysicalLocation + "/" + ImageName;

    PasteImageUrl(FinalImageUrl, ImageWidth, ImageHeight, GalleryItemId, GalleryItemType);

    return "successful";
}

if (typeof (Sys) != "undefined") {
    if (Sys && Sys.Application) {
        Sys.Application.notifyScriptLoaded();
    }
}

// Javascript moved from content-anp-modules.js

function ParameterInserted(ddlParameters, ckId, aspCkId) {
    if (ddlParameters.value != _parameterTag) {
        var ckEditor = CKEDITOR.instances[ckId];
        ckEditor = (typeof (ckEditor) === 'undefined') ? CKEDITOR.instances[ckId + "_" + aspCkId] : ckEditor;
        if (typeof (ckEditor) !== 'undefined') {
            ckEditor.insertHtml(" ##" + ddlParameters.value + "## ");
        }
    }
}
function ParameterInsertedForLight(ddlParameters, txtP) {
    if (ddlParameters.value != _parameterTag) {
        document.getElementById(txtP).value += " ##" + ddlParameters.value + "##";
    }
}
function LinkArticleInserted(ddlArticle, _txtLinkURL) {
    if (ddlArticle.selectedIndex != 0) {
        var txtLinkURL = document.getElementById(_txtLinkURL);
        if (typeof (txtLinkURL) != "undefined") {
            txtLinkURL.value = _linkArticleTag + ddlArticle.value;
        }
    }

}
//if(typeof(Sys)!="undefined")
//{
//    if( Sys && Sys.Application ){
//       Sys.Application.notifyScriptLoaded();
//        }
//}

// Javascript moved from report.js

function checkListValue(ddlFromClientID, ddlToClientID) {
    var ddlFrom = document.getElementById(ddlFromClientID);
    var ddlInto = document.getElementById(ddlToClientID);
    if (ddlFrom.value == '') {
        alert(_reportValidationMessageFrom);
        return false;
    }
    if (ddlInto.value == '') {
        alert(_reportValidationMessageTo);
        return false;
    }
}
function toggleBox(id) {
    var oExpand = document.getElementById('expand_' + id);
    Effect.toggle(oExpand, 'blind', {});
}
//merge comment

//gets url parameters
function GetUrlParameter(name, isPopup) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]").toLowerCase();
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results;
    if (!isPopup) {
        results = regex.exec(window.location.href.toLowerCase());
    }
    else {
        results = regex.exec(window.parent.location.href.toLowerCase());
    }
    if (results == null)
        return "";
    else
        return results[1];
}

function toggleBoxLink(id) {
    var oExpand = 'div[id=expand_' + id + ']';
    $(oExpand).toggle();
}

function get(url) {
    var rand = Math.random();
    jQuery.get(url + '&r=' + rand, '', function (newitems) {
        jQuery("head").append(newitems);
    });
}

function ImpersonateUser(accID, url, type) {
    jQuery.post(GetLightAccountHandler, { AccountID: accID, Type: type }, function (data) { if (eval(data).Success = true) { window.location.href = url; } }, "json")
}

function startNewSendTabOverlay() {
    startNewSendTabOverlayWithBaseUrl('..');
}

function startNewSendTabOverlayWithBaseUrl(baseUrl) {
    if (window.SendTabOverlayActionUrl != undefined && window.SendTabOverlayActionUrl != '') {
        window.location = window.SendTabOverlayActionUrl;
        return;
    }
    if (jQuery('.image-gallery-modal').length) { jQuery('.image-gallery-modal').remove(); }
    startOverlayWithBaseUrl("NewSendTab", "NewSendTab", baseUrl, function () {
        jQuery("#divOverlayContainer").load(baseUrl + "/home2/controls/overlay/NewSendTabOverlay.aspx .overlay1", {}, function (response, status, xhr) {
            if (response.match("hdnLogin") != null) {
                top.location = baseUrl + "/Login.aspx";
            }
            resizeOverlay();
        });
    });
}

function startOverlay(type, item, loadFunction) {
    startOverlayWithBaseUrl(type, item, '..', loadFunction);
}

function startOverlayWithBaseUrl(type, item, baseUrl, loadFunction) {
    jQuery("html").css('overflow', 'hidden');
    jQuery("body").append('<div class="overlay" ></div><div id="divOverlayContainer" class="overlaycontainer"><div><img src="' + baseUrl + '/App_Themes/DarkGreen_New/img/loader.gif"></div></div>')
        .css({ "margin-right": "15px" });

    jQuery(".overlay").css("top", jQuery(window).scrollTop());
    jQuery(".overlay").first().animate({ "opacity": "0.6" }, 400, "linear", function () {
        resizeOverlay();
        loadFunction(type, item);
    });
}


function removeOverlay() {
    jQuery("html").css('overflow', '');
    jQuery("body").css({ "margin-right": "0" });
    jQuery(".overlay, .overlaycontainer").animate({ "opacity": "0" }, 200, "linear", function () {
        jQuery(".overlay, .overlaycontainer").remove();
    });
}

function resizeOverlay() {
    var divWidth = jQuery("#divOverlayContainer div").width();
    var divHeight = jQuery("#divOverlayContainer div").height();

    var scrollTop = jQuery(window).scrollTop();
    var windowHeight = jQuery(window).height();
    var top = (windowHeight / 2) + scrollTop;

    jQuery("#divOverlayContainer")
			.css({
			    "top": top,
			    "left": "50%",
			    "width": divWidth,
			    "height": divHeight,
			    "margin-top": -(divHeight / 2),
			    "margin-left": -(divWidth / 2)

			})
			.animate({ "opacity": "1" }, 400, "linear");
}
