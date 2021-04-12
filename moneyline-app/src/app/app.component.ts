import { Component } from '@angular/core';
import { IconService } from './icon.service';
import { MatchupService } from './matchup.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'moneyline-app';
  constructor(
    private iconService: IconService,
    private matchupService : MatchupService
  ){
    this.iconService.registerIcons();
    this.matchupService.getGames().subscribe(
      x => console.log('Observer got a next value: ' + x)
    );
  }
}
