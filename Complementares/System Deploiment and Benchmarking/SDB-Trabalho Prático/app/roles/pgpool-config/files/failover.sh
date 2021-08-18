#!/bin/bash
# By Fat Dragon, 05/25/2016
# Recovers a standby server.
 
if [ $# -ne 5 ]
then
    echo "failover falling_node oldprimary_node new_primary replication_password trigger_file"
    exit 1
fi
 
FALLING_NODE=$1         # %d
OLDPRIMARY_NODE=$2      # %P
NEW_PRIMARY=$3          # %H
REPL_PASS=$4
TRIGGER_FILE=$5
 
echo "failover.sh FALLING_NODE: ${FALLING_NODE}; OLDPRIMARY_NODE: ${OLDPRIMARY_NODE}; NEW_PRIMARY: ${NEW_PRIMARY}; at $(date)\n" >> /etc/postgresql/9.5/main/replscripts/exec.log
 
if [ $FALLING_NODE = $OLDPRIMARY_NODE ]; then
    if [ $UID -eq 0 ]
    then
        sudo -u postgres ssh -T postgres@$NEW_PRIMARY /etc/postgresql/9.5/main/replscripts/promote.sh -f -p $REPL_PASS -d $OLDPRIMARY_NODE
    else
        ssh -T postgres@$NEW_PRIMARY /etc/postgresql/9.5/main/replscripts/promote.sh -f -p $REPL_PASS -d $OLDPRIMARY_NODE
    fi
    exit 0;
fi;
 
exit 0;