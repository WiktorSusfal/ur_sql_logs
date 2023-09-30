CREATE TABLE IF NOT EXISTS {schema_name}.{run_exp_msg_table_name} (
	message_id int8 NOT NULL,
    robot_id varchar NOT NULL,
	msg_type varchar NULL,
	"timestamp" varchar NULL,
	date_time timestamp NULL,
	"source" varchar NULL,
	source_name varchar NULL,
	robot_message_type varchar NULL,
    script_line_no int4 NULL,
	script_column_no int4 NULL,
	text_message varchar NULL,
	CONSTRAINT {run_exp_msg_table_name}_pkey PRIMARY KEY (message_id),
	CONSTRAINT run_exp_message_robot_id_fkey FOREIGN KEY ({msg_foreign_key_column_name}) 
			REFERENCES {schema_name}.{robot_info_table_name}({robot_pk_column_name})
);
CREATE INDEX IF NOT EXISTS "MDRunExpMessage_robot_info_fk" ON {schema_name}.{run_exp_msg_table_name} USING btree ({msg_foreign_key_column_name});