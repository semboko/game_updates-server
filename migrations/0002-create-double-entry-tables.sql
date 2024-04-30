create table currency (
    id serial primary key,
    name_short varchar(10)
);


create table account (
    id serial primary key,
    user_id integer references player (id),
    currency_id integer references currency(id),
    is_active boolean default true
);

create table balance (
    account_id integer references account(id),
    amount numeric(20, 4)
);

create table transaction (
    id serial primary key,
    from_account_id integer references account(id),
    to_account_id integer references account(id),
    amount numeric(20, 4),
    transaction_type int,
    date_time timestamp with time zone
);