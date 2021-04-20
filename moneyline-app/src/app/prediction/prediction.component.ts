import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Inject } from '@angular/core';
import { Component,  OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatchupService } from '../matchup.service';

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent implements OnInit {

  team1!: String;

  team2!: String;

  confidence!: Number;

  winner!: String;

  data

  res : any

  constructor(
    private matchupService : MatchupService,
    private dialogRef: MatDialogRef<PredictionComponent>,
        @Inject(MAT_DIALOG_DATA) data : any
    ) {
      
      this.data = data;

  }

  ngOnInit(): void {
    this.matchupService.getPrediction(this.data['home'], this.data['away']).then(res=>{
      this.res = res;
      this.team1 = this.res['HOME_TEAM'];
      this.team2 = this.res['AWAY_TEAM'];
      this.confidence = this.res['PROBABILITY'];
      this.winner = this.res['WINNER'];
    });
  }

  getProb(team: String){
    if (team === this.winner){
      return (100*this.confidence.valueOf()).toFixed(2) + "%"
    }
    else{
      return (100*(1 - this.confidence.valueOf())).toFixed(2) + "%"
    }
  }

  getLines(team: String){
    var p

    if (team === this.winner){
      p = this.confidence.valueOf()
    }
    else{
      p = 1 - this.confidence.valueOf()
    }

    if (p > 0.5){
      return (-100 / (1/p - 1)).toFixed(0)
    }
    else{
      return "+" + (100 * (1/p - 1)).toFixed(0)
    }
  }

}
