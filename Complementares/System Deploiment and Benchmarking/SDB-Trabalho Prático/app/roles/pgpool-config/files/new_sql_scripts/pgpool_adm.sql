/* contrib/pgpool_adm/pgpool_adm--1.0.sql */

/* ***********************************************
 * Administrative functions for pgPool
 * *********************************************** */

/**
 * input parameters: node_id, host, port, username, password
 */
CREATE FUNCTION pcp_node_info(integer, text, integer, text, text, OUT host text, OUT port integer, OUT status text, OUT weight float4)
RETURNS record
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_node_info'
LANGUAGE C VOLATILE STRICT;

/**
 * input parameters: node_id, server_name
 */
CREATE FUNCTION pcp_node_info(integer, text, OUT host text, OUT port integer, OUT status text, OUT weight float4)
RETURNS record
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_node_info'
LANGUAGE C VOLATILE STRICT; 


/**
 * input parameters: host, port, username, password
 */
CREATE FUNCTION pcp_pool_status(text, integer, text, text, OUT item text, OUT value text, OUT description text)
RETURNS record
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_pool_status'
LANGUAGE C VOLATILE STRICT; 

/**
 * input parameters: server_name
 */
CREATE FUNCTION pcp_pool_status(text, OUT item text, OUT value text, OUT description text)
RETURNS record
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_pool_status'
LANGUAGE C VOLATILE STRICT; 

/**
 * input parameters: host, port, username, password
 */
CREATE FUNCTION pcp_node_count(text, integer, text, text, OUT node_count integer)
RETURNS record
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_node_count'
LANGUAGE C VOLATILE STRICT;

/**
 * input parameters: server_name
 */
CREATE FUNCTION pcp_node_count(text, OUT node_count integer)
RETURNS record
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_node_count'
LANGUAGE C VOLATILE STRICT;

/**
 * input parameters: node_id, host, port, username, password
 */
CREATE FUNCTION pcp_attach_node(integer, text, integer, text, text, OUT node_attached boolean)
RETURNS boolean
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_attach_node'
LANGUAGE C VOLATILE STRICT;

/**
 * input parameters: node_id, server_name
 */
CREATE FUNCTION pcp_attach_node(integer, text, OUT node_attached boolean)
RETURNS boolean
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_attach_node'
LANGUAGE C VOLATILE STRICT;

/**
 * input parameters: node_id, gracefully, host, port, username, password
 */
CREATE FUNCTION pcp_detach_node(integer, boolean, text, integer, text, text, OUT node_attached boolean)
RETURNS boolean
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_detach_node'
LANGUAGE C VOLATILE STRICT;

/**
 * input parameters: node_id, gracefully, server_name
 */
CREATE FUNCTION pcp_detach_node(integer, boolean, text, OUT node_attached boolean)
RETURNS boolean
AS '/usr/lib/postgresql/9.5/lib/pgpool_adm', '_pcp_detach_node'
LANGUAGE C VOLATILE STRICT;
