USE room_details;

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    sa_no INTEGER NOT NULL,
    class_no INTEGER NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL,
    total_seats INTEGER
);
