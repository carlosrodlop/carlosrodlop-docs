# CloudBees CI Admin Hero

<p align="center">
  <img alt="admin-hero-icon" src="https://www.jenkins.io/images/logos/jenkins-is-the-way/jenkins-is-the-way.png" height="160" />
  <p align="center">This track is orientated to the CI <strong>Admin</strong> rol</p>
</p>

---

![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)

Inspired by [CloudBees CI feature comparison](https://docs.cloudbees.com/docs/cloudbees-ci/latest/feature-definition) and completed with my experience in the field and awesome content (from awesome people) public on the Internet.

Technology integration choices here cover the most common use cases based on the [Jenkins Stats](https://stats.jenkins.io/) but more integrations are available via plugins.

This guide needs to be read from the top to the bottom: CloudBees CI is built on top of Jenkins.

Check out my GitHub start repositories for [CloudBees CI Admin](https://github.com/stars/carlosrodlop/lists/jenkins-cbci-admin).

## Jenkins: Starting with a solid Open Source core

* Jenkins is an open source automation server. It helps automate the parts of SDLF, facilitating CI and CD [check in Wikipedia](https://en.wikipedia.org/wiki/Jenkins_(software)).
* Spot Jenkins inside the [CD Landscape Map](https://landscape.cd.foundation/)
* Get a first look at the Jenkins UI accessing the instance [jenkins.io](https://ci.jenkins.io/) as a Guest. Jenkins uses Jenkins for the CI of their plugins and core ("Dogfooding").

### Jenkins: Installation and Architecture

* High level overview of the [Jenkins architecture](https://www.jenkins.io/doc/developer/architecture/)
* [Install Jenkins](https://www.jenkins.io/doc/book/installing/) in your desired platform following the recommendations explained in [Prepare Jenkins for Support](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/best-practices/prepare-jenkins-for-support)
* Always install the latest available version. It is a good practice to review [LTS Changelog](https://www.jenkins.io/changelog-stable/) to understand the new features and bug fixes (specifically for upgrades)
* Additional [Jenkins Features are controlled with System Properties](https://www.jenkins.io/doc/book/managing/system-properties/).
* Capacity planning: How many Jenkins instances does my Organization needs to perform efficiently their CI pipelines?
  * Number of Controllers: Generally speaking, **one per Development Team**. Additionally. there are references to **estimate number of controllers** based on the [number of jobs and developers](https://www.jenkins.io/doc/book/scaling/architecting-for-scale/#Calculating-how-many-jobs)
    * [🎥 Big Monolithic Controllers are performance killers](https://www.cloudbees.com/videos/splitting-monolithic-jenkins-controllers-for-increased-performance). Check this [Guide to Slipt Controllers](https://docs.cloudbees.com/docs/cloudbees-ci-migration/latest/splitting-controllers/)
  * Compute resources per Controller Node:
    * [Minumum requirements](https://docs.cloudbees.com/docs/cloudbees-ci/latest/traditional-install-guide/system-requirements)
    * [Memory max up to 16GB](https://docs.cloudbees.com/docs/admin-resources/latest/jvm-troubleshooting/#_heap_size)
    * [4 CPU unit is a good number for production](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-reference-architecture/ra-for-eks/#_controller_sizing_guidelines)
    * [Scalable Storage](https://www.jenkins.io/doc/book/scaling/architecting-for-scale/#scalable-storage-for-master) strating by 50 GB ( 🍬 For Kubernetes add [`allowVolumeExpansion: true`](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/cloudbees-ci-on-modern-cloud-platforms/how-to-expand-a-pvc-on-cloudbees-ci) and `volumeBindingMode: WaitForFirstConsumer` (for Nodes using multi AZs - recommended) to the Storage Classes).
* Network Requirements
  * [Ports and Proxy configuration](https://docs.cloudbees.com/docs/cloudbees-ci/latest/traditional-secure-guide/configuring-network-requirements)
  * Firewall: [Required URLs to allowlist](https://docs.cloudbees.com/docs/cloudbees-ci/latest/traditional-secure-guide/url-list) (Note some of the URL are only required for CloudBees)
  * Running Jenkins on Private Subnets: Use software Agent for inbound SCM webhooks.
    * [🎥 Smee.io](https://www.youtube.com/watch?v=ULe7c-2aPYY)
    * [Webhookrelay](https://webhookrelay.com/blog/2017/11/23/github-jenkins-guide/)
  * For your [Agents Nodes design](https://www.jenkins.io/doc/book/managing/nodes/), use [Websockets](https://www.jenkins.io/blog/2020/02/02/web-socket/) for the in-bound types to connect via via HTTPS.

### Jenkins: Data Persistence

Jenkins depends on a Fyle System to store its configuration and build data: [$JENKINS_HOME](https://docs.cloudbees.com/docs/admin-resources/latest/backup-restore/jenkins-home)
Nevertheless, some of it outcomes can be storage outside of the Filesystem see [Pluggable Storage](https://www.jenkins.io/sigs/cloud-native/pluggable-storage/)

### Jenkins: Configuration

* Configuration as Code: Explore [JCasc](https://github.com/jenkinsci/configuration-as-code-plugin), and pay special attention to the [Handling secrets](https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/secrets.adoc) and the [Exporting configuration tool](https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/configExport.md) sections.
* Plugins Management: Jenkins comes with a series of bundle plugins (required) but its capabilities can be extended via [Manage Plugins](https://www.jenkins.io/doc/book/managing/plugins/). There are more than 1800+ community-contributed plugins (see [Jenkins Plugins Index](https://plugins.jenkins.io/)).
  * ⚠️ Note that [Advanced installation](https://www.jenkins.io/doc/book/managing/plugins/#advanced-installation) does manage transitive dependencies requirements.
  * Air-gapped environments: The [plugin manager tools](https://github.com/jenkinsci/plugin-installation-manager-tool) downloads plugins and their dependencies into a folder so that they can be easily imported into an instance of Jenkins.
* Prepare the instance to onboard developers:
  * 🔑 Add [Credentials](https://www.jenkins.io/doc/book/using/using-credentials/) to the Jenkins Internal Store to connect to your third-party systems (Security Realm, SCM, Artifactory Registry). Check out that you [understand different scopes](https://github.com/jenkinsci/credentials-plugin/blob/master/docs/user.adoc#credentials-scopes).
  * 🔒 Define Jenkins [Access Control](https://www.jenkins.io/doc/book/security/managing-security/#access-control). Among the different options, the most common setup would be:  
    * Configuring [LDAP](https://plugins.jenkins.io/ldap/) plugin for `Security Realm` (🍬 ensure [tuning](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/troubleshooting-guides/the-log-in-with-ldap-plugin-is-very-slow) is enabled)
    * Configuring [Matrix Authorization Strategy](https://plugins.jenkins.io/matrix-auth/) plugin as `Authorization Strategy` for your projects.
  * :octocat: Integrate with [GitHub](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-and-managed-masters/github-webhook-configuration) as SCM via WebHook (🍬 review additional [Best Practices for SCM](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/best-practices/scm-best-practices))
  * [Configure Agents](https://www.jenkins.io/doc/book/managing/nodes/#managing-nodes) to perform your builds (🍬 check [best practices](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/best-practices/remoting-best-practices)
    * Jenkins supports different types of OS (Windows, Linux and MacOS) and deployments [Static Agents](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/agents#static-agents) vs Cloud [Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/))
  * Integrate with an Artifact Registry like [Artifactory](https://plugins.jenkins.io/artifactory/) to store artifacts (build outcome) for Continuos Delivery or Release Orchestration
    * ⚠️ For intermediate artifacts to be used by others Jenkins builds (e.g. [archiveArtifacts](https://www.jenkins.io/doc/pipeline/steps/core/#archiveartifacts-archive-the-artifacts)), do not use `$JENKINS_HOME` but S3 compatible storage like [Artifact Manager on S3](https://plugins.jenkins.io/artifact-manager-s3/)
* Housekeeping: [Configure Global Build Discarders](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/best-practices/deleting-old-builds-best-strategy-for-cleanup-and-disk-space-management#_resolution) helps to reduce the **disk space** consumption on build data for jobs ([🎥 How to Clean up Old Jenkins Builds](https://www.youtube.com/watch?v=_Z7BlaTTGlo))
  * 🍬 Build data consume more Disk space and has higher IO rates that the rest of the elements outside the `$JENKINS_HOME`. Why do not place it a more appropiate disk according to its requirements outside the `$JENKINS_HOME` thanks to [jenkins.model.Jenkins.buildsDir](https://www.jenkins.io/doc/book/managing/system-properties/#jenkins-model-jenkins-buildsdir)?

### Jenkins: Administration

* 📈 Observability:
  * By default, the [Metrics](https://plugins.jenkins.io/metrics/) plugin exposes a set of metrics including  System and Java Virtual Machine metrics, Web UI metrics and Jenkins-specific metrics. Other plugins might add additional metrics like the [CloudBees Disk Usage Simple](https://plugins.jenkins.io/cloudbees-disk-usage-simple/)
    * Recommended resources to watch for performance: memory usage percentage, CPU usage percentage, JENKINS_HOME disk usage percentage, JENKINS_HOME IOPS, operations center and managed controller response time, Remaining build nodes capacity, Remaining master nodes capacity and Build/master nodes instances usage.
    * Integrate Jenkins with an external solution like [🎥 Prometheus and Graphana](https://www.youtube.com/watch?v=3H9eNIf9KZs). (⚠️ Using [Monitoring plugin](https://plugins.jenkins.io/monitoring/) for production environment is not a good approach because Jenkins is being monitored inside Jenkins).
      * 🍬 Grafana offers series of ready-built [dashboards for Jenkins](https://grafana.com/grafana/dashboards/?search=jenkins)
      * 🍬 Must-have alerts for Jenkins can be found at [Awesome Prometheus alerts](https://samber.github.io/awesome-prometheus-alerts/rules#jenkins)
  * Identifying where are the pipeline bottlenecks by [🎥 Tracing Your Jenkins Pipelines With OpenTelemetry and Jaeger](https://www.youtube.com/watch?v=3XzVOxvNpGM) (Additionally [Troubleshooting Slow Builds](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/troubleshooting-guides/how-to-identify-cause-for-building-times-increase)).
* 🔬 Auditing:
  * [Audit Trail Plugin](https://plugins.jenkins.io/audit-trail/). More info at [How does Audit Trail plugin work](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-d-managed-masters/how-does-audit-trail-plugin-work).
  * [Job Config History Plugin](https://plugins.jenkins.io/jobConfigHistory/) (⚠️ This plugin can become a performance killer if you do not follow the recommendations provided in [JobConfigHistory Plugin Best Practices](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/best-practices/jobconfighistory-best-practices)). GitOps using JCasc is a better approach.
* 💾 [Backup/Restore](https://www.jenkins.io/doc/book/system-administration/backing-up/)
  * [Thinbackup plugin](https://plugins.jenkins.io/thinBackup/) for process automation.
    * Backup storage: Directory/Mount point accessible from `$JENKINS_HOME`
    * Currently, it is no integrated in JCasc [JENKINS-53442](https://issues.jenkins.io/browse/JENKINS-53442)
* Operate remotely with Jenkins
  * [Jenkins CLI](https://www.jenkins.io/doc/book/managing/cli/) (🍬 If you use the Jenkins CLI tool regularly, [configure an alias](https://docs.cloudbees.com/docs/admin-resources/latest/cli-guide/config-alias) to avoid having to type the entire command each time).
    * `$JENKINS_URL/cli` contains up-to-date docs about remoting cli commands.
  * [REST API](https://www.jenkins.io/doc/book/using/remote-access-api/) (⚠️ Jenkins REST API should [never be used without the tree parameter](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/best-practices/best-practice-for-using-jenkins-rest-api)).
    * `$JENKINS_URL/api` contains up-to-date docs about remoting API REST.
* Automate management via Groovy code running into the [Script Console](https://www.jenkins.io/doc/book/managing/script-console/) (🍬 [Write Groovy scripts for Jenkins with code completion](https://www.mdoninger.de/2011/11/07/write-groovy-scripts-for-jenkins-with-code-completion.html))
  * Check API on [Jenkins Core and Plugins Javadoc](https://javadoc.jenkins.io/)
  * [Learn by examples](https://www.jenkins.io/doc/book/managing/script-console/#example-groovy-scripts)

### Jenkins: Support 🏥

* Find your answers within the [community](https://community.jenkins.io/) in different channels like [Stack Overflow](https://stackoverflow.com/questions/tagged/jenkins)
* Use [Support Core plugin](https://plugins.jenkins.io/support-core/) to export a snaphot of the configuration of your instance.
* Create a [Custom log Recorder](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-and-managed-masters/how-do-i-create-a-logger-in-jenkins-for-troubleshooting-and-diagnostic-information) to increase visibility on the failure components.
* If you are stuck, report your request or bug in the [Jenkins Jira](https://issues.jenkins.io/secure/Dashboard.jspa)

### Jenkins: Inspiring Talks

* [🎥 MANGO: Orchestrating a Terraform pipeline with Jenkins](https://www.youtube.com/watch?v=61C6wD_y1HA)
* [🎥 DevOps Toolkit: Running Jenkins In Kubernetes](https://www.youtube.com/watch?v=2Kc3fUJANAc)

## CloudBees CI: Make Jenkins administration more scalable and reliable 🚀

### CloudBees CI: Installation and Architecture

* There are two plataform types to install CloudBees CI:
  * [Traditional platform](https://docs.cloudbees.com/docs/cloudbees-ci/latest/architecture/ci-trad) (see [diagram](https://docs.cloudbees.com/docs/cloudbees-ci/latest/architecture/_images/cloudbees-ci-traditional-arch.574b6fc.svg))
    * Make your CI builds **more resilient** by adding [High Availability](https://docs.cloudbees.com/docs/cloudbees-ci/latest/traditional-install-guide/high-availability) (see [architecture diagram](https://docs.cloudbees.com/docs/cloudbees-ci/latest/traditional-install-guide/_images/ha-network-diagram.e8469d2.png)).
      * ⚠️ Ensure to meet the requirements from [NFS Guide](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-and-managed-masters/nfs-guide)
  * [Modern platform](https://docs.cloudbees.com/docs/cloudbees-ci/latest/architecture/ci-cloud) (see [architecture diagram](https://docs.cloudbees.com/docs/cloudbees-ci/latest/architecture/_images/k8s-ci-architecture.31527cd.svg))
    * CloudBees CI on Kubernetes additionally benefits from the robust container management of the Kubernetes control plane. Aside from the operations center and managed controllers running as `StatefulSets`, controllers use the Jenkins Kubernetes plugin to schedule builds on disposable agent pods, eliminating the need to explicitly manage worker infrastructure.
    * Make your CI build **more elastic** thanks to:
      * Configure autoscaling (for [example in EKS](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/eks-auto-scaling-nodes))
      * Configure [Hibernation on Controllers](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/managing-controllers#_hibernation_in_managed_masters) to save computing cost
      * Enable Hybrid Cloud workload (among different public clouds and on-premises)
        * [Controllers](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/provisioning-in-multiple-clusters)
        * [Agents](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/deploying-agents-separate-cluster)
* License: Get a Trial or [Import your Key and Certificate pair](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-and-managed-masters/what-is-a-cloudbees-jenkins-enterprise-instance-id-and-how-do-i-find-it)
* Always install the latest version and review [CloudBees CI Release Notes](https://docs.cloudbees.com/docs/release-notes/latest/cloudbees-ci/) to understand the new features and bug fixes.
* Network Requirements
  * For inbound agents but also for [Controllers use Wesockets](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-setup-guide/websockets) to make connections simpler, more straightforward, and easier to establish via HTTPS.
* 🔒 Installations more secure with:
  * [Signed Docker images](https://docs.cloudbees.com/docs/cloudbees-ci/latest/kubernetes-install-guide/verifying-cloud-docker-images)
  * [Signed Helm Charts](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/helm-verification)

### CloudBees CI: Configuration

* If you come from Jenkins Open source, [Migrate](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-and-managed-masters/migrating-jenkins-instances) your configuration and transit data (builds) to CloudBees CI. See [🎥 Migrating from Jenkins LTS to CloudBees CI](https://cloudbees.wistia.com/medias/x5ixxnvhy4)
  * For this types of scenarios or any type of service maintenance, [CloudBees Quiet Start](https://docs.cloudbees.com/docs/admin-resources/latest/plugins/quiet-start) can help to not run all your builds immediately after restart.
* Configuration as Code: Extend JCasc with more enriched features thanks to Casc.
  * [Operation Center](https://docs.cloudbees.com/docs/cloudbees-ci/latest/casc-oc/)
  * [Controllers](https://docs.cloudbees.com/docs/cloudbees-ci/latest/casc-oc/)
* Operation Center: Central governance of connected CI Controllers by a Shared Context which eases the scaling of your CI platform (It mitigates the pain of managing isolated Jenkins instances).
  * Controllers types:
    * Traditional: [Client Controllers](https://docs.cloudbees.com/docs/cloudbees-ci/latest/traditional-setup-guide/connecting-cms)
    * Modern: [Managed Controllers](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/managing-controllers).
      * Note, Modern also supports Client Controllers.
  * Use [Move/Copy/Promote](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/move-copy-promote) to disribute items across your Plataform.
  * [Cluster Operations](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/cluster-operations) perform maintenance operations on various items in operations center, such as Client/Managed Controllers.
  * Shared Agent Configuration
    * [Shared Agent](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/shared-agents) for static agents.
    * [Shared Cloud](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/pushed-clouds), including Kubernetes ([Globally editing pod templates in operations center](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/agents#_globally_editing_pod_templates_in_operations_center))
  * [Centrally managing security for controllers SSO](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/using-sso).
* Plugins Management:
  * Enable [Beekeeper Upgrade Assistant](https://docs.cloudbees.com/docs/admin-resources/latest/plugin-management/beekeeper-upgrade-assistant) to guarantee plugin compatibility with the Jenkins core version thanks to the [CloudBees Assurance Program (CAP)](https://docs.cloudbees.com/docs/admin-resources/latest/assurance-program/)
    * [Plugins in the CAP are categorized into three tiers](https://docs.cloudbees.com/search?type=ci-plugins&search=show), adding to Jenkins comunity plugin a set of Propietary plugins, when you are trying to determine if you should install a particular plugin, [choosing plugins that are part of CAP](https://docs.cloudbees.com/docs/admin-resources/latest/plugin-management/find-support-tier) (Tier 1 and Tier 2) provides the assurance of greater stability and security.
    * Have flexibility to override CAP on a plugin-by-plugin basis with [Beekeeper plugin exceptions](https://docs.cloudbees.com/docs/admin-resources/latest/plugin-management/beekeeper-exceptions)
    * Extend Beekeeper with plugins outside CAP (e.g. custom plugins) with the [Plugin Catalog](https://docs.cloudbees.com/docs/admin-resources/latest/plugin-management/configuring-plugin-catalogs)
  * Air-gapped Environment: Use [kyounger/casc-plugin-dependency-calculation:](https://github.com/kyounger/casc-plugin-dependency-calculation) to calculate target plugin.yaml and plugin-catalog.yaml
* 🔒 Increase your Security
  * Adding roles to your authorization strategy using [RBAC](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/rbac) ([setup example](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/operations-center/rbac-multiple-configurations-in-a-cjoc-cje-architecture))
    * ⚠️ Remember to map your AD/LDAP Groups with CloudBees RBAC Groups as membership. Mapping to AD/LDAP individual users increase the complexity to mantein your security.
  * Support for [Self-signed certificates in Kubernetes](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/kubernetes-self-signed-certificates)
  * 🔑 Credentials:
    * CloudBees HashiCorp Vault plugin (coming soon) - Note: The [OSS plugin](https://plugins.jenkins.io/hashicorp-vault-plugin/) only works in jobs.
    * Restrictions with:
      * [Folders and RBAC](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-and-managed-masters/ssh-credentials-management-with-jenkins#_architecture_with_credential_management_in_folders)
      * [Restricted Credentials](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/restricted-credentials) lets you define restricted credentials with built-in access control using the full item names define in allowlists and denylists.
    * Adding [CyberArk plugin](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/cyberark) provider.
  * [Trigger restrictions](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/trigger-restrictions) restrict which upstream jobs are allowed to trigger builds of other jobs.
* [Folder plus](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-secure-guide/folders-plus) adds the following features to the Standard folder plugin: Define environment variables that are passed to the builds of all jobs within a folder, Display selected jobs types from subfolders in a higher-level view, and Restrict which agents each team has access to and Restrict which kinds of items may be created in a folder (useful for Compliance)
* Developer productivity:
  * [Cross Team Collaboration](https://docs.cloudbees.com/docs/admin-resources/latest/pipelines/cross-team-collaboration) improves collaboration by connecting Pipelines on the same controller or different one. It allows a Pipeline to create a notification event that will be consumed by other Pipelines waiting on it to trigger a job.
  * :octocat: [GitHub Apps](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/github-app-auth): Receive and act upon granular, actionable build data directly in GitHub. [Unthrottling GitHub API usage](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/github-app-auth#_unthrottling_github_api_usage)
  * [CloudBees SCM Reporting](https://docs.cloudbees.com/docs/cloudbees-ci/latest/scm-integration/enabling-scm-reporting): Provides rich information beyond the standard GitHub or Bitbucket pass/fail status, Displays check for code coverage and test results directly in GitHub or Bitbucket, and Delivers detailed error and warning summaries.
  * 🔔 [Slack](https://docs.cloudbees.com/docs/cloudbees-ci/latest/slack-integration/slack-integration-intro): Receive granular, actionable build data directly in Slack. Its complementary to the [🎥 Slack Notifications From Jenkins](https://www.youtube.com/watch?v=EDVZli8GdUM)
    * OOS plugins is for general notifications to be sent to a channel (...but you have to add that integration in the pipeline)
    * CloudBee's plugin is for personal/channel actionable notifications but only for PRs.
  * [Service Now](https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/servicenow) Create and manage ServiceNow change requests and incident tickets from your Pipeline
  * New UI replacement for [Blue Ocean](https://www.jenkins.io/doc/book/blueocean/getting-started/): [CloudBees Pipeline Explorer Plugin](https://docs.cloudbees.com/docs/release-notes/latest/plugins/cloudbees-pipeline-explorer-plugin/).
* Housekeeping
  * [CloudBees Inactive Items plugin](https://docs.cloudbees.com/docs/admin-resources/latest/plugins/inactive-items): Identify **unused items** which are good candidate to be removed from the instance.
  * [CloudBees Usage plugin](https://docs.cloudbees.com/docs/admin-resources/latest/plugins/plugin-usage): Curated list of **plugins usage** at instance level. It is recommeded to only install plugin the instance required.

### CloudBees CI: Administration

* 📈 Observability, adding the [CloudBees Prometheus Metrics plugin](https://docs.cloudbees.com/docs/cloudbees-ci/latest/monitoring/prometheus-plugin) which exposes metrics securely for Operation Center. (it can be used also with Controllers)
* 🔬 Auditing, adding the [User Activity Monitoring plugin](https://docs.cloudbees.com/docs/admin-resources/latest/plugins/user-activity-monitoring) which provides you with a summary of user activity.
* 💾 [Backup/Restore](https://docs.cloudbees.com/docs/admin-resources/latest/backup-restore/)
  * [CloudBees Backup plugin](https://docs.cloudbees.com/docs/admin-resources/latest/backup-restore/cloudbees-backup-plugin) to automate the backup process.
    * It offers a more solid backup solution which is integrated in CasC and compatible with [multiple Storage types](https://docs.cloudbees.com/docs/admin-resources/latest/backup-restore/cloudbees-backup-plugin#where-to-back-up) (including [AWS S3](https://docs.cloudbees.com/docs/admin-resources/latest/backup-restore/cloudbees-backup-plugin#_amazon_s3) or other [Cloud Buckets S3-compatible](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/operations-center/overriding-aws-s3-endpoint-for-cluster-operation-backups))
    * It can be integrated with [Cluster Operation to take a backup](https://docs.cloudbees.com/docs/admin-resources/latest/backup-restore/backup-cluster) for every controller connected to the controller.
* Operate remotely with Jenkins
  * API REST
    * 🔒 [CloudBees Request Filter Plugin](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/client-and-managed-masters/how-do-i-use-the-cloudbees-request-filter-plugin) can block any specifict API endpoint request that has been identified like potential damage for the performance or security instance.
    * New API Endpoints are adding for [Casc](https://docs.cloudbees.com/docs/cloudbees-ci-api/latest/bundle-management-api) and [RBAC](https://docs.cloudbees.com/docs/cloudbees-ci-api/latest/rbac-api)

### CloudBees CI: Support 🏥

* [Get the best support in Jenkins](https://www.cloudbees.com/jenkins/what-is-jenkins): CloudBees is an active participant in the Jenkins community and plays a significant role in supporting the project. A number of key contributors to the Jenkins project are employed by CloudBees.Engineers from the CloudBees support and product teams regularly contribute code to the Jenkins project.
* From day zero you are not alone in this journey, [CloudBees Support](https://support.cloudbees.com/hc/en-us) counts on a Global Team of [Certified CloudBees CI/Jenkins experts](https://www.cloudbees.com/cloudbees-university/training-certifications) willing to answer your questions and help your processes including [Assisted updates](https://docs.cloudbees.com/docs/cloudbees-ci-kb/latest/required-data/required-data-upgrade-a-jenkins-instance)
  * [CloudBees plugin support policies](https://docs.cloudbees.com/docs/cloudbees-common/latest/plugin-support-policies) will cover Tier 1 and Tier 2 plugins.
  * Additionally, CloudBees includes:
    * [Jenkins Health Advisor](https://plugins.jenkins.io/cloudbees-jenkins-advisor/)  to make sure your instance is not impacted by Known issues and meets with Best Practices
    * [Support CLI](https://docs.cloudbees.com/docs/cbsupport/latest/) to help you with data collection per topic.
  
### CloudBees CI: Inspiring Talks

* [🎥 CloudBees TV: CloudBees CI Tutorials](https://www.youtube.com/watch?v=61C6wD_y1HA)
* [🎥 CloudBees TV: CloudBees Customers](https://www.youtube.com/playlist?list=PLvBBnHmZuNQLeQFZcDOQxFAHYk96_c7sp)