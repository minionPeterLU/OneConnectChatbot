import { TestBed } from '@angular/core/testing';

import { OneconnectchatbotService } from './oneconnectchatbot.service';

describe('OneconnectchatbotService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: OneconnectchatbotService = TestBed.get(OneconnectchatbotService);
    expect(service).toBeTruthy();
  });
});
