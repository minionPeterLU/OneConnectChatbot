var data=[];
var WelcomeMsg = "Hi, I am OneConnectChatBot!. How can I help you?";


function addBr(text){
    
    console.log("addBr");
    console.log(text);

    return text.replace(/\n/g, "<br />");

}


$(window).load(function () {
    showBotMessages(null);
});

var Message;

Message = function (arg) {

    this.text = arg.text, 
    this.buttons = arg.buttons,
    this.message_side = arg.message_side,
    this.image = arg.image,
    this.element = arg.element,
    this.attachment = arg.attachment;


    this.draw = function (_this) {

        var content;
        var type;

        console.log("_this");
        console.log(_this);

        if (_this.text !== null){
            type = ".text";
            content = _this.text;
        }else if (_this.image !== null){
            type = ".image";
            content = _this.image;
        }else if (_this.buttons.length >= 1 && _this.buttons !== undefined){
            type = ".buttons";
            content = _this.buttons;
        }else if (_this.element.length >= 1 && _this.element !== undefined){
            type = ".element";
            content = _this.element;
        }else if (_this.attachment.length >= 1 && _this.attachment !== undefined){
            type = ".attachment";
            content = _this.attachment;
        }

        console.log("content");
        console.log(content);

        return function () {
            var $message;
            $message = $($('.message_template').clone().html());

            if(type === ".text"){
                $message.addClass(_this.message_side).find('.text').html(addBr(content));
            }else{

                $message.addClass(_this.message_side).find('.img').html(content);
            }

            $('.messages').append($message);
            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
};

function showBotMessages(msgs){

    if(msgs=== null || msgs === undefined){
        showBotMessage(null);
    }else{
        msgs.forEach(function(e) {
            showBotMessage(e);
        });
    }

}

function showBotMessage(msg){

    $messages = $('.messages');
    var text = null;
    var image = null;
    var buttons = [];
    var element = [];
    var attachment = [];

    console.log("======msg======");
    console.log(msg);
    

    if(msg === null){
   
        message = new Message({
            text: WelcomeMsg,
            image: image,
            buttons: buttons,
            element: element ,
            attachment: attachment,
            message_side: 'left'
        });

    }else{
        

        console.log("image");
        console.log(msg.image);

        if (msg.text !== null && msg.text !== undefined){
            text = msg.text;
        }else if(msg.image !== null && msg.image !== undefined){

  

            image = new Image();
            image.src = msg.image;
            
        }else if(msg.buttons !== null && msg.buttons !== undefined){
            buttons = msg.buttons;
        }else if(msg.element !== null && msg.element !== undefined){
            element = msg.element;
        }else if (msg.attachment !== null && msg.attachment !== undefined){
            attachment = msg.attachment;
        }
        


        message = new Message({
            text: text,
            image: image,
            buttons: buttons,
            element: element ,
            attachment: attachment,
            message_side: 'left'
        });
    }

    message.draw();
    
    $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
}

function showUserMessage(msg){
    $messages = $('.messages');
    message = new Message({
        text: msg,
        message_side: 'right'
    });
    message.draw();
    $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
    $('#msg_input').val('');
}


function sayToBot(text){
    document.getElementById("msg_input").placeholder = "Type your messages here..."
    $.post("/chat",
        {
            //csrfmiddlewaretoken:csrf,
            text:text,
        },
        function(jsondata, status){
            if(jsondata["status"]=="success"){
                response=jsondata["response"];

                if(response){showBotMessages(response);}
            }
    });
}

getMessageText = function () {
    var $message_input;
    $message_input = $('.message_input');
    return $message_input.val();
};

$("#say").keypress(function(e) {
    if(e.which == 13) {
        $("#saybtn").click();
    }
});

$('.send_message').click(function (e) {
        msg = getMessageText();
        if(msg){
        showUserMessage(msg);
        sayToBot(msg);
    $('.message_input').val('');}
});

$('.message_input').keyup(function (e) {
    if (e.which === 13) {
        msg = getMessageText();
        if(msg){
        showUserMessage(msg);
        sayToBot(msg);
    $('.message_input').val('') ;}
    }
});