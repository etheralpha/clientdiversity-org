window.onload = getData().then(updatePageData).then(setDataSource);


// hard-coded distribution until CORS issue is resolved 
var migalabsData = { "Grandine": 26, "Lighthouse": 664, "Lodestar": 4, "Nimbus": 185, "Others": 1, "Prysm": 2349, "Teku": 321 };
// var blockprintData = { "Uncertain": 0, "Lighthouse": 46030, "Lodestar": 0, "Nimbus": 675, "Other": 0, "Prysm": 135291, "Teku": 21713 };
// lighthouse majority
// var migalabsData = { "Grandine": 26, "Lighthouse": 1264, "Lodestar": 4, "Nimbus": 185, "Others": 1, "Prysm": 349, "Teku": 321 };
// var blockprintData = { "Uncertain": 0, "Lighthouse": 56030, "Lodestar": 0, "Nimbus": 675, "Other": 0, "Prysm": 11291, "Teku": 21713 };
// no majority
// var migalabsData = { "Grandine": 26, "Lighthouse": 664, "Lodestar": 4, "Nimbus": 185, "Others": 1, "Prysm": 349, "Teku": 321 };
var blockprintData = { "Uncertain": 0, "Lighthouse": 46030, "Lodestar": 0, "Nimbus": 675, "Other": 0, "Prysm": 31291, "Teku": 21713 };


var migalabsHasMajority = true;
var migalabsHasExtremeMajority = false;
var migalabsMajorityClient = "Prysm";
var migalabsTopClient = "Prysm";
var blockprintHasMajority = true;
var blockprintHasExtremeMajority = false;
var blockprintMajorityClient = "Prysm";
var blockprintTopClient = "Prysm";


const initialTimestamp = 1606824023;
const initialEpoch = 0;
const currentTimestamp = Math.floor(Date.now() / 1000);
const deltaTimestamp = currentTimestamp - initialTimestamp;
const currentEpoch = Math.floor(deltaTimestamp / 384);

// the Blockprint API caches results so fetching data based on an "epoch day" so 
// everyone that loads the page on an "epoch day" will use the cached results and 
// their backend doesn't get overloaded
// Michael Sproul recommends using a 2-week period
const endEpoch = Math.floor(currentEpoch / 225) * 225;
const startEpoch = endEpoch - 6300;
const blockprintEndpoint = `https://api.blockprint.sigp.io/blocks_per_client/${startEpoch}/${endEpoch}`



// https://github.com/sigp/blockprint/blob/main/docs/api.md
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

// https://migalabs.es/api-documentation
// example MigaLabs response:
  // {
  //     "Grandine": 26,
  //     "Lighthouse": 664,
  //     "Lodestar": 4,
  //     "Nimbus": 185,
  //     "Others": 1,
  //     "Prysm": 2349,
  //     "Teku": 321
  // }



// async function getData() {
//   const [cdResponse] = await Promise.all([
//     fetch("https://migalabs.es/api/v1/client-distribution?crawler=london")
//   ]);
//   const cdJson = await cdResponse.json();
//   console.log(cdJson);
//   return cdJson
// }


async function getData() {
  // https://migalabs.es/api-documentation
  // example response:
  // {
  //     "Grandine": 26,
  //     "Lighthouse": 664,
  //     "Lodestar": 4,
  //     "Nimbus": 185,
  //     "Others": 1,
  //     "Prysm": 2349,
  //     "Teku": 321
  // }

  // commented out until CORS issue is resolved
  // const [cdResponse] = await Promise.all([
    // fetch("https://migalabs.es/api/v1/client-distribution?crawler=london")
  // ]);
  // const cdJson = await cdResponse.json();
  // console.log(cdJson);
  // return cdJson
  return;
}

function updatePageData() {
  updateChart(migalabsData, "migalabs");
  updateChart(blockprintData, "blockprint");
  // populate charts, warning messages, global majority variable
}

// When the data source is toggled, show the respective data
function setDataSource() {
  const datasource = document.querySelector('input[name="datasources"]:checked').value;

  // migalabs elements
  const marketshareWarningMigaLabs = document.getElementById("marketshareWarningMigaLabs");
  const distributionMigaLabs = document.getElementById("distributionMigaLabs");
  const majorityMsgMigaLabs = document.getElementById("majorityMsgMigaLabs");
  // blockprint elements
  const marketshareWarningBlockprint = document.getElementById("marketshareWarningBlockprint");
  const distributionBlockprint = document.getElementById("distributionBlockprint");
  const majorityMsgBlockprint = document.getElementById("majorityMsgBlockprint");


  if (datasource == "migalabs") {
    distributionBlockprint.classList.add("d-none");
    distributionMigaLabs.classList.remove("d-none");

    if (migalabsHasMajority && !migalabsHasExtremeMajority) {
      marketshareWarningBlockprint.classList.add("d-none");
      marketshareWarningMigaLabs.classList.remove("d-none");
      majorityMsgBlockprint.classList.add("d-none");
      majorityMsgMigaLabs.classList.remove("d-none");
      extremeMajorityMsgBlockprint.classList.add("d-none");
      extremeMajorityMsgMigaLabs.classList.add("d-none");
    } else if (migalabsHasExtremeMajority) {
      marketshareWarningBlockprint.classList.add("d-none");
      marketshareWarningMigaLabs.classList.remove("d-none");
      majorityMsgBlockprint.classList.add("d-none");
      majorityMsgMigaLabs.classList.add("d-none");
      extremeMajorityMsgBlockprint.classList.add("d-none");
      extremeMajorityMsgMigaLabs.classList.remove("d-none");
    } else {
      marketshareWarningBlockprint.classList.add("d-none");
      marketshareWarningMigaLabs.classList.add("d-none");
      majorityMsgBlockprint.classList.add("d-none");
      majorityMsgMigaLabs.classList.add("d-none");
      extremeMajorityMsgBlockprint.classList.add("d-none");
      extremeMajorityMsgMigaLabs.classList.add("d-none");
    }
  }
  if (datasource == "blockprint") {
    distributionMigaLabs.classList.add("d-none");
    distributionBlockprint.classList.remove("d-none");

    if (blockprintHasMajority && !blockprintHasExtremeMajority) {
      marketshareWarningMigaLabs.classList.add("d-none");
      marketshareWarningBlockprint.classList.remove("d-none");
      majorityMsgMigaLabs.classList.add("d-none");
      majorityMsgBlockprint.classList.remove("d-none");
      extremeMajorityMsgMigaLabs.classList.add("d-none");
      extremeMajorityMsgBlockprint.classList.add("d-none");
    } else if (blockprintHasExtremeMajority) {
      marketshareWarningMigaLabs.classList.add("d-none");
      marketshareWarningBlockprint.classList.remove("d-none");
      majorityMsgMigaLabs.classList.add("d-none");
      majorityMsgBlockprint.classList.add("d-none");
      extremeMajorityMsgMigaLabs.classList.add("d-none");
      extremeMajorityMsgBlockprint.classList.remove("d-none");
    } else {
      marketshareWarningMigaLabs.classList.add("d-none");
      marketshareWarningBlockprint.classList.add("d-none");
      majorityMsgMigaLabs.classList.add("d-none");
      majorityMsgBlockprint.classList.add("d-none");
      extremeMajorityMsgMigaLabs.classList.add("d-none");
      extremeMajorityMsgBlockprint.classList.add("d-none");
    }
  }

  // handle guides section
}


// update distribution for Miga Labs
function updateChart(data, datasource) {
  let distribution = [];
  let sampleSize = 0;
  let chart = "";
  let hasMajority = false;
  let hasExtremeMajority = false;
  let dangerClient = "";
  let topClient = "";

  // create array of objects
  for (var key in data) {
    distribution.push({ "name": key, "value": data[key] });
  }
  // sort by value
  distribution.sort(function (a, b) {
    return b.value - a.value;
  });
  // get the total sample size to derive the marketshare
  distribution.forEach(function (item) {
    sampleSize += item["value"];
  });
  // get the most popular client
  topClient = distribution[0]["name"];

  // create the chart
  distribution.forEach(function (item) {
    let client = item["name"][0].toUpperCase() + item["name"].substring(1);
    let marketshare = Math.round( item["value"] / sampleSize * 10000 )/100;
    let fontWeight = "fw-normal";
    let color = "success";
    if (marketshare > 50) {
      fontWeight = "fw-bold";
      color = "danger";
      hasMajority = true;
      dangerClient = client;
      if (marketshare > 66) {
        hasExtremeMajority = true;
      }
    } else if (marketshare > 33) {
      color = "warning";
    }
    let bar =  `
      <div class="my-2">
        <label class="form-label my-0 py-0 ${fontWeight}">${client} - ${marketshare}%</label>
        <div class="progress position-relative" style="height: 1.3rem;">
          <div class="progress-bar position-absolute bg-${color}" role="progressbar" style="width: ${marketshare}%; height: 1.25rem;" aria-valuenow="${marketshare}" aria-valuemin="0" aria-valuemax="100"></div>
          <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
          <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
          <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
        </div>
      </div>`;
    chart += bar;
  });

  if (datasource == "migalabs") {
    document.getElementById("distributionBarsMigaLabs").innerHTML = chart;
    document.getElementById("dangerClientsMigaLabs").innerHTML = dangerClient;
    migalabsHasMajority = hasMajority;
    migalabsHasExtremeMajority = hasExtremeMajority;
    migalabsMajorityClient = dangerClient;
    migalabsTopClient = topClient;
  }
  if (datasource == "blockprint") {
    document.getElementById("distributionBarsBlockprint").innerHTML = chart;
    document.getElementById("dangerClientsBlockprint").innerHTML = dangerClient;
    blockprintHasMajority = hasMajority;
    blockprintHasExtremeMajority = hasExtremeMajority;
    blockprintMajorityClient = dangerClient;
    blockprintTopClient = topClient;
  }

  return;
}






