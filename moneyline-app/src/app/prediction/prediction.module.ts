import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatchupService } from '../matchup.service';
import { PredictionComponent } from './prediction.component';



@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    PredictionComponent,
  ],
  providers: [
    MatchupService,
  ]
})
export class PredictionModule { }
