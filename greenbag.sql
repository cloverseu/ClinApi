CREATE TABLE "user" (
"user_id" int4 NOT NULL,
"username" varchar(122) NOT NULL,
"password" varchar(255) NOT NULL,
"email" varchar(255),
"is_admin" int2,
"can_createTrail" int2,
"can_createSop" int2,
"date_create" date,
"is_active" int2,
PRIMARY KEY ("user_id") 
)
WITHOUT OIDS;

CREATE TABLE "study" (
"study_id" int4 NOT NULL,
"name" varchar(255) NOT NULL,
"description" varchar(255),
"plan_start_date" date,
"plan_end_date" date,
"status_id" int4 NOT NULL,
"user_id" int4,
PRIMARY KEY ("study_id") 
)
WITHOUT OIDS;

CREATE TABLE "sop" (
"sop_id" int4 NOT NULL,
"sop_name" varchar(255),
"study_id" int4,
"user_id" int4,
"sop_description" varchar(255),
"sop_date_create" date,
PRIMARY KEY ("sop_id") 
)
WITHOUT OIDS;


ALTER TABLE "study" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");
ALTER TABLE "sop" ADD FOREIGN KEY ("study_id") REFERENCES "study" ("study_id");
ALTER TABLE "sop" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

