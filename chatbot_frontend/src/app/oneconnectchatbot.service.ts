import { BehaviorSubject } from 'rxjs';
import { bypassSanitizationTrustResourceUrl } from '@angular/core/src/sanitization/bypass';
import { CookieService } from 'ngx-cookie-service';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';


export class Message {
  constructor(public type:string, public content=[], public sentBy: string) {}
}

@Injectable({
  providedIn: 'root'
})

export class OneconnectchatbotService {

  cookieValue = 'UNKNOWN';
  conversation = new BehaviorSubject<Message[]>([]);

  constructor(private http:HttpClient,private cookieService: CookieService) {

  };

  private baseUrl = "http://127.0.0.1:8080/";

  getData(url:string){
    return this.http.get(this.baseUrl+url,{ withCredentials: true});
  }

  postData(url:string, item:any){
    return this.http.post(this.baseUrl+url, item);
  }

  // Adds message to source
  update(msg: Message) {
    this.conversation.next([msg]);
  }

}
