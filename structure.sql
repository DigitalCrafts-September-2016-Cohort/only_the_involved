CREATE TABLE organization (
  id serial PRIMARY KEY,
  name varchar UNIQUE,
  description text
);

CREATE TABLE volunteer (
  id serial PRIMARY KEY,
  name varchar
);

CREATE TABLE project (
  id serial PRIMARY KEY,
  name varchar,
  start_time timestamp,
  organization_id integer REFERENCES organization (id)
);

CREATE TABLE participation (
  id serial PRIMARY KEY,
  project_id integer REFERENCES project (id),
  volunteer_id integer REFERENCES volunteer (id)
);
