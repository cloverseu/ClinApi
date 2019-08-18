CREATE TABLE "trial" (
"trialID" int4 NOT NULL,
"trialName" varchar NOT NULL,
"trialStage" int4,
"trialBriefIntroduction" varchar(255),
"trialCreatedTime" date,
"trialExpectedStartTime" date,
"trialActualStartTime" date,
"trialActualEndTime" date,
"trialSponsor" varchar(255),
"trialInvestigator" varchar(255),
"trialMonitor" varchar(255),
"trialStatistician" varchar(255),
PRIMARY KEY ("trialID") 
)
WITHOUT OIDS;

CREATE TABLE "trial_user" (
"trialID" int4 NOT NULL,
"userID" int4 NOT NULL
)
WITHOUT OIDS;

CREATE TABLE "user" (
"userID" int4 NOT NULL,
"userName" varchar(255),
PRIMARY KEY ("userID") 
)
WITHOUT OIDS;

CREATE TABLE "tasks" (
"taskID" int4 NOT NULL,
"taskName" varchar NOT NULL,
"belongedToTrialID" int4,
"taskCreatorID" int4,
"taskCreatedTime" date,
"taskExecutorID" int4,
"taskReceivedStatus" bool,
"taskDueTime" date,
"taskProgress" int4,
"taskCompletedStatus" bool,
"taskActualCompletedTime" date,
PRIMARY KEY ("taskID") 
)
WITHOUT OIDS;

CREATE TABLE "taskFiles" (
"fileID" int4 NOT NULL,
"belongedToTaskID" int4,
"fileName" varchar,
"createDate" date,
"creatorID" int4,
"description" varchar,
"deleteDate" date,
"deleteExecutorID" int4,
"downloadURL" varchar,
PRIMARY KEY ("fileID") 
)
WITHOUT OIDS;


ALTER TABLE "trial_user" ADD FOREIGN KEY ("trialID") REFERENCES "trial" ("trialID");
ALTER TABLE "trial_user" ADD FOREIGN KEY ("userID") REFERENCES "user" ("userID");
ALTER TABLE "tasks" ADD FOREIGN KEY ("belongedToTrialID") REFERENCES "trial" ("trialID");
ALTER TABLE "taskFiles" ADD FOREIGN KEY ("belongedToTaskID") REFERENCES "tasks" ("taskID");

