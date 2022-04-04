var consensusGuides = {{site.data.consensus-migration-guides | jsonify}};
var executionGuides = {{site.data.execution-migration-guides | jsonify}};
// console.log(guides);

function setSwitchType() {
  let typeSelect = document.getElementById('typeSelect');
  if (typeSelect.value == "consensus") {
    document.getElementById('switchFromExecution').classList.add("d-none");
    document.getElementById('switchToExecution').classList.add("d-none");
    document.getElementById('switchFromConsensus').classList.remove("d-none");
    document.getElementById('switchToConsensus').classList.remove("d-none");
  }
  if (typeSelect.value == "execution") {
    document.getElementById('switchFromConsensus').classList.add("d-none");
    document.getElementById('switchToConsensus').classList.add("d-none");
    document.getElementById('switchFromExecution').classList.remove("d-none");
    document.getElementById('switchToExecution').classList.remove("d-none");
  }
}

function updateClientSwitchForm(topClient) {
  // set the From input to the most popular client
  let fromSelect = document.getElementById('fromSelectCC');
  fromSelect.value = topClient.toLowerCase();
  // in the To input remove the most popular client
  let toSelect = document.getElementById('toSelectCC');
  for (var i=0; i<toSelect.length; i++) {
    if (toSelect.options[i].value == topClient.toLowerCase()) {
      toSelect.options[i].disabled = true;
      // toSelect.remove(i);
    }
  }
}

// error migrationPath noGuides guides
function getGuides() {
  let guides, fromSelect, toSelect;
  let typeSelect = document.getElementById('typeSelect');
  if (typeSelect.value == "consensus") {
    guides = consensusGuides;
    fromSelect = document.getElementById('fromSelectCC');
    toSelect = document.getElementById('toSelectCC');
  }
  if (typeSelect.value == "execution") {
    guides = executionGuides;
    fromSelect = document.getElementById('fromSelectEC');
    toSelect = document.getElementById('toSelectEC');
  }
  let error = document.getElementById('error');
  let migrationPath = document.getElementById('migrationPath');
  let noGuides = document.getElementById('noGuides');
  let guideList = document.getElementById('guideList');
  let fromClient = document.getElementById('fromClient');
  let toClient = document.getElementById('toClient');
  let blank = "Fresh Install";


  if (fromSelect.value == "none" || toSelect.value == "none") {
    // show error if To and From clients not selected
    hideSwitchSections();
    error.classList.remove("d-none");
  } else {
    hideSwitchSections();
    // update and show the migration path
    fromClient.innerHTML = fromSelect.value[0].toUpperCase() + fromSelect.value.substring(1);
    fromClient.innerHTML = (fromClient.innerHTML == "Blank") ? blank : fromClient.innerHTML;
    toClient.innerHTML = toSelect.value[0].toUpperCase() + toSelect.value.substring(1);
    migrationPath.classList.remove("d-none");
    // check if guide exists
    let path = fromSelect.value + "_to_" + toSelect.value;
    // do checking...
    if (guides[path] == "" || guides[path] == null) {
      noGuides.classList.remove("d-none");
    } else {
      // build guide link list elements
      let guideLinks = "";
      guides[path].forEach(function (guide) {
        let link = guide["link"];
        let author = "";
        if (guide["author"]) {
          author = ", by " + guide["author"];
        }
        let note = "";
        if (guide["note"]) {
          note = " (" + guide["note"] + ")";
        }
        let type = "";
        switch (guide["type"]) {
          case 'doc':
            type = '{{site.data.icons.docs}}';
            break;
          case 'video':
            type = '{{site.data.icons.video}}';
            break;
          case 'tool':
            type = '{{site.data.icons.tool}}';
            break;
        }
        let guideLink = "";
        // create link, language based on fresh install or migration
        if (fromClient.innerHTML == blank) {
          guideLink =  `
            <p class="text-start text-md-center">
              ${type}
              <a href="${link}" target="_blank">${toClient.innerHTML} fresh install guide${note}${author}</a>
              {{site.data.icons.new_tab}}
            </p>`
        } else {
          guideLink =  `
            <p class="text-start text-md-center">
              ${type}
              <a href="${link}" target="_blank">${fromClient.innerHTML} to ${toClient.innerHTML} migration guide${note}${author}</a>
              {{site.data.icons.new_tab}}
            </p>`
          }
        guideLinks += guideLink;
      });
      guideList.innerHTML = guideLinks;
      guideList.classList.remove("d-none");
    }
  }
}

// reset view by hiding all response elements
function hideSwitchSections() {
  let error = document.getElementById('error').classList.add("d-none");
  let migrationPath = document.getElementById('migrationPath').classList.add("d-none");
  let noGuides = document.getElementById('noGuides').classList.add("d-none");
  let guideList = document.getElementById('guideList').classList.add("d-none");
}

// when a client is selected in one list, disable it in the other list
function preventDoubleClientSelect(select) {
  // let fromSelect = document.getElementById('fromSelectCC');
  // let toSelect = document.getElementById('toSelectCC');
  let fromSelect, toSelect;
  let typeSelect = document.getElementById('typeSelect');
  if (typeSelect.value == "consensus") {
    fromSelect = document.getElementById('fromSelectCC');
    toSelect = document.getElementById('toSelectCC');
  }
  if (typeSelect.value == "execution") {
    fromSelect = document.getElementById('fromSelectEC');
    toSelect = document.getElementById('toSelectEC');
  }

  if (select == "fromSelect") {
    let fromClient = fromSelect.value;
    for (var i=0; i<toSelect.length; i++) {
      if (toSelect.options[i].value == fromClient) {
        toSelect.options[i].disabled = true;
        // toSelect.remove(i);
      } else if (toSelect.options[i].value != "openethereum") {
        toSelect.options[i].disabled = false;
      }
    }
  }
  if (select == "toSelect") {
    let toClient = toSelect.value;
    for (var i=0; i<fromSelect.length; i++) {
      if (fromSelect.options[i].value == toClient) {
        fromSelect.options[i].disabled = true;
        // fromSelect.remove(i);
      } else {
        fromSelect.options[i].disabled = false;
      }
    }
  }
}


