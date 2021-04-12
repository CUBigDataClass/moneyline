import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatchupModule } from './matchup/matchup.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { IconService } from './icon.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatchupModule,
    BrowserAnimationsModule
  ],
  providers: [IconService],
  bootstrap: [AppComponent]
})
export class AppModule { }
