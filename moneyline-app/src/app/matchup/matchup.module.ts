import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatchupComponent } from './matchup.component';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';



@NgModule({
  declarations: [
    MatchupComponent
  ],
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule
  ],
  providers:[
  ],
  exports: [
    MatchupComponent
  ]
})
export class MatchupModule { }
