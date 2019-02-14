import { Component, OnInit } from '@angular/core';
import * as RecordRTC from 'recordrtc';
import { DomSanitizer } from '@angular/platform-browser';
import { FileSaverService } from 'ngx-filesaver';
import { HttpClient } from '@angular/common/http';


@Component({
	selector: 'app-audio',
	templateUrl: './audio.component.html',
	styleUrls: ['./audio.component.css']
})

export class AudioComponent implements OnInit {

		//Lets initiate Record OBJ
		private record;
		//Will use this flag for detect recording
		private recording = false;
		//Url of Blob
		private url;
		private error;
    public audio = `{ "audio": "This is audio file!中文" }`;
	constructor(private domSanitizer: DomSanitizer,private _httpClient: HttpClient, private _FileSaverService: FileSaverService) { }

	ngOnInit() {
	}

  onDown(type: string, fromRemote: boolean) {
    const fileName = `save.${type}`;
    if (fromRemote) {
      this._httpClient.get(`assets/files/audio.${type}`, {
        observe: 'response',
        responseType: 'blob'
      }).subscribe(res => {
        this._FileSaverService.save(res.body, fileName);
      });
      return;
    }
    const fileType = this._FileSaverService.genType(fileName);
    const txtBlob = new Blob([this.audio], { type: fileType });
    this._FileSaverService.save(txtBlob, fileName);
  }

	sanitize(url:string){
			return this.domSanitizer.bypassSecurityTrustUrl(url);
	}
	/**
	 * Start recording.
	 */
	initiateRecording() {
    this.recording = true;
    let mediaConstraints = {
        video: false,
        audio: true
    };

    navigator.mediaDevices.getUserMedia(mediaConstraints)
      .then(this.successCallback.bind(this), this.errorCallback.bind(this));

    setTimeout (() => {
      this.stopRecording();
    }, 10100);
	}
	/**
	 * Will be called automatically.
	 */
	successCallback(stream) {
    var options = {
        mimeType: "audio/wav",
        numberOfAudioChannels: 1
    };
    //Start Actuall Recording
    var StereoAudioRecorder = RecordRTC.StereoAudioRecorder;
    this.record = new StereoAudioRecorder(stream, options);
    this.record.record();
  }

	/**
	 * Stop recording.
	 */
	stopRecording() {
			this.recording = false;
			this.record.stop(this.processRecording.bind(this));
	}
	/**
	 * processRecording Do what ever you want with blob
	 * @param  {any} blob Blog
	 */
	processRecording(blob) {
    this.url = URL.createObjectURL(blob);

    this.onDown('wma', true);

	}
	/**
	 * Process Error.
	 */
	errorCallback(error) {
			this.error = 'Can not play audio in your browser';
	}
}
