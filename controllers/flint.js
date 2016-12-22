/**
 * Code to read python script
 */
const _ = require('lodash');
const spawn = require('child_process').spawn;
let py, dataString, input_data;

exports.getHello = (bot, trigger) => {
    bot.say("Hello %s! How may i help you today. To know list of commands you can type **Help**.", trigger.personDisplayName);
};

exports.getHelp = (bot, trigger) => {
    let str = "Please find below a list of commands you can use: \n" +
        "- Search \<Query\>.";

    bot.say(str);
};

exports.getSearch = (bot, trigger) => {
  py = spawn('python', ['./document_prediction.py']);
  dataString = '';
  
  input_data = _.drop(trigger.args);
  input_data = _.join(input_data, ' ');

  let inputData = JSON.stringify([input_data]);
  main(inputData)
    .then(result => {
            title = 'Please find below a list of top 5 results i found: \n - '
            result = JSON.parse(result)
            result = _.join(result, '\n - ');
            result = title + result;
            bot.say(result);
        })
};

function main(inputData) {
  return new Promise(function(resolve, reject){

    py.stdout.on('data', function(data){
        dataString += data.toString();
    });
    py.stdout.on('end', function(){
        console.log(dataString);
        resolve(dataString);
    });
    py.stdout.on('error', function(){
        console.log('error');
        reject('error');
    });

    py.stdin.write(inputData);
    py.stdin.end();
  })
}