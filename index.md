---
layout: default
---


<header class="pb-md-3 pb-lg-5">
 <div class="px-4 py-5 my-5 text-center">
    <h1 class="display-1 fw-bold mt-5">Diversify Now</h1>
    <div class="col-lg-7 mx-auto">
      <p class="h4 fw-normal mb-4">Improve Etheruem's resiliance by using a minority client</p>
      <a href="#switch" class="btn btn-dark btn-lg px-4 m-1">Switch Clients</a>
      <a href="#why" class="btn btn-outline-dark btn-lg px-4 m-1">Learn More</a>
    </div>
  </div>
</header>

<!-- Logos -->
<section class="bg-light">
  <div class="container my-5">
    <div class="row text-center">
      <div class="col text-center">
        <img src="/assets/img/clients/lighthouse-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/lodestar-logo-text.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/prysm-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/nimbus-logo-text.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/teku-logo.png" alt="" class="my-2 client-logos">
      </div>
    </div>
  </div>
</section>

<!-- Client Distribution -->
<section id="distribution" class="">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Client Distribution</h2>
    <div class="row justify-content-center mt-4">
      <div class="col col-lg-6 col-md-8 text-center">
        <p class="lead">Goal: &#60;33% <span class="mx-2">|</span> Danger: &#62;50%</p>
        <a id="marketshatWarning" href="#why" class="text-decoration-none d-none">
          <div class="alert alert-danger d-flex align-items-center" role="alert">
            {{site.data.icons.warning}}
            <div>We need to move away from <span id="dangerClients">Prysm</span> to minority clients!</div>
          </div>
        </a>
      </div>
    </div>
    <div class="row justify-content-center">
      <div id="distributionBars" class="col col-lg-6 col-md-8">
        <div class="my-2">
          <label id="prysmLabel" class="form-label my-0 py-0 fw-bold">Prysm - <span id="prysmText">59.47%</span></label>
          <div class="progress position-relative" style="height: 1.3rem;">
            <div id="prysmProgress" class="progress-bar position-absolute bg-danger" role="progressbar" style="width: 59.47%; height: 1.25rem;" aria-valuenow="59.47" aria-valuemin="0" aria-valuemax="100"></div>
            <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
          </div>
        </div>
        <div class="my-2">
          <label id="lighthouseLabel" class="form-label my-0 py-0">Lighthouse - <span id="lighthouseText">24.64%</span></label>
          <div class="progress position-relative" style="height: 1.3rem;">
            <div id="lighthouseProgress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 24.64%; height: 1.25rem;" aria-valuenow="24.64" aria-valuemin="0" aria-valuemax="100"></div>
            <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
          </div>
        </div>
        <div class="my-2">
          <label id="tekuLabel" class="form-label my-0 py-0">Teku - <span id="tekuText">9.54%</span></label>
          <div class="progress position-relative" style="height: 1.3rem;">
            <div id="tekuProgress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 9.54%; height: 1.25rem;" aria-valuenow="9.54" aria-valuemin="0" aria-valuemax="100"></div>
            <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
          </div>
        </div>
        <div class="my-2">
          <label id="nimbusLabel" class="form-label my-0 py-0">Nimbus - <span id="nimbusText">5.11%</span></label>
          <div class="progress position-relative" style="height: 1.3rem;">
            <div id="nimbusProgress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 5.11%; height: 1.25rem;" aria-valuenow="5.11" aria-valuemin="0" aria-valuemax="100"></div>
            <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
          </div>
        </div>
        <div class="my-2">
          <label id="grandineLabel" class="form-label my-0 py-0">Grandine - <span id="grandineText">1.07%</span></label>
          <div class="progress position-relative" style="height: 1.3rem;">
            <div id="Progress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 1.07%; height: 1.25rem;" aria-valuenow="1.07" aria-valuemin="0" aria-valuemax="100"></div>
            <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
          </div>
        </div>
        <div class="my-2">
          <label id="lodestarLabel" class="form-label my-0 py-0">Lodestar - <span id="lodestarText">0.11%</span></label>
          <div class="progress position-relative" style="height: 1.3rem;">
            <div id="lodestarProgress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0.11%; height: 1.25rem;" aria-valuenow="0.11" aria-valuemin="0" aria-valuemax="100"></div>
            <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
          </div>
        </div>
        <div class="my-2">
          <label id="otherLabel" class="form-label my-0 py-0">Other - <span id="otherText">0.02%</span></label>
          <div class="progress position-relative" style="height: 1.3rem;">
            <div id="otherProgress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0.02%; height: 1.25rem;" aria-valuenow="0.02" aria-valuemin="0" aria-valuemax="100"></div>
            <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
            <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="text-center">
      <small>
        Data provided by <a href="https://migalabs.es/api-documentation" target="_blank">Miga Labs</a>. 
        Data may not be 100% accurate. 
        (<a href="/client-fingerprinting">Read more</a>)
      </small>
    </div>
  </div>
</section>

<!-- Why Client Diversity -->
<section id="why" class="bg-light">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Client Diversity Is <u>Not</u> Optional</h2>
    <div class="row justify-content-center mt-4">
      <div class="col col-lg-10">
        <p>Many know client diversity is important for a more resilient network, but they don't understand why or just how important it is. It's not just simply important &#8212; <span class="fw-bold fst-italic">it's critical</span>. If a single client is used by 2/3rd of validators <span id="has66majority" class="d-none text-danger fw-bold text-decoration-underline">(which is currently the case) </span>there's a very real risk this can result in disrupting the chain and monetary loss for node operators.</p>
        <p>It takes 2/3rds of validators to reach finality. If a client with 66%+ of marketshare has a bug and forks to its own chain, it will be capable of finalizing. If the fork finalizes, the <strong>validators cannot return to the real chain without being slashed</strong><!--  or exiting and watching their funds drain while in queue -->. If 66% of the chain gets slashed simultaneously, the penalty is the whole 32 ETH.</p>
        <p>So why is >50% still dangerous? If a minority client forks, the 50%+ majority client can obtain a 66%+ majority. With no client having a marketshare over 33%, these scenarios are avoided. That's why <strong>&#60;33% marketshare is the goal for all clients</strong>.</p>
      </div>
    </div>
    <div class="row justify-content-center mt-2">
      <div class="col col-lg-6 col-md-8 text-center">
        <div class="accordion" id="furtherReading">
          <div class="accordion-item">
            <h2 class="accordion-header" id="furtherReadingHeader">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFurtherReading" aria-expanded="false" aria-controls="collapseFurtherReading">
                Further reading...
              </button>
            </h2>
            <div id="collapseFurtherReading" class="accordion-collapse collapse" aria-labelledby="furtherReadingHeader" data-bs-parent="#furtherReading">
              <div class="accordion-body text-start">
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://medium.com/prysmatic-labs/prysmatic-labs-statement-on-client-diversity-c0e3c2f05671">
                    Prysm: Statement on Client Diversity {{site.data.icons.new_tab}}
                </a>
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://our.status.im/the-importance-of-client-diversity/">
                    Nimbus: The Importance of Client Diversity {{site.data.icons.new_tab}}
                </a>
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://lighthouse.sigmaprime.io/switch-to-lighthouse.html">
                    Lighthouse: Why You Should Switch to Lighthouse {{site.data.icons.new_tab}}
                </a>
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://www.reddit.com/r/ethstaker/comments/ptm04i/the_financial_incentive_to_run_a_minority_client/">
                    The financial incentive to run a minority client {{site.data.icons.new_tab}}
                </a>
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://www.symphonious.net/2021/09/23/what-happens-if-beacon-chain-consensus-fails/">
                    What Happens If Beacon Chain Consensus Fails? {{site.data.icons.new_tab}}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Consensus Clients -->
<section id="clients" class="">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Consensus Clients</h2>
    <div class="row justify-content-center mt-4">
      <div class="col col-lg-8 col-md-10">
        <div class="table-responsive">
          <table class="table table-bordered">
            <thead class="table-light">
              <tr>
                <th scope="col" style="min-width: 8rem;">Client</th>
                <th scope="col">Github</th>
                <th scope="col" style="min-width: 3.8rem;">Docs</th>
                <th scope="col">Discord</th>
                <th scope="col">Support</th>
              </tr>
            </thead>
            <tbody>
              {%- for client in site.data.clients-consensus -%}
                <tr>
                  <th scope="row">
                    {%- if client.name == "Grandine" -%}*{%- endif -%}
                    <a href="{{client.link}}" class="link-dark" target="_blank">
                      {{client.name}}
                      {{site.data.icons.new_tab}}
                    </a>
                  </th>
                  <td>
                    <a href="{{client.github}}" class="text-decoration-none link-dark" target="_blank">
                      {{site.data.icons.github}}
                      {{site.data.icons.new_tab}}
                    </a>
                  </td>
                  <td>
                    <a href="{{client.docs}}" class="text-decoration-none link-dark" target="_blank">
                      {{site.data.icons.docs}}
                      {{site.data.icons.new_tab}}
                    </a>
                  </td>
                  {%- if client.name == "Grandine" -%}
                    <td>(none)</td>
                  {%- else -%}
                    <td>
                      <a href="{{client.discord}}" class="text-decoration-none link-dark" target="_blank">
                        {{site.data.icons.discord}}
                        {{site.data.icons.new_tab}}
                      </a>
                    </td>
                  {%- endif -%}
                  <td>{{client.support}}</td>
                </tr>
              {%- endfor -%}
            </tbody>
          </table>
        </div>
        <div class="text-center">
          <small>* Grandine is not open sourced</small>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Switch Clients -->
<section id="switch" class="bg-light">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Switch Clients</h2>
    <div class="text-center">
      <a href="/" class="btn btn-outline-dark btn-sm px-4 m-1">Submit Guide</a>
    </div>
    <div class="row justify-content-center mt-4">
      <div class="col col-lg-6 col-md-8">
        <div class="input-group mb-3">
          <label class="input-group-text" for="fromSelect">From</label>
          <select class="form-select" id="fromSelect" onchange="preventDoubleClientSelect(this)">
            <!-- <option selected>Choose...</option> -->
            <option value="none" selected disabled hidden>Choose...</option>
            <option value="lighthouse">Lighthouse</option>
            <option value="lodestar">Lodestar</option>
            <option value="nimbus">Nimbus</option>
            <option value="prysm">Prysm</option>
            <option value="teku">Teku</option>
            <option value="grandine">Grandine</option>
          </select>
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col col-lg-6 col-md-8">
        <div class="input-group mb-3">
          <label class="input-group-text" for="toSelect">To</label>
          <select class="form-select" id="toSelect" onchange="preventDoubleClientSelect(this)">
            <!-- <option selected>Choose...</option> -->
            <option value="none" selected disabled hidden>Choose...</option>
            <option value="lighthouse">Lighthouse</option>
            <option value="lodestar">Lodestar</option>
            <option value="nimbus">Nimbus</option>
            <option value="prysm">Prysm</option>
            <option value="teku">Teku</option>
            <option value="grandine">Grandine</option>
          </select>
        </div>
      </div>
    </div>
    <div class="row justify-content-center mt-2">
      <div class="col col-lg-6 col-md-8">
        <div class="text-center">
          <a onclick="getGuides()" class="btn btn-dark btn-lg px-4 m-1">Search Guides</a>
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col col-lg-8 col-md-10">
        <div id="error" class="text-center mt-4 d-none">
          <p class="my-2 text-danger fw-bold">Error: Select both To and From clients.</p>
        </div>
        <div id="migrationPath" class="text-center my-4 d-none">
          <span class="d-block text-muted">
            <span id="fromClient">From Client</span>
            <span class="mx-2">{{site.data.icons.arrow_right}}</span>
            <span id="toClient">To Client</span>
          </span>
        </div>
        <div id="noGuides" class="text-center mt-4 d-none">
          {{site.data.icons.sad_emoji}}
          <p class="my-2">There are no guides for this migration yet.</p>
          <!-- <a href="/" class="btn btn-primary btn-sm px-4 m-1">Submit one for a bounty!</a> -->
        </div>
        <div id="guideList" class="text-center mt-4 d-none">
          <!-- <p class="text-center">
            {{site.data.icons.docs}}
            <a href="">Prysm to Nimbus migration guide, by Paul Harris</a>
            {{site.data.icons.new_tab}}
          </p> -->
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Resources -->
<section id="resources" class="">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Resources</h2>
    <div class="row justify-content-center mt-4">
      <div class="col col-md-3">
        <h5>Tools</h5>
        <ul class="">
          <li class="mb-2">
            <a href="https://stereum.net/" target="_blank" class="p-0 text-muted text-capitalize">Sterneum</a>
          </li>
          <li class="mb-2">
            <a href="https://eth-docker.net/" target="_blank" class="p-0 text-muted text-capitalize">eth-docker</a>
          </li>
          <li class="mb-2">
            <a href="https://github.com/attestantio/vouch" target="_blank" class="p-0 text-muted text-capitalize">Vouch</a>
          </li>
          <li class="mb-2">
            <a href="https://github.com/ethereum/keymanager-APIs" target="_blank" class="p-0 text-muted text-capitalize">keymanager APIs</a>
          </li>
        </ul>
      </div>
      <div class="col col-md-3">
        <h5>Metrics</h5>
        <ul class="">
          <li class="mb-2">
            <a href="https://migalabs.es/crawler/dashboard" target="_blank" class="p-0 text-muted text-capitalize">Miga Labs Dashboard</a>
          </li>
          <li class="mb-2">
            <a href="https://www.nodewatch.io/" target="_blank" class="p-0 text-muted text-capitalize">Chainsafe Nodewatch</a>
          </li>
        </ul>
      </div>
      <div class="col col-md-3">
        <h5>Research</h5>
        <ul class="">
          <li class="mb-2">
            <a href="https://twitter.com/sproulM_/status/1440512518242197516" target="_blank" class="p-0 text-muted text-capitalize">Client Fingerprinting</a>
          </li>
          <li class="mb-2">
            <a href="https://eips.ethereum.org/EIPS/eip-3076" target="_blank" class="p-0 text-muted text-capitalize">EIP-3076: Slashing Protection Interchange Format</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>




