create table player (
    id serial primary key,
    username varchar(512) unique not null,
    password char(64) not null,
    is_active boolean default true
)