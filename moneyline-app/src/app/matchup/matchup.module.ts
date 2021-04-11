import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatchupComponent } from './matchup.component';
import { HttpClientModule } from '@angular/common/http';
import { MatchupService } from './matchup.service';



@NgModule({
  declarations: [
    MatchupComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule
  ],
  providers:[
    MatchupService
  ],
  exports: [
    MatchupComponent
  ]
})
export class MatchupModule { }
