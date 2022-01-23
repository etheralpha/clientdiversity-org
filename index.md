---
layout: default
---


<header class="">
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
  <div class="container ppy-3 my-5">
    <div class="row justify-content-center">
      <div class="col text-center">
        <img src="/assets/img/clients/lighthouse-logo.png" alt="" class="my-2" style="height: 3rem;">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/lodestar-logo-text.png" alt="" class="my-2" style="height: 3rem;">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/prysm-logo.png" alt="" class="my-2" style="height: 3rem;">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/nimbus-logo-text.png" alt="" class="my-2" style="height: 3rem;">
      </div>
      <div class="col text-center">
        <img src="/assets/img/clients/teku-logo.png" alt="" class="my-2" style="height: 3rem;">
      </div>
    </div>
  </div>
</section>

<!-- Client Distribution -->
<section id="distribution" class="">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Client Distribution</h2>
    <div class="row justify-content-center">
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
        Data provided by <a href="https://migalabs.es/api-documentation">Miga Labs</a>. 
        Data may not be 100% accurate. 
        (<a href="/client-fingerprinting">Read more</a>)
        <!-- <svg data-bs-toggle="tooltip" 
            data-bs-placement="top" 
            title=""
            style="margin-top: -5px;" 
            xmlns="http://www.w3.org/2000/svg" 
            width="0.875rem" 
            height="0.875rem" 
            fill="currentColor" 
            class="bi bi-question-circle" 
            viewBox="0 0 16 16">
          <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
          <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z"/>
        </svg> -->
      </small>
    </div>
  </div>
</section>


<!-- Why Client Diversity -->
<section id="why" class="bg-light">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Client Diversity Is <u>Not</u> Optional</h2>
    <div class="text-center">
    </div>
    <div class="row justify-content-center ppx-2">
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    </div>
  </div>
</section>

<!-- Consensus Clients -->
<section id="clients" class="">
  <div class="container py-5 my-5">
    <h3 class="h1 fw-bold mb-3 text-center">Consensus Clients</h3>
    <div class="row justify-content-center mt-4">
      <div class="col col-lg-8 col-md-10">
        <div class="table-responsive">
          <table class="table table-bordered">
            <thead class="table-light">
              <tr>
                <th scope="col" style="min-width: 8rem;">Client</th>
                <th scope="col">Github</th>
                <th scope="col">Docs</th>
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
    <div class="text-center mb-4">
      <a href="/" class="btn btn-outline-dark btn-sm px-4 m-1">Submit Guide</a>
    </div>
    <div class="row justify-content-center">
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
    <div class="row justify-content-center">
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

<!-- Tools and Resources -->
<section id="resources" class="">
  <div class="container py-5 my-5">
    <h2 class="h1 fw-bold mb-3 text-center">Tools and Resources</h2>
    <div class="row justify-content-center">
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    </div>
  </div>
</section>




