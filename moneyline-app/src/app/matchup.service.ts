import { Injectable } from '@angular/core';
import { HttpClient , HttpHeaders, HttpParams} from '@angular/common/http';


@Injectable()
export class MatchupService {

  constructor(
    private http: HttpClient
  ) { }
  
  getGames(){
    let today = new Date();
    let todayStr = today.getFullYear() + '-' + today.getMonth() + '-' + today.getDay();
    console.log(todayStr);
    let params = new HttpParams().set('start_date', todayStr );
    let headers = new HttpHeaders().set("Access-Control-Allow-Origin", "*");
    console.log(headers.keys());
    // headers = headers
    // headers.append("Access-Control-Allow-Methods", "DELETE, POST, GET, OPTIONS");
    // headers.append("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
    const url = 'api/games';
    let options = {
      headers: headers, 
      params: params
    }
    return this.http.get(url, options );
  
   }
  }

