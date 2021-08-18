#!/bin/bash
# By Fat Dragon, 05/25/2016
# Recovers a standby server.
 
if [ $# -ne 3 ]
then
    echo "recovery_1st_stage datadir remote_host remote_datadir"
    exit 1
fi
 
PGDATA=$1
REMOTE_HOST=$2
REMOTE_PGDATA=$3
 
PORT=5433
 
echo "recovery_1st_stage.sh - PGDATA: ${PGDATA}; REMOTE_HOST: ${REMOTE_HOST}; REMOTE_PGDATA: ${REMOTE_PGDATA}; at $(date)\n" >> /etc/postgresql/9.5/main/replscripts/exec.log
 
hostnamelower=$(echo "$HOSTNAME" | tr '[:upper:]' '[:lower:]')
remotelower=$(echo "$REMOTE_HOST" | tr '[:upper:]' '[:lower:]')
 
if [ "$hostnamelower" = "$remotelower" ]; then
	echo "Cannot recover myself."
	exit 1
fi
 
echo "Checking if primary info file exists..."
if [ ! -f /var/lib/postgresql/9.5/main/primary_info ]; then
	echo "Primary info file not found."
	exit 1
fi
 
echo "Reading additional data from primary info file..."
source /var/lib/postgresql/9.5/main/primary_info
 
if [ ! -e $TRIGGER_FILE ]; then
	echo "Trigger file not found."
	exit 1
fi
 
if [ -e $STANDBY_FILE ]; then
	echo "Standby file found."
	exit 1
fi
 
if [ $UID -eq 0 ]
then
	sudo -u postgres ssh -T postgres@$REMOTE_HOST /etc/postgresql/9.5/main/replscripts/initiate_replication.sh -f -t $TRIGGER_FILE -s $STANDBY_FILE -H $HOSTNAME -P $PORT -u $REPL_USER -p $REPL_PASSWORD
else
	ssh -T postgres@$REMOTE_HOST /etc/postgresql/9.5/main/replscripts/initiate_replication.sh -f -t $TRIGGER_FILE -s $STANDBY_FILE -H $HOSTNAME -P $PORT -u $REPL_USER -p $REPL_PASSWORD
fi
 
exit 0;