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

		this.chat.getData("welcome_msg").subscribe(data => {

      this.welcomeMsg = data["response"];

			const botMessage = new Message("text",this.welcomeMsg,'bot');
			this.chat.update(botMessage);

			console.log(this.welcomeMsg);

		} );

	}

	sendMessage(){


		this.sendMsg = {"status":"success","request":this.messageInput};

		console.log(this.messageInput);

		const userMessage = new Message("text",this.messageInput,'user');
		this.chat.update(userMessage);
		this.messageInput = "";

		this.chat.postData("chat",this.sendMsg).subscribe(data => {

			this.responseMsgList = data["response"];


			for(let i = 0;i < this.responseMsgList.length; i++){

				var value : any = this.responseMsgList[i];

				var content: any;
				var type : string;

				if(value.text != null){
					content = value["text"];
					type = "text";
				}else if(value.image != null){
          content = new Image();
          content.src = value["image"];
          content = "<img src="+content.src+'>';
					type = "img";
				}

				const botMessage = new Message(type,content,'bot');
				this.chat.update(botMessage);

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
