import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatchupComponent } from './matchup.component';
import { HttpClientModule } from '@angular/common/http';
import { MatchupService } from './matchup.service';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';



@NgModule({
  declarations: [
    MatchupComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule,
    MatCardModule,
    MatIconModule
  ],
  providers:[
    MatchupService
  ],
  exports: [
    MatchupComponent
  ]
})
export class MatchupModule { }
