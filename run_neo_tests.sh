#!/usr/bin/env bash

cd tests || exit 1

# Start the containers, backgrounded so we can do docker wait
# Pre pulling the postgres image so wait-for-it doesn't time out
docker-compose rm -f
docker-compose pull
docker-compose up --build --force-recreate -d

# Print logs based on the test results
docker-compose logs -f tox-tests

# Wait for the tox-tests container to finish, and assign to RESULT
RESULT=$(docker wait tox-tests)

docker cp tox-tests:/home/runner/work/polaris-bg-readings-api/polaris-bg-readings-api/coverage-reports/coverage.xml ../coverage-reports/coverage.xml

# Stop the containers
docker-compose down

# Exit based on the test results
if [ "$RESULT" -ne 0 ]; then
  echo "Tests failed :-("
  exit 1
fi

echo "Tests passed! :-)"
