# Carlosrodlop

This Mono-repo aims to be my entry point for daily work. I aim to do everything
as code, creating reusable assets:

* `.docker` Docker containers definition
* `.github/workflow` Actions for
  * [![Push Devops Image](https://github.com/carlosrodlop/carlosrodlop/actions/workflows/docker-buildAndPush-devops.yml/badge.svg)](https://github.com/carlosrodlop/carlosrodlop/actions/workflows/docker-buildAndPush-devops.yml)
  * [![Book to PDF](https://github.com/carlosrodlop/carlosrodlop-docs/actions/workflows/book-to-pdf.yml/badge.svg)](https://github.com/carlosrodlop/carlosrodlop/actions/workflows/book-to-pdf.yml)
  * [![Update Index](https://github.com/carlosrodlop/carlosrodlop-docs/actions/workflows/book-update-index.yaml/badge.svg)](https://github.com/carlosrodlop/carlosrodlop/actions/workflows/book-update-index.yaml)
* `src/gist`  Bucket for snippets of code
* `src/config` (🔒) Configuration of my workstation
  * Containing secrets encrypted via [SOPS](https://github.com/mozilla/sops)
* `src/secrets` (🔒) Secrets Bucket
  * Encrypted via [Git-crypt](https://github.com/AGWA/git-crypt)
  * Vaults: [pass](https://www.passwordstore.org/) and [KeePassX](https://www.keepassx.org/)

[Pre-commit](https://pre-commit.com) is configured to a [set of hooks](https://pre-commit.com/hooks.html)
to validate

* Formatting
* Shellbangs
* Secrets leaks, including <img alt="gitleaks badge" src="https://img.shields.io/badge/protected%20by-gitleaks-blue">
* Ensure not uploading not encrypted [SOPS](https://github.com/mozilla/sops) secrets
