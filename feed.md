---
layout: default
permalink: /feed/
---


<header class="container py-4 mt-5">
  <div class="text-center">
    <h1 class="display-6 fw-bold mb-3">Feed</h1>
    <p class="col-md-10 col-lg-8 mx-auto lead">
      Client diversity news and developments.
    </p>
    <a href="/contribute/" class="btn btn-outline-dark btn-lg px-4 m-1">Submit Link</a>
  </div>
</header>

<section class="container py-4">
  {%- for news in site.data.feed -%}
    <div class="row justify-content-center">
        <div class="col col-lg-6 col-md-8">
          <div class="card mb-3 rounded-3">
            <div class="card-body">
              <p class="card-subtitle mb-1">
                <small class="text-muted">{{news.date}}</small>
              </p>
              <div class="d-inline me-2" style="margin-top: -0.32rem">
                {%- if news.link contains "twitter.com" -%}
                  <span class="text-primary">{{site.data.icons.twitter}}</span>
                {%- elsif news.link contains "youtube.com" or news.link contains "youtu.be" -%}
                  <span class="text-danger">{{site.data.icons.video}}</span>
                {%- elsif news.link contains "reddit.com" -%}
                  <span style="color: #ff4500;">{{site.data.icons.reddit}}</span>
                {%- elsif news.link contains "github.com" -%}
                  <span class="text-dark">{{site.data.icons.github}}</span>
                {%- else -%}
                  <span class="text-secondary">{{site.data.icons.web}}</span>
                {%- endif -%}
              </div>
              <a href="{{news.link}}" target="_blank">{{news.title}}</a>
            </div>
          </div>
        </div>
    </div>
  {%- endfor -%}
</section>