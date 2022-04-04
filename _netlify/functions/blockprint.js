import fetch from 'node-fetch';
let data;
let lastUpdate = 0;


// https://github.com/sigp/blockprint/blob/main/docs/api.md
// https://api.blockprint.sigp.io/blocks_per_client/${startEpoch}/${endEpoch}
// example Blockprint response:
// {
//   "Uncertain": 0,
//   "Lighthouse": 46030,
//   "Lodestar": 0,
//   "Nimbus": 675,
//   "Other": 0,
//   "Prysm": 131291,
//   "Teku": 21713
// }


exports.handler = async (event, context) => {
  const fetchData = async () => {
    const initialTimestamp = 1606824023; // seconds
    const initialEpoch = 0;
    const currentTimestamp = Math.floor(Date.now() / 1000); // seconds
    const deltaTimestamp = currentTimestamp - initialTimestamp; // seconds
    const currentEpoch = Math.floor(deltaTimestamp / 384);

    // the Blockprint API caches results so fetching data based on an "epoch day" so 
    // everyone that loads the page on an "epoch day" will use the cached results and 
    // their backend doesn't get overloaded
    // Michael Sproul recommends using a 2-week period
    const endEpoch = Math.floor(currentEpoch / 225) * 225;
    const startEpoch = endEpoch - 3150;
    const blockprintEndpoint = `https://api.blockprint.sigp.io/blocks_per_client/${startEpoch}/${endEpoch}`;

    try {
      const response = await fetch(blockprintEndpoint).then( response => response.json() );
      console.log(response);
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

