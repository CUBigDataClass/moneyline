import { Component, Input, OnInit } from '@angular/core';
import { IconService } from '../icon.service';
import { MatchupService } from './matchup.service';

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

  teams = ['nuggets', 'spurs', 'mavs', 'wolves', 'warriors', '76ers', 'lakers' , 'celtics',
  'jazz', 'suns', 'pels', 'kings', 'rockets', 'heat','bucks', 'hawks', 'nets', 'clippers', 'pistons',
  'knicks', 'bulls', 'blazers', 'hornets','wizards', 'cavs', 'thunder', 'pacers', 'griz','magic'];

  constructor(
    private matchupService : MatchupService,
    private iconService: IconService
    
  ) { }

  ngOnInit(): void {
    // this.matchupService.getGames().subscribe(
    //   x => console.log('Observer got a next value: ' + x)
    // );
  }

}
