#!/bin/bash
openapi-generator-cli generate -i http://localhost:8000/api/v1/openapi.json -g typescript-axios -o src/generated -p withSeparateModelsAndApi=true,apiPackage=api,modelPackage=models,useSingleRequestParameter=true
