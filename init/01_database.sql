CREATE SCHEMA IF NOT EXISTS "stark_integration";

-- Table definitions

CREATE TABLE stark_integration."InvoiceStatus" (
  "id" SERIAL PRIMARY KEY,
  "enumerator" VARCHAR(100) UNIQUE NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."TransferStatus" (
  "id" SERIAL PRIMARY KEY,
  "enumerator" VARCHAR(100) UNIQUE NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."AccountType" (
  "id" SERIAL PRIMARY KEY,
  "enumerator" VARCHAR(100) UNIQUE NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."Invoice" (
  "id" SERIAL PRIMARY KEY,
  "invoice_key" CHAR(36) NOT NULL,
  "external_id" INTEGER UNIQUE NOT NULL,
  "payer_document_number" VARCHAR(14) NOT NULL,
  "amount" NUMERIC(10, 2) NOT NULL,
  "fee_amount" NUMERIC(10, 2),
  "name" VARCHAR(255) NOT NULL,
  "invoice_status_id" INTEGER NOT NULL,
  "barcode" VARCHAR(255),
  "pdf_url" VARCHAR(255),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  "updated_at" TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."Transfer" (
  "id" SERIAL PRIMARY KEY,
  "transfer_key" CHAR(36) NOT NULL,
  "external_id" INTEGER UNIQUE NOT NULL,
  "account_id" INTEGER NOT NULL,
  "amount" NUMERIC(10, 2) NOT NULL,
  "transfer_status_id" INTEGER NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  "updated_at" TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."Account" (
  "id" SERIAL PRIMARY KEY,
  "account_key" CHAR(36) NOT NULL,
  "bank_code" VARCHAR(8) NOT NULL,
  "branch_code" VARCHAR(10) NOT NULL,
  "account_number" VARCHAR(40) NOT NULL,
  "owner_document_number" VARCHAR(18) NOT NULL,
  "owner_name" VARCHAR(255) NOT NULL,
  "account_type_id" INTEGER NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Foreign key constraints

ALTER TABLE stark_integration."Invoice" 
  ADD CONSTRAINT fk_invoice_status FOREIGN KEY ("invoice_status_id") REFERENCES stark_integration."InvoiceStatus" ("id");

ALTER TABLE stark_integration."Transfer" 
  ADD CONSTRAINT fk_transfer_status FOREIGN KEY ("transfer_status_id") REFERENCES stark_integration."TransferStatus" ("id");

ALTER TABLE stark_integration."Transfer" 
  ADD CONSTRAINT fk_transfer_account FOREIGN KEY ("account_id") REFERENCES stark_integration."Account" ("id");

ALTER TABLE stark_integration."Account" 
  ADD CONSTRAINT fk_account_account_type FOREIGN KEY ("account_type_id") REFERENCES stark_integration."AccountType" ("id");

-- Enumerator Insertions
INSERT INTO stark_integration."InvoiceStatus" ("enumerator") VALUES 
  ('created'),
  ('paid'),
  ('credited'),
  ('canceled'),
  ('overdue'),
  ('expired')
  ;

  INSERT INTO stark_integration."TransferStatus" ("enumerator") VALUES 
  ('created'),
  ('processing'),
  ('canceled'),
  ('failed'),
  ('success');

  INSERT INTO stark_integration."AccountType" ("enumerator") VALUES 
  ('checking'),
  ('payment'),
  ('savings'),
  ('salary');