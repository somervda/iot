-- run from psql using the \i command e.g.
-- \i iotdb.sql

DROP DATABASE IF EXISTS  iotdb WITH (FORCE);

CREATE DATABASE iotdb with OWNER pi; 

-- Schema for the iotdb prostgresql database

\c iotdb

CREATE TABLE public.application (
	id SERIAL PRIMARY KEY,
	"name" varchar(50) NOT NULL,
	description varchar(2000) NULL,
	fields varchar(80)[] 
);

INSERT INTO public.application ("name",description,fields)
	VALUES ('Climate','Climate',ARRAY['celsius','humidity','hPa']);


CREATE TABLE public.device (
	id SERIAL PRIMARY KEY,
	"name" varchar(50) NOT NULL,
	description varchar(2000) NULL
);
INSERT INTO public.device ("name",description)
	VALUES ('Sensor01','Bed');
INSERT INTO public.device ("name",description)
	VALUES ('Sensor02','Piano');

-- many to many relationship table, linking applications to a device
-- one device can support measurements for multiple applications
-- This also holds the most recient data recieved for the app/dev combination
-- and the umt time it was recieved
-- initially umt and data are null until iot data starts to be recieved.
CREATE TABLE public.applicationDevice (
	application_id int4 REFERENCES public.application(id) ON DELETE CASCADE,
	device_id int4 REFERENCES public.device(id) ON DELETE CASCADE,
	umt int8 ,
	data JSONB 
);

CREATE INDEX applicationDevice_idx ON public.applicationDevice (application_id,device_id);

CREATE TABLE public.measurement (
	id SERIAL PRIMARY KEY,
	umt int8 NOT NULL,
	data JSONB NOT NULL,
	application_id int4 REFERENCES public.application(id) ON DELETE CASCADE,
	device_id int4 REFERENCES public.device(id) ON DELETE CASCADE
);


-- Couple of indexes to find a sequence of measurements by fitering on application, or application/device 

CREATE INDEX measurement_application_umt_idx ON public.measurement (application_id,umt);

CREATE INDEX measurement_application_device_umt_idx ON public.measurement (application_id,device_id,umt);

-- display database 
\d

