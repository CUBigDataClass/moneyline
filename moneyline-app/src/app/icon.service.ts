import { Injectable } from '@angular/core';
import { MatIconRegistry} from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Injectable()
export class IconService {

  teams = ['nuggets', 'spurs', 'mavs', 'wolves', 'warriors', '76ers', 'lakers' , 'celtics',
  'jazz', 'suns', 'pels', 'kings', 'rockets', 'heat','bucks', 'hawks', 'nets', 'clippers', 'pistons',
  'knicks', 'bulls', 'blazers', 'hornets','wizards', 'cavs', 'thunder', 'pacers', 'griz','magic']

  constructor(
    private matIconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer
  ) { }

  public registerIcons(): void {
    this.loadIcons(Object.values(this.teams), '../assets/svg/icons');
  }

  private loadIcons(iconKeys: string[], iconUrl: string): void {
    iconKeys.forEach(key => {
      this.matIconRegistry.addSvgIcon(key, this.domSanitizer.bypassSecurityTrustResourceUrl('../'+`${iconUrl}/${key}.svg`));
    });
  }
}
