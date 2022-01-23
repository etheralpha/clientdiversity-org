var guides = {{site.data.migration-guides | replace: '=>', ':' | replace: 'nil', '""'}};
// console.log(guides);

function updateClientSwitchForm(topClient) {
  // set the From input to the most popular client
  let fromSelect = document.getElementById('fromSelect');
  fromSelect.value = topClient.toLowerCase();
  // in the To input remove the most popular client
  let toSelect = document.getElementById('toSelect');
  for (var i=0; i<toSelect.length; i++) {
    if (toSelect.options[i].value == topClient.toLowerCase())
      toSelect.remove(i);
      // toSelect.options[i].disabled = true;
  }
}

// error migrationPath noGuides guides
function getGuides() {
  let fromSelect = document.getElementById('fromSelect');
  let toSelect = document.getElementById('toSelect');
  let error = document.getElementById('error');
  let migrationPath = document.getElementById('migrationPath');
  let noGuides = document.getElementById('noGuides');
  let guideList = document.getElementById('guideList');
  let fromClient = document.getElementById('fromClient');
  let toClient = document.getElementById('toClient');


  if (fromSelect.value == "none" || toSelect.value == "none") {
    // show error if To and From clients not selected
    hideSwitchSections();
    error.classList.remove("d-none");
  } else {
    hideSwitchSections();
    // update and show the migration path
    fromClient.innerHTML = fromSelect.value[0].toUpperCase() + fromSelect.value.substring(1);
    toClient.innerHTML = toSelect.value[0].toUpperCase() + toSelect.value.substring(1);
    migrationPath.classList.remove("d-none");
    // check if guide exists
    let path = fromSelect.value + "_to_" + toSelect.value;
    // do checking...
    if (guides[path] == "") {
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
        let guideLink =  `
          <p class="text-start text-md-center">
            ${type}
            <a href="${link}" target="_blank">${fromClient.innerHTML} to ${toClient.innerHTML} migration guide${note}${author}</a>
            {{site.data.icons.new_tab}}
          </p>`
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
  let fromSelect = document.getElementById('fromSelect');
  let toSelect = document.getElementById('toSelect');

  if (select.id == "fromSelect") {
    let fromClient = fromSelect.value;
    for (var i=0; i<toSelect.length; i++) {
      if (toSelect.options[i].value == fromClient) {
        // toSelect.remove(i);
        toSelect.options[i].disabled = true;
      } else {
        toSelect.options[i].disabled = false;
      }
    }
  }
  if (select.id == "toSelect") {
    let toClient = toSelect.value;
    for (var i=0; i<fromSelect.length; i++) {
      if (fromSelect.options[i].value == toClient) {
        // fromSelect.remove(i);
        fromSelect.options[i].disabled = true;
      } else {
        fromSelect.options[i].disabled = false;
      }
    }
  }
}


