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
      // sort list based on status field which is time of tipoff
      let sorted = games.sort((a, b) => Number(a.status.split(":")[0]+a.status.split(":")[1].substring(0,2)) > Number(b.status.split(":")[0]+b.status.split(":")[1].substring(0,2)) ? 1 : -1);
      this.todayGames = sorted;
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
  status: String;
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
