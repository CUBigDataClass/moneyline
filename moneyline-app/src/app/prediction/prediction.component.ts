import { Component, OnInit } from '@angular/core';
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

  constructor(private matchupService : MatchupService) {

  }

  ngOnInit(): void {
    this.matchupService.getPrediction().then(res=>{
      console.log(res)});

    // this.team1 = res.team1
    // this.team2 = res.team2
    // this.confidence = res.confidence
    // this.winner = res.winner
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
