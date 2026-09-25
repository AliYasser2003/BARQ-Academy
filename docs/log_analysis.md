# Log Analysis

## 1. Purpose

This document summarizes the analysis of the three historical logs supplied with the BARQ-Academy project:

- `logs/access.log`
- `logs/application.log`
- `logs/error.log`

The logs were inspected without modification. The analysis was used to understand request outcomes, application behavior, and NGINX upstream failures.

## 2. Log Files and Record Counts

The command used was:

`wc -l logs/access.log logs/application.log logs/error.log`

Results:

- `access.log`: 726 total lines. 725 lines contained an HTTP status; 1 line was incomplete.
- `application.log`: 730 total lines. 729 lines contained a request ID; 1 line was malformed or incomplete.
- `error.log`: 68 total lines. 67 request-related lines and 1 log collector notice.

The access and application logs are structured, while NGINX errors are text-based. Request IDs were used to correlate records across the logs.

## 3. HTTP Status Counts

The access log contained 725 valid HTTP status entries:

- HTTP 200: 620
- HTTP 404: 10
- HTTP 500: 0
- HTTP 502: 40
- HTTP 503: 47
- HTTP 504: 8

The access log contains successful responses as well as gateway and service errors. The 502, 503, and 504 responses indicate that some requests did not complete successfully through NGINX.

There were no HTTP 500 responses in the valid access-log entries.

## 4. NGINX Upstream Connection Errors

The command used was:

`grep -c 'connect() failed' logs/error.log`

Result: 59 connection-failure lines.

All 59 contained `Connection refused`. The upstream address referenced in these entries was `172.23.0.12:8080`.

These messages show that NGINX attempted to connect to an upstream service but the connection was refused. They are evidence of upstream connectivity failures in the historical logs.

## 5. Correlated Request: lab-000606

Request ID `lab-000606` was found across the error, access, and application logs.

- `error.log`: NGINX reported an upstream timeout while reading the response header.
- `access.log`: The `/records` request returned HTTP 504; request time was approximately 2.001 seconds.
- `application.log`: `app-02` returned HTTP 200 after approximately 2700 ms.

### Interpretation

The application completed the request after approximately 2.7 seconds, but NGINX timed out at approximately 2 seconds and returned HTTP 504 to the client.

This explains why the same request ID is associated with an NGINX 504 and an application 200. The application’s successful completion occurred after NGINX had already timed out.

## 6. Data Quality and Correlation

The analysis identified incomplete or malformed records:

- `access.log`: 1 incomplete line.
- `application.log`: 1 malformed or incomplete line.
- `error.log`: 1 log collector notice.

The incomplete records were not included in the valid status or request-ID counts.

Request IDs were used to connect records from different log sources. A request may appear in more than one log, so the number of log lines should not be treated as the number of unique client requests.

## 7. Main Findings

1. The access log contained 725 valid HTTP status entries.
2. The access log recorded 40 HTTP 502, 47 HTTP 503, and 8 HTTP 504 responses.
3. NGINX recorded 59 upstream connection-refused errors.
4. Request `lab-000606` showed an NGINX timeout at approximately 2 seconds while the application completed after approximately 2.7 seconds.
5. The logs contained a small number of malformed, incomplete, or non-request records.
6. The historical logs provide evidence of request and upstream failures, but do not by themselves prove the exact cause of every failure.

## 8. Limitations

- This analysis covers the supplied historical logs only.
- The logs were not modified.
- The findings do not represent a live monitoring period.
- The historical logs do not prove that every failure had the same cause.
- Runtime validation and controlled failure testing were performed separately during later project phases.

## 9. Commands Used

- `find . -type f \( -name "*.log" -o -name "*.txt" \) -print`
- `wc -l logs/access.log logs/application.log logs/error.log`
- `grep -c 'connect() failed' logs/error.log`
- `grep -c 'upstream: "http://172.23.0.12:8080' logs/error.log`
- `grep 'lab-000606' logs/access.log`
- `grep 'lab-000606' logs/application.log`

The investigation commands and detailed baseline findings are also recorded in the Phase 1 Investigation Report.
