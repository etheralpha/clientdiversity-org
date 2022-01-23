---
layout: default
permalink: /feed/

header: 404
---


<header class="container py-4 mt-5">
  <div class="text-center">
    <h1 class="display-6 fw-bold mb-3">Feed</h1>
    <p class="col-md-10 col-lg-8 mx-auto lead">
      Client diversity news and developments.
    </p>
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
              <span class="me-2" style="margin-top:-15px;">
                {%- if news.link contains "twitter.com" -%}
                  {{site.data.icons.twitter}}
                {%- elsif news.link contains "youtube.com" or news.link contains "youtu.be" -%}
                  {{site.data.icons.video}}
                {%- elsif news.link contains "reddit.com" -%}
                  {{site.data.icons.reddit}}
                {%- elsif news.link contains "github.com" -%}
                  {{site.data.icons.github}}
                {%- else -%}
                  {{site.data.icons.web}}
                {%- endif -%}
              </span>
              <a href="{{news.link}}" target="_blank">{{news.title}}</a>
            </div>
          </div>
        </div>
    </div>
  {%- endfor -%}
</section>