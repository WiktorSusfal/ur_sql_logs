CREATE TABLE IF NOT EXISTS {schema_name}.{version_msg_table_name} (
	message_id int8 NOT NULL,
	robot_id varchar NULL,
	msg_type varchar NULL,
	"timestamp" varchar NULL,
	date_time timestamp NULL,
	"source" varchar NULL,
	robot_message_type varchar NULL,
    project_name varchar NULL,
	major_version varchar NULL,
	minor_version varchar NULL,
	bugfix_version varchar NULL,
	build_number varchar NULL,
	build_date varchar NULL,
	CONSTRAINT {version_msg_table_name}_pkey PRIMARY KEY (message_id)
);