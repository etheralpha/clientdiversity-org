import fetch from 'node-fetch';
const API_ENDPOINT = 'https://ethernodes.org/api/clients';
let data;
let lastUpdate = 0;


// https://ethernodes.org/api/clients
// example MigaLabs response:
// [
//   { "client":"geth",         "value":4421 },
//   { "client":"openethereum", "value":333  },
//   { "client":"erigon",       "value":300  },
//   { "client":"nethermind",   "value":63   },
//   { "client":"besu",         "value":31   },
//   { "client":"coregeth",     "value":5    },
//   { "client":"teth",         "value":3    },
//   { "client":"merp-client",  "value":2    }
// ]


exports.handler = async (event, context) => {
  const fetchData = async () => {
    try {
      const response = await fetch(API_ENDPOINT).then( response => response.json() );
      // reformat to match blockprint and migalabs
      let mainClients = ["geth", "openethereum", "erigon", "nethermind", "besu"];
      let others = 0;
      let formattedResponse = {};
      for (let item in response) {
        let key = response[item]["client"];
        let value = response[item]["value"];
        if (mainClients.includes(key)) {
          key = (key == "openethereum") ? "openEthereum" : key;
          formattedResponse[key] = value;
        } else {
          others += value;
        }
      }
      formattedResponse["others"] = others;
      console.log(response);
      console.log(formattedResponse)
      return formattedResponse;
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

