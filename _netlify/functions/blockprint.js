import fetch from 'node-fetch';
let data = [];
let lastUpdate = 0;


// https://github.com/sigp/blockprint/blob/main/docs/api.md
// https://api.blockprint.sigp.io/blocks_per_client/${startEpoch}/${endEpoch}
// example blockprint response:
// {
//   "Uncertain": 0,
//   "Lighthouse": 46030,
//   "Lodestar": 0,
//   "Nimbus": 675,
//   "Other": 0,
//   "Prysm": 131291,
//   "Teku": 21713
// }

// https://api.blockprint.sigp.io/accuracy
// example response: 
// {
//   "Lighthouse": {
//     "num_blocks": 47015,
//     "num_correct": 46305,
//     "misclassifications": {
//       "lighthouse-subscribe-none": {
//         "Nimbus": 499,
//         "Prysm": 211
//       }
//     }
//   },
//   ...
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
    const blockprintMarketshareEndpoint = `https://api.blockprint.sigp.io/blocks_per_client/${startEpoch}/${endEpoch}`;
    // endpoint fo the accuracy of fingerprinting for each client
    const blockprintAccuracyEndpoint = 'https://api.blockprint.sigp.io/accuracy';

    try {
      let response = [];
      const [blockprintMarketshare, blockprintAccuracy] = await Promise.all([
        fetch(blockprintMarketshareEndpoint),
        fetch(blockprintAccuracyEndpoint)
      ]);
      const blockprintMarketshareResponse = await blockprintMarketshare.json();
      const blockprintAccuracyResponse = await blockprintAccuracy.json();
      response[0] = blockprintMarketshareResponse;
      response[1] = blockprintAccuracyResponse;
      console.log({"blockprint":response});
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
  const noData = (data.length < 2 || data[0] === undefined || data[0] === null || data[1] === undefined || data[1] === null);
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

