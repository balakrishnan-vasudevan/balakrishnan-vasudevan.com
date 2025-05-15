
## Go Learning Roadmap for SRE & Platform Engineering

## Overview
This roadmap is designed for SREs and platform engineers aiming to master Go for cloud-native systems, observability, automation, and infrastructure tooling.

---

## Phase 1: Core Go Fundamentals (2–3 weeks)

### Topics
- Basic syntax, types, structs, interfaces
- Idiomatic error handling
- Goroutines, channels, select
- Dependency management with Go modules

### Resources
- [Tour of Go](https://tour.golang.org/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go by Example - Concurrency](https://gobyexample.com/goroutines)
- [Go Error Handling Best Practices](https://medium.com/@thedevsaddam/error-handling-in-golang-best-practices-a1e19d3cbd8c)
- [Using Go Modules](https://blog.golang.org/using-go-modules)

---

## Phase 2: Infrastructure and Systems Focus (3–4 weeks)

### Topics
- REST APIs & JSON
- gRPC & Protocol Buffers
- CLI tooling (Cobra)
- Config management (Viper, YAML, JSON)

### Resources
- [Go REST API Example (Chi)](https://github.com/go-chi/chi)  
- [Build RESTful APIs with Go](https://levelup.gitconnected.com/how-to-build-restful-api-in-go-fc3b5e5d2bcd)
- [gRPC Quickstart for Go](https://grpc.io/docs/languages/go/quickstart/)
- [Cobra CLI Guide](https://github.com/spf13/cobra)
- [Viper Config Management](https://github.com/spf13/viper)

---

## Phase 3: Observability and SRE Tooling (3–4 weeks)

### Topics
- Prometheus instrumentation
- Distributed tracing with OpenTelemetry
- Structured logging
- Test automation and benchmarks

### Resources
- [Prometheus Go Client](https://github.com/prometheus/client_golang)
- [Instrumenting Go apps with Prometheus](https://prometheus.io/docs/guides/go-application/)
- [OpenTelemetry for Go](https://opentelemetry.io/docs/instrumentation/go/)
- [SigNoz + OpenTelemetry](https://signoz.io/blog/opentelemetry-go/)
- [Zerolog](https://github.com/rs/zerolog), [Logrus](https://github.com/sirupsen/logrus)
- [Go testing](https://go.dev/doc/tutorial/add-a-test)
- [Testify](https://github.com/stretchr/testify)

---

## Phase 4: Advanced Topics & Real-World Projects (ongoing)

### Topics
- Kubernetes operators with Kubebuilder
- Performance tuning and pprof
- Networking in Go

### Resources
- [Kubebuilder Book](https://book.kubebuilder.io/)
- [Sample Controller with client-go](https://github.com/kubernetes/sample-controller)
- [Go Performance Tuning](https://blog.golang.org/pprof)
- [Uber Go Performance Guide](https://github.com/uber-go/guide/blob/master/style.md#performance)
- [TCP Server in Go](https://gobyexample.com/tcp-server)

---

## Capstone Projects

- [ ] Build a CLI tool for parsing and alerting on log files
- [ ] Create a REST/gRPC service for internal service health checks
- [ ] Build a Kubernetes operator with Kubebuilder
- [ ] Instrument a service with Prometheus and OpenTelemetry

---

**Tip:** Use backlinks (`[[Go Concurrency]]`, `[[Prometheus]]`, etc.) to break out topics into detailed notes as you learn.