CREATE TABLE IF NOT EXISTS {schema_name}.{comm_msg_table_name} (
	message_id int8 NOT NULL,
	robot_id varchar NULL,
	msg_type varchar NULL,
	"timestamp" varchar NULL,
	date_time timestamp NULL,
	"source" varchar NULL,
	robot_message_type varchar NULL,
    code varchar NULL,
	argument varchar NULL,
	report_level varchar NULL,
	report_level_name varchar NULL,
	data_type varchar NULL,
	"data" varchar NULL,
	text_message varchar NULL,
	CONSTRAINT {comm_msg_table_name}_pkey PRIMARY KEY (message_id)
);