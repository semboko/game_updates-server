alter table balance add column id serial primary key;
alter table balance add constraint unique_pair_account_balance unique(account_id, amount);

alter table account alter column user_id set not null;
alter table account alter column currency_id set not null;
alter table account add constraint unique_pair_user_currency unique(user_id, currency_id);

alter table currency alter column name_short set not null;
alter table currency add constraint unique_currency_name unique(name_short);