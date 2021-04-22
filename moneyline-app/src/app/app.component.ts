import { Component, OnInit, OnDestroy } from '@angular/core';
import { IconService } from './icon.service';
import { MatchupService } from './matchup.service';
import {MatDialog, MatDialogConfig, MatDialogModule} from '@angular/material/dialog';
import { PredictionComponent } from './prediction/prediction.component';
import { CalculatorComponent } from './calculator/calculator.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {

  teams: { [index: string]: any; } = {'DEN': 'nuggets', 'SAS' : 'spurs', 'DAL': 'mavs', 'MIN':'wolves',
  'GSW' : 'warriors', 'PHI':'76ers', 'LAL' :'lakers' , 'TOR': 'raptors',
   'BOS':'celtics', 'UTA': 'jazz', 'PHX' : 'suns', 'NOP': 'pels', 
   'SAC':'kings', 'HOU': 'rockets', 'MIA': 'heat','MIL': 'bucks', 
   'ATL': 'hawks','BKN' :'nets', 'LAC' : 'clippers', 'DET' :'pistons',
  'NYK': 'knicks', 'CHI' : 'bulls', 'POR' :'blazers',  'CHA' : 'hornets',
  'WAS': 'wizards', 'CLE': 'cavs', 'OKC' :'thunder', 'IND' : 'pacers', 
  'MEM' : 'griz', 'ORL':'magic'}

  options = Object.keys(this.teams).sort();

  
  todayGames: game[] = [];

  homeTeam : String = 'DEN';
  awayTeam : String = 'LAL';
  homeBias : number = 0;
  opened: boolean = false;

  title = 'moneyline-app';

  interval

  constructor(
    private iconService: IconService,
    private matchupService : MatchupService,
    private dialog: MatDialog
  ){
    
    this.iconService.registerIcons();
    this.matchupService.getGames().then((games)=>{
      this.todayGames = games;
    }).catch(err => console.log(err));
    this.interval = setInterval(()=> {
      this.matchupService.getGames().then((games)=>{
        this.todayGames = games;
      }).catch(err => console.log(err));
    }, 30000);
  }

  prediction(team1:String,team2:String,bias:number){
    const dialogConfig = new MatDialogConfig();
    dialogConfig.data = {
      home: team1,
      away: team2,
      bias: bias
  };
    dialogConfig.width = '600px';
    this.dialog.open(PredictionComponent, dialogConfig);
  }


  calculator(){
    const dialogConfig = new MatDialogConfig();
    dialogConfig.width = '600px';
    this.dialog.open(CalculatorComponent, dialogConfig);
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
