import fetch from 'node-fetch';
const API_ENDPOINT = 'https://migalabs.es/api/v1/client-distribution';
let data;
let lastUpdate = 0;


// https://migalabs.es/api-documentation
// https://migalabs.es/api/v1/client-distribution?crawler=london
// example migalabs response:
// {
//     "Grandine": 26,
//     "Lighthouse": 664,
//     "Lodestar": 4,
//     "Nimbus": 185,
//     "Others": 1,
//     "Prysm": 2349,
//     "Teku": 321
// }


exports.handler = async (event, context) => {
  const fetchData = async () => {
    try {
      const response = await fetch(API_ENDPOINT).then( response => response.json() );
      let consensusClients = ["grandine","lighthouse","lodestar","nimbus","prysm","teku","unknown"];
      for (const [key, value] of Object.entries(response)) {
        if (!consensusClients.includes(key)) {
          response["unknown"] += response[key];
          delete response[key];
        }
      }
      console.log({"migalabs":response});
      return response;
    } catch (err) {
      return {
        statusCode: err.statusCode || 500,
        body: JSON.stringify({
          error: err.message
        })
      }
    }
  }

  // If cached data from the past 12 hrs, send that, otherwise fetchData
  const currentTime = new Date().getTime();
  const noData = (data === undefined || data === null);
  if (noData || ( currentTime - lastUpdate > 43200000 )) { // 43200000 = 12hrs
    const response = await fetchData();
    data = response;
    lastUpdate = new Date().getTime();
    return {
      statusCode: 200,
      body: JSON.stringify(data)
    }
  } else {
    return {
      statusCode: 200,
      body: JSON.stringify(data)
    }
  }
}

