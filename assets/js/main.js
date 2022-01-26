---
---

{% include js/base.js %}
{% include js/clientdistribution.js %}
{% include js/switchclients.js %}
{%- if site.notification_enabled == true -%}
  {% include js/notification.js %}
{%- endif -%}
{% comment %}
  {% include js/lazysizes.min.js %}
{% endcomment %}

// Must be last due to error
{% comment %}
  {% include js/updateLinkTargets.js %}
{% endcomment %}

