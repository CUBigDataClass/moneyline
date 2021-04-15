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

  confidence!: number;

  winner!: String;

  constructor(private matchupService : MatchupService) {

  }

  ngOnInit(): void {
    let res = this.matchupService.getPrediction()
    this.team1 = res.team1
    this.team2 = res.team2
    this.confidence = res.confidence
    this.winner = res.winner
  }

}
