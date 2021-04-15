import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-matchup',
  templateUrl: './matchup.component.html',
  styleUrls: ['./matchup.component.css']
})


export class MatchupComponent implements OnInit {

  @Input()
  team1!: String;

  @Input()
  team2!: String;

  @Input()
  team1score!: Number;

  @Input()
  team2score!: Number;

  @Input()
  status!: String;

  teams = ['nuggets', 'spurs', 'mavs', 'wolves', 'warriors', '76ers', 'lakers' , 'celtics',
  'jazz', 'suns', 'pels', 'kings', 'rockets', 'heat','bucks', 'hawks', 'nets', 'clippers', 'pistons',
  'knicks', 'bulls', 'blazers', 'hornets','wizards', 'cavs', 'thunder', 'pacers', 'griz','magic'];

  constructor(
  ) { }

  ngOnInit(): void {
  }

}
