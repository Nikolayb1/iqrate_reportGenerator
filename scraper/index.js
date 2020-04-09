var path = require('path');
var url = require('url');
var fs = require('fs');
const express = require('express')
const app = express()
const port = 8080
var redis = require('redis');

const {parse, stringify} = require('flatted/cjs');

const {Builder, By, Key, until, wait} = require('selenium-webdriver');
require('chromedriver');

var myVar;
var i = 0;
var driver = new Builder()
.forBrowser('chrome')
.build();
 
async function check_menu(){
    try {
        setTimeout(async function(){
            await (await driver.findElement(By.xpath("//div[@class='_13mwa6jh'][contains(text(), 'Stays')]"))).click().then(function(){
                return 0})
        }, 5000);
        
        
      }
      catch(err) {
        return 0;
      }
}

async function start(counter){
        if(counter < 5){
            setTimeout(async function(){
             await driver.findElements(By.className("_1p7iugi")).then(async function(elements){
                 await elements.forEach(async function (element) {
                     await element.getText().then(async function(text){
                         console.log(text);
                         i++;
                     });
                 });
             });
             await driver.findElement(By.xpath(("//a[@aria-label='Next'][@class='_1li8g8e']"))).click();
             start(++counter);
           }, 6000);
         }else{
             console.log(i);
         }
        
    
    
  }

async function home(location, month, day){
    var visible_month = "";
    await driver.get("https://www.airbnb.co.uk");
    await (await driver.findElement(By.className("_1f8ev6q"))).sendKeys(location, Key.ENTER);
    await choose_date(month, day)
    setTimeout(async function(){
        try{
            await driver.findElement(By.xpath("//div[@class='_13mwa6jh'][contains(text(), 'Stays')]")).click().then(async function(){
                await start(0);
            });
        }catch(err){
            await start(0);
        }
        
    }, 3000)
    
    
}

async function choose_date(month, day){
    await driver.findElements(By.xpath("//div[@class='_gucugi']/strong")).then(async function(elements){
        await elements.forEach(async function (element) {
           await element.getText().then(async function(text){
               //console.log(text + "hello");
               if((text) !== ""){
                   //console.log(text);
                   visible_month = text;
                   var date = visible_month.split(" ");
           
                   if(date[0].toLowerCase() == month){
                       await driver.findElements(By.xpath(("//td[contains(text(), '"+day+"')]"))).then(async function(elements){
                           await elements.forEach(async function (element) {
                               await element.getText().then(async function(text){
                                   if((text) !== ""){
                                
                                    await element.click().then(async function(){
                                        await driver.findElement(By.id("checkout_input")).sendKeys(Key.ENTER);
                                    });
                                    
                                       
                                       
                                   }
                               })
                           })
                       })
                       
                   }else{
                        //_1h5uiygl
                        await driver.findElement(By.className("_1h5uiygl")).click().then(async function(){
                            await choose_date(month, day);
                        
                        });
                        
                        
                        
                   }
               }
           })
           
       })
   })
}
//start(0);
home("London", "april", 20);


app.get('/', function (req, res) {

})


app.listen(8080);