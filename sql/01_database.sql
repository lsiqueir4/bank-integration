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

CREATE TABLE stark_integration."WebhookStatus" (
  "id" SERIAL PRIMARY KEY,
  "enumerator" VARCHAR(100) UNIQUE NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."WebhookType" (
  "id" SERIAL PRIMARY KEY,
  "enumerator" VARCHAR(100) UNIQUE NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."Invoice" (
  "id" SERIAL PRIMARY KEY,
  "invoice_key" CHAR(36) NOT NULL,
  "external_id" VARCHAR(255) UNIQUE,
  "payer_document_number" VARCHAR(14) NOT NULL,
  "amount" NUMERIC(10, 2) NOT NULL,
  "fee_amount" NUMERIC(10, 2),
  "name" VARCHAR(255) NOT NULL,
  "invoice_status_id" INTEGER NOT NULL,
  "brcode" VARCHAR(255),
  "pdf_url" VARCHAR(255),
  "transfer_account_key" CHAR(36),
  "transfer_key" CHAR(36),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE stark_integration."Transfer" (
  "id" SERIAL PRIMARY KEY,
  "transfer_key" CHAR(36) NOT NULL,
  "external_id" VARCHAR(255) UNIQUE,
  "account_id" INTEGER NOT NULL,
  "amount" NUMERIC(10, 2) NOT NULL,
  "transfer_status_id" INTEGER NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
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

CREATE TABLE stark_integration."Webhook" (
  "id" SERIAL PRIMARY KEY,
  "webhook_key" CHAR(36) NOT NULL,
  "external_id" VARCHAR(255) UNIQUE,
  "webhook_type_id" INT,
  "webhook_status_id" INT NOT NULL,
  "payload" JSONB NOT NULL,
  "failure_reason" VARCHAR(255),
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

ALTER TABLE stark_integration."Webhook" 
  ADD CONSTRAINT fk_webhook_webhook_type FOREIGN KEY ("webhook_type_id") REFERENCES stark_integration."WebhookType" ("id");

ALTER TABLE stark_integration."Webhook" 
  ADD CONSTRAINT fk_webhook_status FOREIGN KEY ("webhook_status_id") REFERENCES stark_integration."WebhookStatus" ("id");

-- Enumerator Insertions
INSERT INTO stark_integration."InvoiceStatus" ("enumerator") VALUES 
  ('created'),
  ('paid'),
  ('voided'),
  ('canceled'),
  ('overdue'),
  ('credited'),
  ('expired');

  INSERT INTO stark_integration."TransferStatus" ("enumerator") VALUES 
  ('created'),
  ('canceled'),
  ('failed'),
  ('success');

  INSERT INTO stark_integration."AccountType" ("enumerator") VALUES 
  ('checking'),
  ('payment'),
  ('savings'),
  ('salary');

    INSERT INTO stark_integration."WebhookStatus" ("enumerator") VALUES 
  ('processed'),
  ('failed');

  INSERT INTO stark_integration."WebhookType" ("enumerator") VALUES 
  ('invoice_created'),
  ('invoice_paid'),
  ('invoice_credited'),
  ('transfer_created'),
  ('transfer_processing'),
  ('transfer_canceled'),
  ('transfer_failed'),
  ('transfer_success'),
  ('transfer_sending'),
  ('transfer_sent');