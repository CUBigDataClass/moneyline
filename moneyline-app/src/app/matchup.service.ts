import { Injectable } from '@angular/core';
import { HttpClient , HttpParams} from '@angular/common/http';

interface info {
  current_page: Number;
  next_page: Number;
  per_page: Number;
  total_count: Number;
  total_pages:Number;
}

interface game {
  id: Number;
  date: Date;
  home_team: {
      id: 29,
      abbreviation: String;
      city: String;
      conference: String;
      division: String;
      full_name: String;
      name: String;
  },
  home_team_score: Number;
  period: Number;
  postseason: Boolean;
  season: Number;
  status: String;
  time: String,
  visitor_team: {
      id: Number;
      abbreviation: String;
      city: String;
      conference: String;
      division: String;
      full_name: String;
      name: String;
  },
  visitor_team_score: Number;
}

interface res {
  data: Array<game>;
  meta: info;
}

@Injectable()
export class MatchupService {

  constructor(
    private http: HttpClient
  ) { }
  
  async getGames(){
    let today = new Date();
    let todayStr = today.getFullYear() + '-' + (today.getMonth()+1).toString() + '-' + today.getDate();
    let params = new HttpParams().set('start_date', todayStr ).set('end_date', todayStr );
    const url = 'api/games';
    const res = await this.http.get<res>(url, {params:params} ).toPromise();
    return res.data;
  
   }

  async getPrediction(home: String ,away: String ){
    const url = 'get/'+home+'/'+away;
    const res:any = await this.http.get<res>(url).toPromise();
    return res[0];
  }
  }

