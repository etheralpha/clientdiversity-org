# clientdiversity-org

This is the repo for <https://clientdiversity.org>, a resource site to assist client diversity efforts. This project is maintained by [Ether Alpha](https://etheralpha.org/).

## Local Setup

### Just Using Jekyll

1. Clone the repo (or fork the repo to your account)
1. Install dependencies: `bundle install`
1. Create a feature branch off of the latest version branch
1. Start the local server: `bundle exec jekyll serve`
1. Go to <http://localhost:4000/> to view changes

To build the site use `bundle exec jekyll build`. 


Resources:

- [Jekyll Docs](https://jekyllrb.com/docs/)
- [Liquid Syntax](https://shopify.github.io/liquid/basics/introduction/)

## Updating Content

- Client resources: `_data/clients-consensus.yml` and `_data/clients-execution.yml`
- Client guides: `_data/consensus-migration-guides.yml` and `_data/execution-migration-guides.yml`
- Rest of the content is within `index.md` as raw html
