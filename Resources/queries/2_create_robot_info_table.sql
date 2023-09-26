CREATE TABLE IF NOT EXISTS {schema_name}.{robot_info_table_name} (
	id varchar NOT NULL,
	"name" varchar NULL,
	ip_address varchar NULL,
	port int4 NULL,
	read_frequency float8 NULL,
	CONSTRAINT {robot_info_table_name}_pkey PRIMARY KEY (id)
);