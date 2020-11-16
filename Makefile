LANDSCAPING_IMAGE ?= landscaping:develop
LANDSCAPING_TEST_IMAGE ?= landscaping:develop-test
LANDSCAPING_CONTAINER ?= landscaping_web_1
CI_COMMIT_SHORT_SHA ?= $(shell git rev-parse --short HEAD)
GIT_STAMP ?= $(shell git describe)

.EXPORT_ALL_VARIABLES:

ifdef CI
  REBUILD_IMAGES_FOR_TESTS =
else
  REBUILD_IMAGES_FOR_TESTS = docker-build
endif

run: COMPOSE ?= docker-compose
run: docker-build
	$(COMPOSE) up

run-d: COMPOSE ?= docker-compose
run-d: docker-build
	$(COMPOSE) up -d


mm: COMPOSE ?= docker-compose
mm: docker-build
	$(COMPOSE) run --name $(CI_COMMIT_SHORT_SHA) web \
	python3 /landscaping/manage.py makemigrations
	$(COMPOSE) stop
	$(COMPOSE) rm -f

docker-build:
	docker build --build-arg version=$(GIT_STAMP) -t $(LANDSCAPING_IMAGE) .
	docker build --target=test --build-arg version=$(GIT_STAMP) -t $(LANDSCAPING_TEST_IMAGE) .

test: COMPOSE ?= docker-compose -f compose-test.yml
test: $(REBUILD_IMAGES_FOR_TESTS)
	docker rm -f $(CI_COMMIT_SHORT_SHA) || true
	$(COMPOSE) -p $(CI_COMMIT_SHORT_SHA) run --name $(CI_COMMIT_SHORT_SHA) web \
		bash -c "/wait-for-it.sh db:5432 -t 60 --strict -- coverage run ./manage.py test --noinput && \
		 echo TEST COVERAGE && \
		 coverage report --skip-covered | grep TOTAL"

script:
	$(eval SCRIPT ?= $(shell read -p "Script: " SCRIPT; echo $$SCRIPT))
	docker exec -it $(LANDSCAPING_CONTAINER) ./manage.py $(SCRIPT)

rm: COMPOSE ?= docker-compose
rm:
	$(COMPOSE) stop
	$(COMPOSE) rm -f

clean:
	docker exec -it landscaping_db_1 bash -c "psql -U postgres landscaping --command='DROP SCHEMA public CASCADE; \
	CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO landscaping; \
	GRANT ALL ON SCHEMA public TO public;'" && \
	echo !!!DATABASE SUCCESFULLY CLEANED, PLEASE RESTART SERVER!!!

version:
	$(eval GIT_TAG ?= $(shell git describe --abbrev=0))
	$(eval VERSION ?= $(shell read -p "Version: " VERSION; echo $$VERSION))
	echo "Tagged release $(VERSION)\n" > Changelog-$(VERSION).txt
	git log --oneline --no-decorate --no-merges $(GIT_TAG)..HEAD >> Changelog-$(VERSION).txt
	git tag -a -e -F Changelog-$(VERSION).txt $(VERSION)

remove-compose: COMPOSE ?= docker-compose
remove-compose:
	$(COMPOSE) -p $(CI_COMMIT_SHORT_SHA) stop
	$(COMPOSE) -p $(CI_COMMIT_SHORT_SHA) rm -f

