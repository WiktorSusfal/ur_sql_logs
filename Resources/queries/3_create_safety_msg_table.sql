CREATE TABLE IF NOT EXISTS {schema_name}.{safety_msg_table_name} (
	message_id int8 NOT NULL,
    robot_id varchar NULL,
	msg_type varchar NULL,
	"timestamp" varchar NULL,
	date_time timestamp NULL,
	"source" varchar NULL,
	robot_message_type varchar NULL,
    code varchar NULL,
	argument varchar NULL,
	safety_mode_type varchar NULL,
	safety_mode_name varchar NULL,
	report_data_type varchar NULL,
	report_data varchar NULL,
	CONSTRAINT {safety_msg_table_name}_pkey PRIMARY KEY (message_id)
);
CREATE INDEX "MDSafetyMessage_robot_info_fk" ON {schema_name}.{safety_msg_table_name} USING btree ({msg_foreign_key_column_name});


ALTER TABLE {schema_name}.{safety_msg_table_name} 
	ADD CONSTRAINT safety_message_robot_id_fkey FOREIGN KEY ({msg_foreign_key_column_name}) 
	REFERENCES {schema_name}.{robot_info_table_name}({robot_pk_column_name});