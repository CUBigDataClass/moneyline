import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-calculator',
  templateUrl: './calculator.component.html',
  styleUrls: ['./calculator.component.css']
})
export class CalculatorComponent implements OnInit {

  line = -110;
  bet = 0;
  profit = "";
  constructor() { }

  ngOnInit(): void {
  }

  calc_profit(){
    if (this.line > 0){
      this.profit = "$" + (this.bet * Math.abs(this.line/100)).toFixed(2)
    }
    else{
      this.profit = "$" + (this.bet / Math.abs(this.line/100)).toFixed(2)
    }
  }

}
