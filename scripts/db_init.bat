docker run --name crawl-db -e POSTGRES_PASSWORD=koko -e POSTGRES_USER=admin -d -p 5432:5432 postgres:12.6-alpine

rem create table in DB
create table if not exists land (
    estate_id integer not null,
    latitude decimal NOT NULL,
    longitude decimal NOT NULL,
    price_avg decimal,
    land_cnt integer NOT NULL,
    date_processed date NOT NULL,
    source_system text NOT NULL,
    CONSTRAINT estate_source PRIMARY KEY(estate_id,source_system)


)