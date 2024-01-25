# convert-json-logs-to-legacy
Convert MongoDB 4.4 JSON logs to legacy logs to work for mTools and t2

Modified the script to generate logs that would resemble the legacy format. These changes support mplotquery --yaxis.

# Usage:
generate_mplot_logs.py --log mongodb.log > legacy.log

# Below are the following log types that the script process:
* CONTROL
  * Only a single CONTROL line to make it work for t2
  * It needs to add pid, port, arch and host
* ACCESS
  * To generate authentication entry
* NETWORK
  * To generate the clients, connstats and connections statistics
* COMMAND, WRITE, QUERY and TXN
  * To generate mplotqueries
  * To generate mloginfo --queries
  * To generate mloginfo --clients --connstats --connections
  * To generate mplotqueries with bytesRead as yaxis. mplotqueries <log> --yaxis bytesRead

# Note:
The converted log can be dragged to t2 to add "Server Log" metrics
