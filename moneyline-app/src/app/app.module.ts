import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatchupModule } from './matchup/matchup.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { IconService } from './icon.service';
import { MatchupService } from './matchup.service';
import { HttpClientModule } from '@angular/common/http';
import { MatCardModule } from '@angular/material/card';
import {MatToolbarModule} from '@angular/material/toolbar';
import { PredictionComponent } from './prediction/prediction.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button'


@NgModule({
  declarations: [
    AppComponent,
    PredictionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatchupModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatToolbarModule,
    MatDialogModule,
    MatIconModule,
    MatCardModule,
    MatButtonModule,
  ],
  providers: [
    IconService,
    MatchupService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
