import { Component, OnInit } from '@angular/core';
import { OneconnectchatbotService, Message } from '../oneconnectchatbot.service';
import { Observable } from 'rxjs';
import { scan } from 'rxjs/operators';
// import 'rxjs/add/operator/scan';

@Component({
	selector: 'app-chatbot',
	templateUrl: './chatbot.component.html',
	styleUrls: ['./chatbot.component.css'],
  providers: [OneconnectchatbotService]
})

export class ChatbotComponent implements OnInit {

	welcomeMsg;
	messageInput : string = '';
	responseMsg;
	responseMsgList;
	sendMsg: any;
	messages: Observable<Message[]>;


	constructor(private chat:OneconnectchatbotService) { }

	getMessage(){

		// this.chat.getData("welcome_msg").subscribe(data => {

    //   this.welcomeMsg = data["response"];

		// 	const botMessage = new Message("text",this.welcomeMsg,'bot');
		// 	this.chat.update(botMessage);

		// 	console.log(this.welcomeMsg);

    // } );
    var content = [];
    var welcomeMsg = "Hi, I am OneConnectChatBot!. How can I help you?";
    content.push(welcomeMsg);
    const botMessage = new Message("text",content,'bot');
    this.chat.update(botMessage);
    console.log(welcomeMsg);
	}

	sendMessage(element : any){


    var content = [];
    console.log(element);

    if(element != null){
      console.log("===========element===========");
      console.log(element);
      content.push(element);
      this.sendMsg = {"status":"success","request":element};
    }else{
      content.push(this.messageInput);
      console.log("===========messageInput===========");
      console.log(this.messageInput);
      this.sendMsg = {"status":"success","request":this.messageInput};
    }

		const userMessage = new Message("text",content,'user');
		this.chat.update(userMessage);
		this.messageInput = "";

		this.chat.postData("chat",this.sendMsg).subscribe(data => {

			this.responseMsgList = data["response"];


			for(let i = 0;i < this.responseMsgList.length; i++){

				var value : any = this.responseMsgList[i];

				var content : any = [];
				var type : string;

				if(value.text != null){
					content.push(value["text"]);
					type = "text";
				}else if(value.image != null){

          var image = new Image();
          image.src = value["image"];
          var imageElement = "<img src="+image.src+'>';
          type = "img";
          content.push(imageElement);

				}else if(value.buttons != null){

          content = value["buttons"];
          type = "button";

          console.log("==============content==============");
          console.log(content);

				}

				const botMessage = new Message(type,content,'bot');
				this.chat.update(botMessage);

        console.log("===========Value============")
        console.log(value);

			}


		});
	}


	// Initate
	ngOnInit() {

		// refreash the page
		this.getMessage();

		// appends to array after each new message is added to feedSource
		this.messages = this.chat.conversation.asObservable()
		.pipe(scan((acc, val) => acc.concat(val)) );

	}


}
