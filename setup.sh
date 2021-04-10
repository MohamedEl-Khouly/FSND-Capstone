#!/bin/sh

# Database URI
export DATABASE_URL=postgresql://serag:password1@localhost:5432/castingAgency
export DATABASE_USER=serag
export DATABASE_PASSWORD=password1

# Environment Variables
export ITEMS_PER_PAGE=10

# Flask App config
export FLASK_APP=app
export FLASK_ENV=development

# Configurations gotten from the account created on Auth0
export AUTH0_DOMAIN=se-fsnd.us.auth0.com
export ALGORITHMS=RS256
export API_AUDIENCE=agency

export AUTH0_CLIENT_ID=yKiu9F8JsUtKelZwtob4eQHGiicBQaSJ
export AUTH0_CALLBACK_URL="http://localhost:5000/"
