---
layout: default
---


<header class="pb-md-3 pb-lg-5 mb-5 mb-md-0">
 <div class="px-4 py-5 my-4 my-md-5 text-center">
    <h1 class="display-1 fw-bold mt-5">Diversify Now</h1>
    <div class="col-lg-7 mx-auto">
      <p class="h4 fw-normal mb-4">Improve Ethereum's resilience by using a minority client</p>
      <a href="#switch" class="btn btn-dark btn-lg px-4 m-1">Switch Clients</a>
      <a href="#why" class="btn btn-outline-dark btn-lg px-4 m-1">Learn More</a>
    </div>
  </div>
</header>

<!-- Logos -->
<section class="bg-light">
  <div class="container my-5">
    <div class="row text-center">
      <div class="col">
        <img src="/assets/img/consensus-clients/lighthouse-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/consensus-clients/lodestar-logo-text.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/consensus-clients/prysm-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/consensus-clients/nimbus-logo-text.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/consensus-clients/teku-logo.png" alt="" class="my-2 client-logos">
      </div>
    </div>
    <div class="row text-center mt-2 d-none d-lg-flex">
      <div class="col">
        <img src="/assets/img/execution-clients/besu-text-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/execution-clients/nethermind-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/execution-clients/erigon-text-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/execution-clients/open-ethereum-text-logo.png" alt="" class="my-2 client-logos">
      </div>
      <div class="col">
        <img src="/assets/img/execution-clients/geth-logo.png" alt="" class="my-2 client-logos">
      </div>
    </div>
  </div>
</section>

<!-- Client Distribution -->
<section id="distribution" class="">
  <div class="container py-5 my-5">
    <div class="text-center mb-5">
      <h2 class="h1 fw-bold mb-2 text-center">Client Distribution</h2>
      <a href="https://pools.invis.cloud/" target="_blank" class="btn btn-dark mt-2 mb-3">View Staking Pool Diversity</a>
      <p class="lead">Goal: &#60;33% <span class="mx-2">|</span> Danger: &#62;50%</p>
    </div>
    <div class="row justify-content-evenly">
      <div class="col-12 col-xl-5 col-lg-6 col-md-8 col-sm-12 text-center">
        <div class="card h-100 rounded-3 p-0 p-lg-2">
          <div class="card-body d-flex flex-column p-4">
            <h3 class="p-2 mb-4">Consensus Clients</h3>
            <div id="marketshareAlertsCC">
              <a id="marketshareWarningMigaLabs" href="#why" class="d-none text-decoration-none">
                <div class="alert alert-danger d-flex align-items-center" role="alert">
                  {{site.data.icons.warning}}
                  <div>Switch from <span id="dangerClientsMigaLabs">Prysm</span> to a minority client!</div>
                </div>
              </a>
              <a id="marketshareSuccessCC" href="#why" class="d-none text-decoration-none">
                <div class="alert alert-info d-flex align-items-center" role="alert">
                  {{site.data.icons.info}}
                  <div class="ms-2">The consensus client diversity has improved!</div>
                </div>
              </a>
              <a id="marketshareWarningBlockprint" href="#why" class="d-none text-decoration-none">
                <div class="alert alert-danger d-flex align-items-center" role="alert">
                  {{site.data.icons.warning}}
                  <div>Switch from <span id="dangerClientsBlockprint">Prysm</span> to a minority client!</div>
                </div>
              </a>
            </div>
            <div id="distributionMigaLabs" class="text-start flex-grow-1">
              <div id="distributionBarsMigaLabs">
                <div class="my-2">
                  <label class="form-label my-0 py-0 fw-bold">Prysm - 55.19%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-danger" role="progressbar" style="width: 55.19%; height: 1.25rem;" aria-valuenow="55.19" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Lighthouse - 29.77%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 29.77%; height: 1.25rem;" aria-valuenow="29.77" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Teku - 8.88%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 8.88%; height: 1.25rem;" aria-valuenow="8.88" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Nimbus - 4.65%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 4.65%; height: 1.25rem;" aria-valuenow="4.65" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Grandine - 1.22%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 1.22%; height: 1.25rem;" aria-valuenow="1.22" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Lodestar - 0.2%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0.2%; height: 1.25rem;" aria-valuenow="0.2" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Other - 0.1%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0.1%; height: 1.25rem;" aria-valuenow="0.1" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
              </div>
              <div class="text-center small">
                Data provided by <a href="https://migalabs.es/api-documentation" target="_blank">Miga Labs</a> — updated daily. <br>
                Data may not be 100% accurate. (<a href="/client-fingerprinting">Read more</a>)
              </div>
            </div>
            <div id="distributionBlockprint" class="d-none text-start">
              <div id="distributionBarsBlockprint">
                <div class="my-2">
                  <label class="form-label my-0 py-0 fw-bold">Prysm - 54.64%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-danger" role="progressbar" style="width: 54.64%; height: 1.25rem;" aria-valuenow="54.64" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Lighthouse - 25.48%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 25.48%; height: 1.25rem;" aria-valuenow="25.48" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Teku - 17.86%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 17.86%; height: 1.25rem;" aria-valuenow="17.86" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Nimbus - 2.03%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 2.03%; height: 1.25rem;" aria-valuenow="2.03" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Lodestar - 0%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0%; height: 1.25rem;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Undefined - 0%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0%; height: 1.25rem;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Other - 0%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0%; height: 1.25rem;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
              </div>
              <div class="text-center small">
                Data provided by <a href="https://github.com/sigp/blockprint/blob/main/docs/api.md" target="_blank">Sigma Prime's Blockprint</a> — updated daily. <br>
                Data may not be 100% accurate. (<a href="/client-fingerprinting">Read more</a>)
              </div>
            </div>
            <div id="dataSourceOptionsCC" class="mt-4 text-start text-sm-center">
              <div class="alert alert-info" role="alert">
                <div class="me-2 fw-bold">
                  <span>Data source </span>
                  <a href="/client-fingerprinting" style="color: #055160;">(read more)</a>:
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" name="datasourcesCC" id="dataSource1" value="migalabs"  onclick="setDataSources();" checked>
                  <label class="form-check-label" for="dataSource1">Miga Labs</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" name="datasourcesCC" id="dataSource2" value="blockprint"  onclick="setDataSources();">
                  <label class="form-check-label" for="dataSource2">Sigma Prime's Blockprint</label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-xl-5 col-lg-6 col-md-8 col-sm-12 mt-5 pt-3 mt-lg-0 pt-lg-0 text-center d-flex flex-column">
        <div class="card h-100 rounded-3 p-0 p-lg-2">
          <div class="card-body d-flex flex-column p-4">
            <h3 class="p-2 mb-4">Execution Clients</h3>
            <div id="marketshareAlertsEC">
              <a id="marketshareWarningEthernodes" href="#why" class="text-decoration-none">
                <div class="alert alert-danger d-flex align-items-center" role="alert">
                  {{site.data.icons.warning}}
                  <div>Switch from <span id="dangerClientsEthernodes">Geth</span> to a minority client!</div>
                </div>
              </a>
              <a id="marketshareSuccessEC" href="#why" class="d-none text-decoration-none">
                <div class="alert alert-info d-flex align-items-center" role="alert">
                  {{site.data.icons.info}}
                  <div class="ms-2">The consensus client diversity has improved!</div>
                </div>
              </a>
            </div>
            <div id="distributionEthernodes" class="text-start flex-grow-1">
              <div id="distributionBarsEthernodes">
                <div class="my-2">
                  <label class="form-label my-0 py-0 fw-bold">Geth - 85.58%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-danger" role="progressbar" style="width: 85.58%; height: 1.25rem;" aria-valuenow="85.58" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Open Ethereum - 6.42%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 6.42%; height: 1.25rem;" aria-valuenow="6.42" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Erigon - 5.95%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 5.95%; height: 1.25rem;" aria-valuenow="5.95" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Nethermind - 1.23%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 1.23%; height: 1.25rem;" aria-valuenow="1.23" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Besu - 0.62%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0.62%; height: 1.25rem;" aria-valuenow="0.62" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
                <div class="my-2">
                  <label class="form-label my-0 py-0">Others - 0.19%</label>
                  <div class="progress position-relative" style="height: 1.3rem;">
                    <div class="progress-bar position-absolute bg-success" role="progressbar" style="width: 0.19%; height: 1.25rem;" aria-valuenow="0.19" aria-valuemin="0" aria-valuemax="100"></div>
                    <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
                    <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
                  </div>
                </div>
              </div>
              <div class="text-center small">
                Data provided by <a href="https://ethernodes.org" target="_blank">Ethernodes</a> — updated daily. <br>
                Data may not be 100% accurate. (<a href="/client-fingerprinting">Read more</a>)
              </div>
            </div>
            <div id="dataSourceOptionsEC" class="mt-4 text-start text-sm-center">
              <div class="alert alert-info" role="alert">
                <div class="me-2 fw-bold">Data source:</div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" name="datasourcesEC" id="dataSourceEC1" value="ethernodes"  onclick="setDataSources();" checked>
                  <label class="form-check-label" for="dataSource1">Ethernodes</label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Why Client Diversity -->
<section id="why" class="bg-light">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Client Diversity Is <u>Not</u> Optional</h2>
    <div class="row justify-content-center mt-4">
      <div class="col col-lg-10">
        <p class="mb-4">Many know client diversity is important for a more resilient network, but they don't understand why or just how essential it is. It's not only important &#8212; <span class="fw-bold fst-italic">it's critical</span>. If a single client is used by 2/3rds (66%) of validators <span id="extremeMajorityMsgMigaLabs" class="d-none text-danger fw-bold text-decoration-underline">(this is currently the case) </span><span id="extremeMajorityMsgBlockprint" class="d-none text-danger fw-bold text-decoration-underline">(this is currently the case) </span>there's a very real risk this can result in disrupting the chain and monetary loss [<a href="https://www.slashed.info/" target="_blank">1</a>, <a href="https://twitter.com/_crypto_crack/status/1504459918539120643" target="_blank">2</a>] for node operators.</p>
        <p class="mb-4">It takes 2/3rds of validators to reach finality. If a client with 66%+ of marketshare has a bug and forks to its own chain, it'll be capable of finalizing. Once the fork finalizes, the <strong>validators cannot return to the real chain without being slashed</strong><!--  or exiting and watching their funds drain while in queue -->. If 66% of the chain gets slashed simultaneously, the penalty is the whole 32 ETH.</p>
        <p class="mb-4">So why is >50% marketshare still dangerous? <span id="majorityMsgMigaLabs" class="d-none text-danger fw-bold text-decoration-underline">(this is currently the case)</span><span id="majorityMsgBlockprint" class="d-none text-danger fw-bold text-decoration-underline">(this is currently the case)</span> If a minority client forks, the 50%+ majority client can obtain a 66%+ majority. With no client having a marketshare over 33%, these scenarios are avoided. That's why <strong>&#60;33% marketshare is the goal for all clients</strong>.</p>
        <p><strong>Execution clients are not immune.</strong> The risks mentioned above apply to both consensus clients and execution clients equally.</p>
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
                    href="https://mirror.xyz/jmcook.eth/S7ONEka_0RgtKTZ3-dakPmAHQNPvuj15nh0YGKPFriA">
                    Client diversity on Ethereum’s consensus layer {{site.data.icons.new_tab}}
                </a>
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
                    href="https://medium.com/chainsafe-systems/on-client-diversity-in-decentralized-networks-848aeedfb49d">
                    Chainsafe: Client Diversity in Decentralized Networks {{site.data.icons.new_tab}}
                </a>
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://www.reddit.com/r/ethstaker/comments/ptm04i/the_financial_incentive_to_run_a_minority_client/">
                    The financial incentive to run a minority client {{site.data.icons.new_tab}}
                </a>
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://www.symphonious.net/2021/09/23/what-happens-if-beacon-chain-consensus-fails/">
                    What Happens If Beacon Chain Consensus Fails? {{site.data.icons.new_tab}}
                </a>
                <a class="d-block my-2 link-dark text-capitalize" target="_blank"
                    href="https://upgrading-ethereum.info/altair/part2/incentives/diversity">
                    Ben Edgington on diversity, scenarios, and penalties {{site.data.icons.new_tab}}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Client Resources -->
<section id="clients" class="">
  <div class="container py-5 my-5">
    <div class="text-center mb-5">
      <h2 class="h1 fw-bold mb-2">Client Resources</h2>
    </div>
    <div class="row justify-content-evenly mt-4">
      <div class="col col-xxl-8 col-xl-9 col-lg-10 col-md-11 ttext-center">
        <h3 class="mb-3">Consensus Clients</h3>
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
                  {%- if client.github -%}
                    <td>
                      <a href="{{client.github}}" class="text-decoration-none link-dark" target="_blank">
                        {{site.data.icons.github}}
                        {{site.data.icons.new_tab}}
                      </a>
                    </td>
                  {%- else -%}
                    <td>(none)</td>
                  {%- endif -%}
                  {%- if client.docs -%}
                    <td>
                      <a href="{{client.docs}}" class="text-decoration-none link-dark" target="_blank">
                        {{site.data.icons.docs}}
                        {{site.data.icons.new_tab}}
                      </a>
                    </td>
                  {%- else -%}
                    <td>(none)</td>
                  {%- endif -%}
                  {%- if client.discord -%}
                    <td>
                      <a href="{{client.discord}}" class="text-decoration-none link-dark" target="_blank">
                        {{site.data.icons.discord}}
                        {{site.data.icons.new_tab}}
                      </a>
                    </td>
                  {%- else -%}
                    <td>(none)</td>
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
      <div class="col col-xxl-8 col-xl-9 col-lg-10 col-md-11 ttext-center mt-5 ppt-3 mmt-md-0 ppt-md-0">
        <h3 class="mb-3">Execution Clients</h3>
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
              {%- for client in site.data.clients-execution -%}
                <tr>
                  <th scope="row">
                    {%- if client.name == "OpenEthereum" -%}*{%- endif -%}
                    <a href="{{client.link}}" class="link-dark" target="_blank">
                      {{client.name}}
                      {{site.data.icons.new_tab}}
                    </a>
                  </th>
                  {%- if client.github -%}
                    <td>
                      <a href="{{client.github}}" class="text-decoration-none link-dark" target="_blank">
                        {{site.data.icons.github}}
                        {{site.data.icons.new_tab}}
                      </a>
                    </td>
                  {%- else -%}
                    <td>(none)</td>
                  {%- endif -%}
                  {%- if client.docs -%}
                    <td>
                      <a href="{{client.docs}}" class="text-decoration-none link-dark" target="_blank">
                        {{site.data.icons.docs}}
                        {{site.data.icons.new_tab}}
                      </a>
                    </td>
                  {%- else -%}
                    <td>(none)</td>
                  {%- endif -%}
                  {%- if client.discord -%}
                    <td>
                      <a href="{{client.discord}}" class="text-decoration-none link-dark" target="_blank">
                        {{site.data.icons.discord}}
                        {{site.data.icons.new_tab}}
                      </a>
                    </td>
                  {%- else -%}
                    <td>(none)</td>
                  {%- endif -%}
                  <td>{{client.support}}</td>
                </tr>
              {%- endfor -%}
            </tbody>
          </table>
        </div>
        <div class="text-center">
          <small>* OpenEthereum is deprecated</small>
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
      <a href="/contribute/" class="btn btn-outline-dark btn-sm px-4 m-1">Submit Guide</a>
    </div>
    <div class="row justify-content-center mt-4">
      <div class="col col-lg-6 col-md-8">
        <div class="input-group mb-3">
          <label class="input-group-text" for="typeSelect">Type</label>
          <select class="form-select" id="typeSelect" onchange="setSwitchType()">
            <option value="consensus" selected>Consensus Client</option>
            <option value="execution">Execution Client</option>
            <!-- <option value="execution" disabled>Execution Client (coming soon&#8482;)</option> -->
          </select>
        </div>
      </div>
    </div>
    <!-- Consensus Clients - From -->
    <div id="switchFromConsensus" class="row justify-content-center mt-3">
      <div class="col col-lg-6 col-md-8">
        <div class="input-group mb-3">
          <label class="input-group-text" for="fromSelectCC">From</label>
          <select class="form-select" id="fromSelectCC" onchange="preventDoubleClientSelect('fromSelect')">
            <option value="none" selected disabled hidden>Choose...</option>
            <option value="blank">Fresh Install</option>
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
    <!-- Consensus Clients - To -->
    <div id="switchToConsensus" class="row justify-content-center">
      <div class="col col-lg-6 col-md-8">
        <div class="input-group mb-3">
          <label class="input-group-text" for="toSelectCC">To</label>
          <select class="form-select" id="toSelectCC" onchange="preventDoubleClientSelect('toSelect')">
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
    <!-- Execution Clients - From -->
    <div id="switchFromExecution" class="d-none row justify-content-center mt-3">
      <div class="col col-lg-6 col-md-8">
        <div class="input-group mb-3">
          <label class="input-group-text" for="fromSelectEC">From</label>
          <select class="form-select" id="fromSelectEC" onchange="preventDoubleClientSelect('fromSelect')">
            <option value="none" disabled hidden>Choose...</option>
            <option value="blank">Fresh Install</option>
            <option value="geth" selected>Geth</option>
            <option value="openethereum">Open Ethereum</option>
            <option value="erigon">Erigon</option>
            <option value="nethermind">Nethermind</option>
            <option value="besu">Besu</option>
          </select>
        </div>
      </div>
    </div>
    <!-- Execution Clients - To -->
    <div id="switchToExecution" class="d-none row justify-content-center">
      <div class="col col-lg-6 col-md-8">
        <div class="input-group mb-3">
          <label class="input-group-text" for="toSelectEC">To</label>
          <select class="form-select" id="toSelectEC" onchange="preventDoubleClientSelect('toSelect')">
            <option value="none" selected disabled hidden>Choose...</option>
            <option value="geth">Geth</option>
            <option value="openethereum" disabled>Open Ethereum (deprecated)</option>
            <option value="erigon">Erigon</option>
            <option value="nethermind">Nethermind</option>
            <option value="besu">Besu</option>
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
          <!-- <a href="/contribute/" class="btn btn-primary btn-sm px-4 m-1">Submit one for a bounty!</a> -->
          <a href="/contribute/" class="btn btn-primary btn-sm px-4 m-1">Submit Guide</a>
        </div>
        <div id="guideList" class="text-center mt-4 d-none">
          <!-- Populated w/ JS based on matching results from _data/migration-guides.yml -->
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Resources -->
<section id="resources" class="">
  <div class="container py-5 my-5 px-4">
    <h2 class="h1 fw-bold mb-3 text-center">Resources</h2>
    <div class="row justify-content-start justify-content-lg-center mt-4">
      <div class="col-12 col-sm-6 col-lg-4 col-xl-3 mt-4">
        <h5>Tools</h5>
        <ul class="">
          <li class="mb-2">
            <a href="https://stereum.net/" target="_blank" class="p-0 text-muted text-capitalize">Stereum</a>
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
      <div class="col-12 col-sm-6 col-lg-4 col-xl-3 mt-4">
        <h5>Metrics</h5>
        <ul class="">
          <li class="mb-2">
            <a href="https://pools.invis.cloud/" target="_blank" class="p-0 text-muted text-capitalize">Staking Pool Client Diversity</a>
          </li>
          <li class="mb-2">
            <a href="https://migalabs.es/crawler/dashboard" target="_blank" class="p-0 text-muted text-capitalize">Miga Labs Dashboard</a>
          </li>
          <li class="mb-2">
            <a href="https://www.nodewatch.io/" target="_blank" class="p-0 text-muted text-capitalize">Chainsafe Nodewatch</a>
          </li>
          <li class="mb-2">
            <a href="https://github.com/sigp/blockprint/blob/main/docs/api.md" target="_blank" class="p-0 text-muted text-capitalize">Proposer Diversity Data</a>
          </li>
          <li class="mb-2">
            <a href="https://www.rated.network/" target="_blank" class="p-0 text-muted text-capitalize">Rated.Network Validator Ratings</a>
          </li>
          <li class="mb-2">
            <a href="https://www.slashed.info/" target="_blank" class="p-0 text-muted text-capitalize">Financial Risk Per Consensus Client</a>
          </li>
        </ul>
      </div>
      <div class="col-12 col-sm-6 col-lg-4 col-xl-3 mt-4">
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

