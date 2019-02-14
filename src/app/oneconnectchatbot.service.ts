import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';
import { bypassSanitizationTrustResourceUrl } from '@angular/core/src/sanitization/bypass';

export class Message {
  constructor(public type:string, public content: any, public sentBy: string) {}
}

@Injectable({
  providedIn: 'root'
})

export class OneconnectchatbotService {

  conversation = new BehaviorSubject<Message[]>([]);

  constructor(private http:HttpClient) {

  };

  private baseUrl = "http://127.0.0.1:8080/";

  getData(url:string){
    return this.http.get(this.baseUrl+url);
  }

  postData(url:string, item:any){
    return this.http.post(this.baseUrl+url, item);
  }

  // Adds message to source
  update(msg: Message) {
    this.conversation.next([msg]);
  }

}
