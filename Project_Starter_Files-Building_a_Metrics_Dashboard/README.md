**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation
![pods.png](answer-img/pods.png)
![services1.png](answer-img/services1.png)
![services2.png](answer-img/services2.png)

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.
![grafana.png](answer-img/grafana.png)

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.
![prometheus_source.png](answer-img/prometheus_source.png)

## Describe SLO/SLI
*TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.

monthly uptime:
It would make sense to set up automatic checks for the entry page of the application with a fixed frequency. Downtime would be calculated as: {number of times app was not responding}/{total amount of requests}

request response time:
Here we need to establish a baseline first. I would measure the response time during different times of the day and from different locations. Based on that data we could use the mean or the median to set a threshold.

## Creating SLI metrics.
*TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 
- share of errors - {number of requests with 40x or 50x}/{total number of requests}
- Response time of frontend and backend. Load time for the initial page load and response time of backend services, like login
- Max cpu usage in a given time period
- Max memory usage in a given time period
- Uptime of application usage in a given time period

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.
![prometheus_dashboard.png](answer-img/prometheus_dashboard.png)

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here. Also provide a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.
![tracer1.png](answer-img/tracer1.png)
![tracer2.png](answer-img/tracer2.png)
![jaeger_trace.png](answer-img/jaeger_trace.png)

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.
![jaeger_dashboard.png](answer-img/jaeger_dashboard.png)

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.

TROUBLE TICKET

Name: Andreas Rickert

Date: 16.10.2023

Subject: latency endpoint takes to long to respond

Affected Area: backend

Severity: high

Description: The grafana dashboard shows that the response time for the latency endpoint is 10 seconds

![ticket_span1.png](answer-img/ticket_span1.png)
![ticket_span2.png](answer-img/ticket_span2.png)


## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.

- CPU usage: Max cpu usage should not exceed 80% in a given month
- Latency: The response time of requests should not be higher than 100 ms
- Uptime: There must be atleast 99.95% uptime per month.
- Failure Rate: The error rate should be below 1 % per month.

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen. We will make a dashboard for this, but first write them down here.
- Error Rate : Share of 4xx and 5xx, given the total number of requests
- Resources: CPU and Memory usage
## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  
![final_dashboard.png](answer-img/final_dashboard.png)
