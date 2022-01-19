---
layout: default
---

{%- assign base_site = site.url -%}
  {% if jekyll.environment == "development" %}
    {%- assign base_site = "" -%}
  {%- endif -%}


<header class="px-4 py-5 my-5 text-center">
  <h1 class="display-3 fw-bold mt-5">Diversify Now</h1>
  <div class="col-lg-7 mx-auto">
    <p class="h4 fw-normal mb-4">Improve Etheruem's resiliance by using a minority client</p>
    <!-- <a href="#switch" class="btn btn-outline-dark btn-lg px-4 m-1">Switch Clients</a> -->
    <!-- <a href="#why" class="btn btn-outline-dark btn-lg px-4 m-1">Learn More</a> -->
  </div>
</header>

<!-- Client Distribution -->
<section class="container py-4 mb-5">
  <h2 class="fw-normal mb-3 text-center">Client Distribution</h2>
  <div class="row justify-content-center">
    <div class="col col-lg-6 col-md-8 text-center">
      <p class="">Goal: &#60;33% <span class="mx-2">|</span> Danger: &#62;50%</p>
      <a href="#why" class="text-decoration-none">
        <div class="alert alert-danger d-flex align-items-center" role="alert">
          <svg style="margin-top: -2px;" xmlns="http://www.w3.org/2000/svg" width="1.5rem" height="1.5rem" fill="currentColor" class="bi bi-exclamation-triangle-fill me-2" viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>
          <div>We need to move away from Prysm to minority clients!</div>
        </div>
      </a>
    </div>
  </div>
  <div class="row justify-content-center">
    <div class="col col-lg-6 col-md-8">
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
        <label id="lighthouseLabel" class="form-label my-0 py-0">Lighthouse - <span id="lighthouseText">24.64%</span></label>
        <div class="progress position-relative" style="height: 1.3rem;">
          <div id="lighthouseProgress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 24.64%; height: 1.25rem;" aria-valuenow="24.64" aria-valuemin="0" aria-valuemax="100"></div>
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
        <label id="nimbusLabel" class="form-label my-0 py-0">Nimbus - <span id="nimbusText">5.11%</span></label>
        <div class="progress position-relative" style="height: 1.3rem;">
          <div id="nimbusProgress" class="progress-bar position-absolute bg-success" role="progressbar" style="width: 5.11%; height: 1.25rem;" aria-valuenow="5.11" aria-valuemin="0" aria-valuemax="100"></div>
          <div class="progress-bar bg-trans clientshare-success" role="progressbar" style="width: 33%; height: 1.25rem"></div>
          <div class="progress-bar bg-trans clientshare-warning" role="progressbar" style="width: 17%; height: 1.25rem"></div>
          <div class="progress-bar bg-trans clientshare-danger" role="progressbar" style="width: 50%; height: 1.25rem"></div>
        </div>
      </div>
      <div class="my-2">
        <label id="prysmLabel" class="form-label my-0 py-0"><strong>Prysm - <span id="prysmText">59.47%</span></strong></label>
        <div class="progress position-relative" style="height: 1.3rem;">
          <div id="prysmProgress" class="progress-bar position-absolute bg-danger" role="progressbar" style="width: 59.47%; height: 1.25rem;" aria-valuenow="59.47" aria-valuemin="0" aria-valuemax="100"></div>
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
      (<a href="{{base_site}}/client-fingerprinting">Read more</a>)
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
</section>

<!-- Why Client Diversity -->
<!-- <section id="why" class="container py-4 mb-5">
  <h2 class="fw-normal mb-3 text-center">Client Diversity Is Not Optional</h2>
  <div class="text-center">
  </div>
  <div class="row justify-content-center">

  </div>
</section> -->

<!-- Consensus Clients -->
<section id="clients" class="container py-4 mb-5">
  <h3 class="fw-normal mb-3 text-center">Consensus Clients</h3>
  <div class="row justify-content-center ">
    <div class="col col-lg-8 col-md-10">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Client</th>
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
                <a href="{{client.link}}" class="link-dark" target="_blank">{{client.name}}</a>
              </th>
              <td>
                <a href="{{client.github}}" class="text-decoration-none link-dark" target="_blank">
                  <svg xmlns="http://www.w3.org/2000/svg" width="1.4rem" height="1.4rem" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
                  <svg xmlns="http://www.w3.org/2000/svg" width="0.7rem" height="0.7rem" fill="#555" class="bi bi-box-arrow-up-right" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/><path fill-rule="evenodd" d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/></svg>
                </a>
              </td>
              <td>
                <a href="{{client.docs}}" class="text-decoration-none link-dark" target="_blank">
                  <svg xmlns="http://www.w3.org/2000/svg" width="1.4rem" height="1.4rem" fill="currentColor" class="bi bi-book" viewBox="0 0 16 16"><path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811V2.828zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492V2.687zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783z"/></svg>
                  <svg xmlns="http://www.w3.org/2000/svg" width="0.7rem" height="0.7rem" fill="#555" class="bi bi-box-arrow-up-right" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/><path fill-rule="evenodd" d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/></svg>
                </a>
              </td>
              {%- if client.name == "Grandine" -%}
                <td>(none)</td>
              {%- else -%}
                <td>
                  <a href="{{client.discord}}" class="text-decoration-none link-dark" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="1.4rem" height="1.4rem" fill="currentColor" class="bi bi-discord" viewBox="0 0 16 16"><path d="M13.545 2.907a13.227 13.227 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.19 12.19 0 0 0-3.658 0 8.258 8.258 0 0 0-.412-.833.051.051 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.041.041 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032c.001.014.01.028.021.037a13.276 13.276 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019c.308-.42.582-.863.818-1.329a.05.05 0 0 0-.01-.059.051.051 0 0 0-.018-.011 8.875 8.875 0 0 1-1.248-.595.05.05 0 0 1-.02-.066.051.051 0 0 1 .015-.019c.084-.063.168-.129.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.052.052 0 0 1 .053.007c.08.066.164.132.248.195a.051.051 0 0 1-.004.085 8.254 8.254 0 0 1-1.249.594.05.05 0 0 0-.03.03.052.052 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.235 13.235 0 0 0 4.001-2.02.049.049 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.034.034 0 0 0-.02-.019Zm-8.198 7.307c-.789 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612Zm5.316 0c-.788 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612Z"/></svg>
                    <svg xmlns="http://www.w3.org/2000/svg" width="0.7rem" height="0.7rem" fill="#555" class="bi bi-box-arrow-up-right" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/><path fill-rule="evenodd" d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/></svg>
                  </a>
                </td>
              {%- endif -%}
              <td>{{client.support}}</td>
            </tr>
          {%- endfor -%}
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- Switch Clients -->
<!-- <section id="switch" class="container py-4 mb-5">
  <h2 class="fw-normal mb-3 text-center">Switch Clients</h2>
  <div class="text-center">
  </div>
  <div class="row justify-content-center">

  </div>
</section> -->

<!-- Tools and Resources -->
<!-- <section id="resources" class="container py-4 mb-5">
  <h2 class="fw-normal mb-3 text-center">Tools and Resources</h2>
  <div class="row justify-content-center">

  </div>
</section> -->




