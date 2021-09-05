#!/bin/bash
LOG_LEVEL="critical"
LOG="locust-log.txt"
MASTER_PORT=8088
MASTER_IP="127.0.0.1"
cores=16
SERVER_HOST=http://aa0af0149eb6c49f7b19964e000e6b28-1582031936.ap-southeast-1.elb.amazonaws.com
echo -e "\nStart LOCUST MASTER\n"
locust -f locustfile.py -L $LOG_LEVEL --logfile=$LOG --master-bind-port=$MASTER_PORT \
--master-bind-host=$MASTER_IP --master --expect-workers=$cores --host=$SERVER_HOST&
PID_MASTER=$!
echo "LOCAST MASTER PID = $PID_MASTER"
sleep 5

# start SLAVE (clients)
echo -e "\nStart LOCUST SLAVES\n"
PID_SLAVES=( )
for ((i = 1; i <= $cores; i++));do
  locust -f locustfile.py --worker --master-host=$MASTER_IP --master-port=$MASTER_PORT -L $LOG_LEVEL --logfile=$LOG &
  PID_SLAVES+=( $! )
done
echo "LOCAST SLAVE PIDs = ${PID_SLAVES[@]}"