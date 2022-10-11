window.onload = getData().then(updatePageData).then(setDataSources);


var ethernodesData = [
  { "client":"geth",         "value":4421 },
  { "client":"openethereum", "value":333  },
  { "client":"erigon",       "value":300  },
  { "client":"nethermind",   "value":63   },
  { "client":"besu",         "value":31   },
  { "client":"coregeth",     "value":5    },
  { "client":"teth",         "value":3    },
  { "client":"merp-client",  "value":2    }
];
var migalabsData = {
    "Grandine": 49,
    "Lighthouse": 1194,
    "Lodestar": 8,
    "Nimbus": 191,
    "Others": 4,
    "Prysm": 2257,
    "Teku": 358
};
var blockprintData = {
  "Uncertain": 0,
  "Lighthouse": 25508,
  "Lodestar": 0,
  "Nimbus": 2030,
  "Other": 0,
  "Prysm": 54699,
  "Teku": 17879
};
var blockprintAccuracy;

var migalabsHasMajority = true;
var migalabsHasExtremeMajority = false;
var migalabsMajorityClient = "Prysm";
var migalabsTopClient = "Prysm";

var blockprintHasMajority = true;
var blockprintHasExtremeMajority = false;
var blockprintMajorityClient = "Prysm";
var blockprintTopClient = "Prysm";

var ethernodesHasMajority = true;
var ethernodesHasExtremeMajority = true;
var ethernodesMajorityClient = "Geth";
var ethernodesTopClient = "Geth";


async function getData() {
  try {
    const [migalabs, blockprint, ethernodes] = await Promise.all([
      fetch("/.netlify/functions/migalabs/"),
      fetch("/.netlify/functions/blockprint/"),
      fetch("/.netlify/functions/ethernodes/")
    ]);
    const migalabsResponse = await migalabs.json();
    const blockprintResponse = await blockprint.json();
    const ethernodesResponse = await ethernodes.json();
    migalabsData = migalabsResponse;
    blockprintData = blockprintResponse[0];
    blockprintAccuracy = blockprintResponse[1];
    ethernodesData = ethernodesResponse;
  }
  catch {
    console.error("Failed to load data")
  }

  return;
}


function updatePageData() {
  createChart(migalabsData, "migalabs");
  createChart(blockprintData, "blockprint");
  createChart(ethernodesData, "ethernodes");
}


// create and update chart
function createChart(data, datasource) {
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
    let client = item["name"].replace("-"," ").split(' ')
      .map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ');
    let marketshare = Math.round( item["value"] / sampleSize * 10000 )/100;
    let fontWeight = "fw-normal";
    let color = "success";
    let status = "danger!";
    let accuracy = "no data";
    if (marketshare > 50) {
      fontWeight = "fw-bold";
      color = "danger";
      status = "great!";
      hasMajority = true;
      dangerClient = client;
      if (marketshare > 66) {
        hasExtremeMajority = true;
      }
    } else if (marketshare > 33) {
      color = "warning";
      status = "caution";
    }
    if (datasource == "blockprint") {
      if (blockprintAccuracy && blockprintAccuracy[client]) {
        let blocksTotal = blockprintAccuracy[client]['num_blocks'];
        let blocksCorrect = blockprintAccuracy[client]['num_correct'];
        accuracy = Math.round( blocksCorrect/blocksTotal*1000 ) / 10 + '%';
      }
    }

    let bar = `
      <div class="my-2">
        <label class="form-label my-0 py-0 ${fontWeight}">${client} - ${marketshare}%</label>
        <div class="progress position-relative" style="height: 1.3rem;" 
          data-bs-toggle="tooltip" data-bs-placement="top" data-bs-html="true" title='
              <div class="progress-tooltip text-capitalize text-start">
                <div class="mb-1 pb-1 text-center border-bottom border-secondary">
                  ${client} status:<br>${marketshare}% (${status})
                </div>
                <div class="d-flex justify-content-between">
                  <span class="me-2">great:</span><span>0-33%</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="me-2">caution:</span><span>33-50%</span>
                </div>
                <div class="d-flex justify-content-between mb-1 pb-1 border-bottom border-secondary">
                <span class="me-2">danger:</span><span>50-100%</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="me-2">accuracy:</span><span>${accuracy}</span>
                </div>
              </div>'>
          <div class="progress-bar position-absolute bg-${color}" role="progressbar" style="width: ${marketshare}%; height: 1.25rem;" aria-valuenow="${marketshare}" aria-valuemin="0" aria-valuemax="100"></div>
          <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
          <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
          <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
        </div>
      </div>`;
    chart += bar;
    enableTooltips();
  });

  // populate respective html and set global variables
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
  if (datasource == "ethernodes") {
    document.getElementById("distributionBarsEthernodes").innerHTML = chart;
    document.getElementById("dangerClientsEthernodes").innerHTML = dangerClient;
    ethernodesHasMajority = hasMajority;
    ethernodesHasExtremeMajority = hasExtremeMajority;
    ethernodesMajorityClient = dangerClient;
    ethernodesTopClient = topClient;
  }

  return;
}


// when the data source is toggled, show the respective data
function setDataSources() {
  const datasourceCC = document.querySelector('input[name="datasourcesCC"]:checked').value;
  const marketshareSuccessCC = document.getElementById("marketshareSuccessCC");

  const datasourceEC = document.querySelector('input[name="datasourcesEC"]:checked').value;
  const marketshareSuccessEC = document.getElementById("marketshareSuccessEC");

  // migalabs elements
  const marketshareWarningMigaLabs = document.getElementById("marketshareWarningMigaLabs");
  const distributionMigaLabs = document.getElementById("distributionMigaLabs");
  const majorityMsgMigaLabs = document.getElementById("majorityMsgMigaLabs");
  const extremeMajorityMsgMigaLabs = document.getElementById("extremeMajorityMsgMigaLabs");
  // blockprint elements
  const marketshareWarningBlockprint = document.getElementById("marketshareWarningBlockprint");
  const distributionBlockprint = document.getElementById("distributionBlockprint");
  const majorityMsgBlockprint = document.getElementById("majorityMsgBlockprint");
  const extremeMajorityMsgBlockprint = document.getElementById("extremeMajorityMsgBlockprint");
  // ethernodes elements
  const marketshareWarningEthernodes = document.getElementById("marketshareWarningEthernodes");
  const distributionEthernodes = document.getElementById("distributionEthernodes");
  // const majorityMsgEthernodes = document.getElementById("majorityMsgEthernodes");
  // const extremeMajorityMsgEthernodes = document.getElementById("extremeMajorityMsgEthernodes");

  // hide all elements to reset
  distributionMigaLabs.classList.add("d-none");
  distributionBlockprint.classList.add("d-none");
  distributionEthernodes.classList.add("d-none");

  marketshareWarningMigaLabs.classList.add("d-none");
  marketshareWarningBlockprint.classList.add("d-none");
  marketshareWarningEthernodes.classList.add("d-none");

  marketshareSuccessCC.classList.add("d-none");
  marketshareSuccessEC.classList.add("d-none");

  majorityMsgMigaLabs.classList.add("d-none");
  majorityMsgBlockprint.classList.add("d-none");
  // majorityMsgEthernodes.classList.add("d-none");

  extremeMajorityMsgMigaLabs.classList.add("d-none");
  extremeMajorityMsgBlockprint.classList.add("d-none");
  // extremeMajorityEthernodes.classList.add("d-none");

  // show only relevant elements
  if (datasourceCC == "migalabs") {
    updateClientSwitchForm(migalabsTopClient);
    distributionMigaLabs.classList.remove("d-none");
    if (migalabsHasMajority && !migalabsHasExtremeMajority) {
      marketshareWarningMigaLabs.classList.remove("d-none");
      majorityMsgMigaLabs.classList.remove("d-none");
    }
    if (migalabsHasExtremeMajority) {
      marketshareWarningMigaLabs.classList.remove("d-none");
      extremeMajorityMsgMigaLabs.classList.remove("d-none");
    }
    if (!migalabsHasMajority) {
      marketshareSuccessCC.classList.remove("d-none");
    }
  }
  if (datasourceCC == "blockprint") {
    updateClientSwitchForm(blockprintTopClient);
    distributionBlockprint.classList.remove("d-none");
    if (blockprintHasMajority && !blockprintHasExtremeMajority) {
      marketshareWarningBlockprint.classList.remove("d-none");
      majorityMsgBlockprint.classList.remove("d-none");
    }
    if (blockprintHasExtremeMajority) {
      marketshareWarningBlockprint.classList.remove("d-none");
      extremeMajorityMsgBlockprint.classList.remove("d-none");
    }
    if (!blockprintHasMajority) {
      marketshareSuccessCC.classList.remove("d-none");
    }
  }
  if (datasourceEC == "ethernodes") {
    // updateClientSwitchForm(ethernodesTopClient);
    distributionEthernodes.classList.remove("d-none");
    if (ethernodesHasMajority && !ethernodesHasExtremeMajority) {
      marketshareWarningEthernodes.classList.remove("d-none");
      // majorityMsgEthernodes.classList.remove("d-none");
    }
    if (ethernodesHasExtremeMajority) {
      marketshareWarningEthernodes.classList.remove("d-none");
      // extremeMajorityMsgEthernodes.classList.remove("d-none");
    }
    if (!ethernodesHasMajority) {
      marketshareSuccessEC.classList.remove("d-none");
    }
  }
}


