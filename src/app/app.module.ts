import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { ChatbotComponent } from './chatbot/chatbot.component';
import { FileSaverModule } from 'ngx-filesaver';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { enableProdMode } from '@angular/core';
import { AudioComponent } from './audio/audio.component';

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
    HttpClientModule,
    FormsModule,
    FileSaverModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule { }
