import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatchupComponent } from './matchup/matchup.component';
import { MatchupModule } from './matchup/matchup.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatchupModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
