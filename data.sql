create table date(
    id integer primary key autoincrement,
    entery_date date not null
);

create table food(
    id integer primary key autoincrement,
    name text not null,
    protien integer not null,
    carbohydrates integer not null,
    fat integer not null,
    calories integer not null
);

create table  food_date(
    food_id integer not null,
    log_date_id integer not null,
    primary key(food_id,log_date_id)
)