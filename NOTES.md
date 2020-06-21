## v1:
- single queue + DLQ
- DLQ reprocessor: human-triggered, pushes DLQ'd messages back to main (real-time) queue
- Alerting is based on DLQ depth
- how to examine/triage/fix messages?
    - Service Bus Explorer (https://github.com/paolosalvatori/ServiceBusExplorer)
- Downsides:
    - Doesn't adapt well to network outages/downstream issues, as only retry is at the queue level
    - Poison and non-poision messages are lumped together in the DLQ if there are downstream issues
    - Not self-healing
    - Noiser with respect to alerting.  In the case of network issues, the lack of deferred retry means DLQ depth can increase and hit an alerting limit, even though there is no reasonable action for the alerted developer to take other than wait out the network issues and requeue the DLQ'd messages.  V2 addresses this by including a deferred retry queue that will be processed at a variable interval to handle transient issues without developer intervention.
- Benefits:
    - "good enough" for low throughput, well-sanitized data (requires making lots of assumptions)
    - simple

## v2:
- multi-queue
- smart routing (route to dead-letter or deferred queue based on api response/standardized response data)
- Additive Increase/Mulplicative Decrease policy for deferred queue
- deferred queue also has DLQ, will fill due to outages that are not resolved within retry window + TTL (or dead-letter if window is at max and retry fails?) <- evaluate DLQ conditions
	- Prevents dropped messages as deferred queue fills + hits size limit, cycles old messages out of rotation for later requeuing back into the deferred queue
    - human-triggered operation to invoke reprocessing from deferred DLQ (from v1)
    - alerting should be present on deferred DLQ depth.  This indicates the presence of a real downstream issue that requires intervention/monitoring
        - alerting on deferred queue depth is not especially helpful, as deferred queue is meant to give best-effort delivery before dead-lettering.