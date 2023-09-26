CREATE TABLE IF NOT EXISTS {schema_name}.{run_exp_msg_table_name} (
	message_id int8 NOT NULL,
    robot_id varchar NULL,
	msg_type varchar NULL,
	"timestamp" varchar NULL,
	date_time timestamp NULL,
	"source" varchar NULL,
	robot_message_type varchar NULL,
    script_line_no int4 NULL,
	script_column_no int4 NULL,
	text_message varchar NULL,
	CONSTRAINT {run_exp_msg_table_name}_pkey PRIMARY KEY (message_id)
);