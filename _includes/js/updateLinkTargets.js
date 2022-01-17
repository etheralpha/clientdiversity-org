window.onload = updateLinkTargets();

function updateLinkTargets() {
  // open external links and pdfs in new tab
  const links = document.getElementsByTagName("a");
  {%- assign site_url = site.url | split: "//" | last -%}
  for (let link in links) {
    let anchorLink = links[link].href;
    // set all links to open in new tab
    if (/^(https?:)?\/\//.test(links[link].href)) {
      links[link].target = "_blank";
    }
    // if current domain, use same tab
    // if (/^(https?:\/\/rocketpool\.community)/.test(links[link].href)) {
    if (anchorLink != undefined && anchorLink.includes("{{site_url}}")) {
      links[link].target = "_self";
    }
    // open all .pdf, .png, .jpg, .mp4 in new tab
    if (/(\.pdf$|\.png$|\.jpe*g$|\.mp4)/.test(links[link].href)) {
      links[link].target = "_blank";
    }
  }
}