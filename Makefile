VERSION = 1-1-1

deploy:
	cd lightupleeton; gcloud app deploy --project lightupleeton --version $(VERSION) --no-promote app.yaml cron.yaml