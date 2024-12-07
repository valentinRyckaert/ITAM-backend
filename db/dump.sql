PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE devicegroup (
	"DG_id" INTEGER NOT NULL, 
	"DG_libelle" VARCHAR NOT NULL, 
	PRIMARY KEY ("DG_id")
);
CREATE TABLE packagegroup (
	"PG_id" INTEGER NOT NULL, 
	"PG_libelle" VARCHAR NOT NULL, 
	PRIMARY KEY ("PG_id")
);
CREATE TABLE role (
	"R_id" INTEGER NOT NULL, 
	"R_libelle" VARCHAR NOT NULL, 
	"R_permissions" INTEGER NOT NULL, 
	PRIMARY KEY ("R_id")
);
CREATE TABLE device (
	"D_id" INTEGER NOT NULL, 
	"D_name" VARCHAR NOT NULL, 
	"D_os" INTEGER NOT NULL, 
	"D_group_id" INTEGER, 
	PRIMARY KEY ("D_id"), 
	FOREIGN KEY("D_group_id") REFERENCES devicegroup ("DG_id")
);
CREATE TABLE user (
	"U_id" INTEGER NOT NULL, 
	"U_username" VARCHAR NOT NULL, 
	"U_passHash" VARCHAR NOT NULL, 
	"U_role_id" INTEGER NOT NULL, 
	PRIMARY KEY ("U_id"), 
	FOREIGN KEY("U_role_id") REFERENCES role ("R_id")
);
CREATE TABLE package (
	"P_id" INTEGER NOT NULL, 
	"P_name" VARCHAR NOT NULL, 
	"P_path" VARCHAR NOT NULL, 
	"P_type" VARCHAR NOT NULL, 
	"P_os_supported" VARCHAR NOT NULL, 
	"P_for_device_id" INTEGER, 
	"P_for_group_id" INTEGER, 
	"P_package_group_id" INTEGER NOT NULL, 
	PRIMARY KEY ("P_id"), 
	FOREIGN KEY("P_for_device_id") REFERENCES device ("D_id"), 
	FOREIGN KEY("P_for_group_id") REFERENCES devicegroup ("DG_id"), 
	FOREIGN KEY("P_package_group_id") REFERENCES packagegroup ("PG_id")
);
CREATE INDEX "ix_devicegroup_DG_libelle" ON devicegroup ("DG_libelle");
CREATE INDEX "ix_devicegroup_DG_id" ON devicegroup ("DG_id");
CREATE INDEX "ix_packagegroup_PG_id" ON packagegroup ("PG_id");
CREATE INDEX "ix_packagegroup_PG_libelle" ON packagegroup ("PG_libelle");
CREATE INDEX "ix_role_R_permissions" ON role ("R_permissions");
CREATE INDEX "ix_role_R_id" ON role ("R_id");
CREATE INDEX "ix_role_R_libelle" ON role ("R_libelle");
CREATE INDEX "ix_device_D_group_id" ON device ("D_group_id");
CREATE INDEX "ix_device_D_id" ON device ("D_id");
CREATE INDEX "ix_device_D_name" ON device ("D_name");
CREATE INDEX "ix_device_D_os" ON device ("D_os");
CREATE INDEX "ix_user_U_passHash" ON user ("U_passHash");
CREATE INDEX "ix_user_U_role_id" ON user ("U_role_id");
CREATE INDEX "ix_user_U_username" ON user ("U_username");
CREATE INDEX "ix_user_U_id" ON user ("U_id");
CREATE INDEX "ix_package_P_name" ON package ("P_name");
CREATE INDEX "ix_package_P_id" ON package ("P_id");
CREATE INDEX "ix_package_P_for_group_id" ON package ("P_for_group_id");
CREATE INDEX "ix_package_P_path" ON package ("P_path");
CREATE INDEX "ix_package_P_package_group_id" ON package ("P_package_group_id");
CREATE INDEX "ix_package_P_for_device_id" ON package ("P_for_device_id");
CREATE INDEX "ix_package_P_os_supported" ON package ("P_os_supported");
CREATE INDEX "ix_package_P_type" ON package ("P_type");
COMMIT;
