import { Component } from '@angular/core';
import { IconService } from './icon.service';
import { MatchupService } from './matchup.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {

  
  todayGames: game[] = [];
  title = 'moneyline-app';
  constructor(
    private iconService: IconService,
    private matchupService : MatchupService
  ){
    this.iconService.registerIcons();
    this.matchupService.getGames().then((games)=>{
      this.todayGames = games;
    });
  }
}

export interface game {
  id: Number;
  date: Date;
  home_team: {
      id: 29,
      abbreviation: String;
      city: String;
      conference: String;
      division: String;
      full_name: String;
      name: String;
  },
  home_team_score: Number;
  period: Number;
  postseason: Boolean;
  season: Number;
  status: Date;
  time: String,
  visitor_team: {
      id: Number;
      abbreviation: String;
      city: String;
      conference: String;
      division: String;
      full_name: String;
      name: String;
  },
  visitor_team_score: Number;
}
