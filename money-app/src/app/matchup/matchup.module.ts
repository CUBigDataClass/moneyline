import { NgModule } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { MatchupComponent } from './matchup.component';




@NgModule({
  declarations: [
    MatchupComponent,
  ],
  imports: [
    CommonModule,
    HttpClientModule,
  ],
  exports: [
    MatchupComponent
  ],
  providers: [
    DatePipe
  ]
})
export class MatchupModule { }
