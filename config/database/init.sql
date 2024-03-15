create table aktien(
    wkn char(6),
    value real,
    time timestamp default CURRENT_TIMESTAMP,
    site integer
);

comment on column aktien.wkn is 'the stocks wkn';

comment on column aktien.site is 'website that was scraped';

comment on column aktien.time is 'the time the entry was created';

comment on column aktien.value is 'the value of the stock at the given time';

alter table
    aktien owner to postgres;

create table companies (
    wkn char(6) not null constraint companies_pk primary key,
    company varchar(128) constraint companies_pk_2 unique,
    country varchar(64)
);

comment on column companies.wkn is 'the companies stock wkn';

comment on column companies.company is 'the companies name';

comment on column companies.country is 'the companies origin country';

alter table
    companies owner to postgres;

create table users(
    id UUID not null constraint user_id primary key,
    username varchar(32) not null,
    full_name varchar(128),
    email varchar(128) not null,
    hashed_password char(256),
    "disabled" boolean not null default false
);