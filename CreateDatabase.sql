-- Database: postgres

-- DROP DATABASE IF EXISTS postgres;

CREATE DATABASE postgres
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.utf8'
    LC_CTYPE = 'Russian_Russia.utf8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE postgres
    IS 'default administrative connection database';


-- Table: public.coin_transfer

-- DROP TABLE IF EXISTS public.coin_transfer;

CREATE TABLE IF NOT EXISTS public.coin_transfer
(
    transfer_id integer NOT NULL DEFAULT nextval('coin_transfer_tranasfer_id_seq'::regclass),
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    coins_send_amount integer NOT NULL,
    CONSTRAINT coin_transfer_pkey PRIMARY KEY (transfer_id),
    CONSTRAINT coin_transfer_receiver_id_fkey FOREIGN KEY (receiver_id)
        REFERENCES public.employee_info (employee_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT coin_transfer_sender_id_fkey FOREIGN KEY (sender_id)
        REFERENCES public.employee_info (employee_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.coin_transfer
    OWNER to postgres;


-- Table: public.employee_info

-- DROP TABLE IF EXISTS public.employee_info;

CREATE TABLE IF NOT EXISTS public.employee_info
(
    employee_id integer NOT NULL,
    employee_name character varying(255) COLLATE pg_catalog."default",
    coins integer,
    CONSTRAINT employee_info_pkey PRIMARY KEY (employee_id),
    CONSTRAINT employee_id_fkey FOREIGN KEY (employee_id)
        REFERENCES public.user_auth (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.employee_info
    OWNER to postgres;


-- Table: public.employee_inventory

-- DROP TABLE IF EXISTS public.employee_inventory;

CREATE TABLE IF NOT EXISTS public.employee_inventory
(
    entry_id integer NOT NULL DEFAULT nextval('employee_inventory_entry_id_seq'::regclass),
    employee_id integer NOT NULL,
    item_type integer NOT NULL,
    item_quantity integer NOT NULL,
    CONSTRAINT employee_inventory_pkey PRIMARY KEY (entry_id),
    CONSTRAINT employee_id_fkey FOREIGN KEY (employee_id)
        REFERENCES public.employee_info (employee_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT item_type_fkey FOREIGN KEY (item_type)
        REFERENCES public.merch (merch_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.employee_inventory
    OWNER to postgres;


-- Table: public.user_auth

-- DROP TABLE IF EXISTS public.user_auth;

CREATE TABLE IF NOT EXISTS public.user_auth
(
    user_id integer NOT NULL DEFAULT nextval('user_auth_user_id_seq'::regclass),
    user_login character varying(255) COLLATE pg_catalog."default" NOT NULL,
    user_password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_auth_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_auth
    OWNER to postgres;

-- Table: public.merch

-- DROP TABLE IF EXISTS public.merch;

CREATE TABLE IF NOT EXISTS public.merch
(
    merch_id integer NOT NULL DEFAULT nextval('merch_merch_id_seq'::regclass),
    merch_name character varying(255) COLLATE pg_catalog."default",
    merch_cost integer,
    CONSTRAINT merch_pkey PRIMARY KEY (merch_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.merch
    OWNER to postgres;

Заполнение таблицы merch:
INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('t-shirt', 80);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('cup', 20);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('book', 50);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('pen', 10);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('powerbank', 200);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('hoody', 300);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('umbrella', 200);


INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('wallet', 50);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('t-shirt', 80);

INSERT INTO public.merch(
	merch_id, merch_name, merch_cost)
	VALUES ('pink-hoody', 500);