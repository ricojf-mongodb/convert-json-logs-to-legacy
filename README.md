# convert-json-logs-to-legacy
Convert MongoDB 4.4 JSON logs to legacy logs to work for mTools and t2

# Usage:
generate_mplot_logs.py --log mongodb.log > legacy.log

# Below are the following log types that the script process:
* CONTROL
  * Only a single CONTROL line to make it work for t2
  * It needs to add pid, port, arch and host
* NETWORK
  * To generate the clients, connstats and connections statistics
* COMMAND, WRITE and QUERY
  * To generate mplotqueries
  * To generate mloginfo --queries
  * To generate mloginfo --clients --connstats --connections

# Note:
The converted log can be dragged to t2 to add "Server Log" metrics
