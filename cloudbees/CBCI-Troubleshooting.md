# CloudBees CI Troubleshooting Guide

## Overview

This document provides a comprehensive troubleshooting workflow for CloudBees CI performance issues. The troubleshooting process requires a series of concatenated processes:

- **Capture** of the data depending on the issue
- **Analysis** to establish a hypothesis based on pieces of evidence  
- **Applying** mitigation measures

After applying the proposed fix, the instance behavior is monitored to assess (feedback) the stability of the application. If it is still unstable, the above steps are repeated.

## Troubleshooting Flow Diagram

The following diagram illustrates the complete troubleshooting workflow:

```mermaid
graph TD
    A[Start] --> B{Meet all Best Practices?};
    B -->|No| C[Fix Prerequisites: System and Infra General and Cloud Pipelines];
    B -->|Yes| D[CloudBees CI ready for Production];
    C --> B;
    D --> M[Monitor System KPIs, Logs, and Alerts];
    M --> N{KPI Alert Triggered};
    N -->|Yes| E[Identify Symptom];
    N -->|No| M;
    E --> E1[CPU];
    E --> E2[Memory];
    E --> E3[Liveness Probe];
    E --> E4[Pipeline Hungs];
    E3 --> E1;
    E3 --> E2;
    E1 --> E1A[Application Slowdown];
    E1A --> F1[Required Data: Controller Support Bundle, collectPerformanceData.sh, GC log];
    E2 --> E2A[JVM Heap exhausted: jenkins.log: java.lang.OutOfMemoryError];
    E2 --> E2B[Linux Kernel OOM: dmesg.log Kill process JENKINS PID];
    E2 --> E2C[Kubernetes OOM Killed];
    E2A --> F2[Required Data: Controller Support Bundle, jenkinsjmap.sh];
    E2B --> F2;
    E2C --> F2;
    E4 --> F4[Required Data: Pipeline Support Bundle Pipeline Explorer and OTEL Tracing Controller Support Bundle FlowExecutionList.xml];
    F1 --> F1A[Threads > FastThread];
    F1 --> F1B[GC Logs > GCEasy];
    F1A --> G["Correlate different troubleshoot datasource at the time windows the incident happened"];
    F1B --> G;
    F2 --> F2C[Heap Dump > Heap Hero];
    F2C --> F2A{Is it required a Native Memory Analysis?};
    F2A -->|Yes| F2B[Add JVM argument -XX:NativeMemoryTracking=detail];
    F2A -->|No| G;
    F2B --> F2D[Gather a summary by jcmd];
    F2D --> G;
    F4 --> G;
    G --> H{Hypothesis Formed?};
    H -->|Yes| I[Apply Fix];
    H -->|No| J[Escalate to CloudBees Support Team];
    I --> K{Issue Resolved?};
    K -->|Yes| L[End Troubleshooting];
    K -->|No| D;
    J --> L;
```

## Key Components Explained

### Prerequisites Check

Before beginning troubleshooting, ensure all best practices are met:

- **System & Infrastructure**: General and Cloud configurations
- **Pipelines**: Following CloudBees CI pipeline best practices

### Symptom Identification

The troubleshooting process begins with monitoring system KPIs, logs, and alerts. When a KPI alert is triggered, identify the specific symptom:

#### CPU Issues

- **Application Slowdown**: High CPU utilization causing performance degradation
- **Required Data**: Controller Support Bundle, collectPerformanceData.sh, GC log file

#### Memory Issues

- **JVM Heap Exhausted**: `java.lang.OutOfMemoryError` in jenkins.log
- **Linux Kernel OOM**: Kill process messages in `/var/log/dmesg.log`
- **Kubernetes OOM Killed**: Container terminated by Kubernetes
- **Required Data**: Controller Support Bundle, jenkinsjmap.sh

#### Liveness Probe Issues

- Pod restarts due to liveness probe failures
- Connects to CPU and Memory analysis paths

#### Pipeline Hangs

- Jenkins CI pipelines become unresponsive or hang
- **Required Data**: OTEL Tracing, Pipeline Support Bundle

### Data Analysis Tools

#### For CPU Analysis

- **Threads > FastThread**: Thread dump analysis
- **GC Logs > GCEasy**: Garbage collection analysis

#### For Memory Analysis

- **Heap Dump > Heap Hero**: Memory usage analysis
- **Native Memory Analysis** (optional):
  1. Add JVM argument: `-XX:NativeMemoryTracking=detail`
  2. Gather summary by running `jcmd` after 24 hours

### Data Correlation

All analysis paths converge to correlate different troubleshoot data sources within the time window when the incident happened.

### Resolution Process

1. **Hypothesis Formation**: Based on data analysis
2. **Apply Fix**: Implement the identified solution
3. **Validation**: Check if the issue is resolved
4. **Escalation**: Contact CloudBees Support Team if hypothesis cannot be formed

## Best Practices

- Always ensure CloudBees CI is ready for production before troubleshooting
- Collect data when the issue is happening or immediately after
- Use the recommended analysis tools for each data type
- Document findings and applied fixes for future reference

## Support

If troubleshooting does not resolve the issue, escalate to the **CloudBees Support Team** with all collected data and analysis results.