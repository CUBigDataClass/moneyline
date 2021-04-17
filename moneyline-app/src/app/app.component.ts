import { Component } from '@angular/core';
import { IconService } from './icon.service';
import { MatchupService } from './matchup.service';
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import { PredictionComponent } from './prediction/prediction.component';


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
    private matchupService : MatchupService,
    private dialog: MatDialog
  ){
    this.iconService.registerIcons();
    this.matchupService.getGames().then((games)=>{
      this.todayGames = games;
    }).catch(err => console.log(err));
  }
  prediction(){
    let dialogRef = this.dialog.open(PredictionComponent, {
      width: '600px',
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
