CREATE SEQUENCE IF NOT EXISTS {schema_name}.{sequence_name}
AS bigint
    INCREMENT BY 1
    MINVALUE 0
    START WITH 0;