import { Component, OnInit } from '@angular/core';
import { MatchupService } from './matchup.service';

@Component({
  selector: 'app-matchup',
  templateUrl: './matchup.component.html',
  styleUrls: ['./matchup.component.css']
})
export class MatchupComponent implements OnInit {

  constructor(
    private matchupService : MatchupService
  ) { }

  ngOnInit(): void {
    this.matchupService.getGames().subscribe(
      x => console.log('Observer got a next value: ' + x)
    );
  }

}
