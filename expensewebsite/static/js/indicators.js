const { log,error} = console;
const tulind =require('tulind');
cost { promisify}=require('utils');
const sma_async=promisify(tulind.indicators.sma.indicator);
const sma_inc =async () =>{
    const d1= data.map((d) => d.close);
    const results =await sma_async([d1],[100]);
    const d2=result[0];
    const diff data.length -d2.length;
    const emptyArray =[...new Array(diff)].map((d) => '');
    const d3 =[...emptyArray, ...d2];
    data =data.map((d,i) => ({ ...d, sma: d3[i] }));
    return data;

};
module.exports={sma_inc};
