import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { AudioComponent } from './audio/audio.component';
import { ChatbotComponent } from './chatbot/chatbot.component';
import { CookieService } from 'ngx-cookie-service';
import { enableProdMode } from '@angular/core';
import { FileSaverModule } from 'ngx-filesaver';
import { FormsModule } from '@angular/forms';
import { HttpClientModule,HttpClientXsrfModule } from '@angular/common/http';
import { NgScrollbarModule } from 'ngx-scrollbar';

enableProdMode();

@NgModule({
  declarations: [
    AppComponent,
    ChatbotComponent,
    AudioComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    FileSaverModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'prep_answers',
      headerName: 'Set-Cookie',
    }),
    NgScrollbarModule
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})

export class AppModule { }
