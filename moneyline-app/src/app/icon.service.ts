import { Injectable } from '@angular/core';
import { MatIconRegistry} from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Injectable()
export class IconService {

  teams: { [index: string]: any; } = {'DEN': 'nuggets', 'SAS' : 'spurs', 'DAL': 'mavs', 'MIN':'wolves',
  'GSW' : 'warriors', 'PHI':'76ers', 'LAL' :'lakers' ,
   'BOS':'celtics', 'UTA': 'jazz', 'PHX' : 'suns', 'NOP': 'pels', 
   'SAC':'kings', 'HOU': 'rockets', 'MIA': 'heat','MIL': 'bucks', 
   'ATL': 'hawks','BKN' :'nets', 'LAC' : 'clippers', 'DET' :'pistons',
  'NYK': 'knicks', 'CHI' : 'bulls', 'POR' :'blazers',  'CHA' : 'hornets',
  'WAS': 'wizards', 'CLE': 'cavs', 'OKC' :'thunder', 'IND' : 'pacers', 
  'MEM' : 'griz', 'ORL':'magic'}

  constructor(
    private matIconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer
  ) { }

  public registerIcons(): void {
    this.loadIcons(Object.values(this.teams), '../assets/svg/icons');
  }

  private loadIcons(iconKeys: string[], iconUrl: string): void {
    for (let key in this.teams) {
      console.log('../'+`${iconUrl}/${this.teams[key]}.svg`);
      this.matIconRegistry.addSvgIcon(key, this.domSanitizer.bypassSecurityTrustResourceUrl('../'+`${iconUrl}/${this.teams[key]}.svg`));
    };
  }
}
