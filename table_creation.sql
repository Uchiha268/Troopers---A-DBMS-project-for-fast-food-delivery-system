create table USER(
	user_id varchar(255) PRIMARY KEY,
	mobile int(10),
	email varchar(255),
	address varchar(255),
	password varchar(255),
	permissions varchar(255),
	name varchar(255)
);

create table RESTAURANT(
	franchise_id int(10) PRIMARY KEY,
	franchise_name varchar(255)
);

create table ORDERS(
	order_id int(10) PRIMARY KEY,
	total_amount int(10),
	user_id varchar(255),
	franchise_id int(10),
	offer_id int (10),
	discount int(10) default 0,
	final_price int(10) default 0,
	date varchar(255), 
	FOREIGN KEY (user_id) REFERENCES USER(user_id),
	FOREIGN KEY (franchise_id) REFERENCES RESTAURANT(franchise_id),
	FOREIGN KEY (offer_id) REFERENCES OFFER(offer_id)
);

create table PAYMENT_INFO(
	payment_id int(10) PRIMARY KEY,
	order_id int(10) UNIQUE,
	bank varchar(255),
	user_id varchar(255),
	card_no varchar(16),
	FOREIGN KEY (user_id) REFERENCES USER(user_id),
	FOREIGN KEY (order_id) REFERENCES ORDERS(order_id)
);

create table FOOD_ITEM(
	food_id int(10),
	food_description varchar(255),
	food_name varchar(255),
	franchise_id int(10),
	availability varchar(255),
	price int(10),
	FOREIGN KEY (franchise_id) REFERENCES RESTAURANT(franchise_id),
	PRIMARY KEY (food_id, franchise_id)
);

create table BRANCH(
	branch_id int(10),
	franchise_id int(10),
	address varchar(255),
	contact varchar(10),
	PRIMARY KEY(branch_id, franchise_id),
	FOREIGN KEY (franchise_id) references RESTAURANT(franchise_id)
);

create table ORDER_AND_FOOD_ITEM(
	order_id int(10),
	food_id int(10),
	franchise_id int(10),
	quantity int(10),
	total_item_price int(10),
	FOREIGN KEY (order_id) references ORDERS(order_id),
	FOREIGN KEY (food_id) references FOOD_ITEM(food_id),
	FOREIGN KEY (franchise_id) references RESTAURANT(franchise_id),
	PRIMARY KEY (order_id, food_id, franchise_id)
);

create table OFFER(
	offer_id int(10) PRIMARY KEY,
	offer_name varchar(255),
	percent float,
	max_discount int(10)
);

create table USER_AND_OFFER(
	user_id varchar(255),
	offer_id int(10),
	PRIMARY KEY (user_id, offer_id),
	FOREIGN KEY (user_id) references USER(user_id),
	FOREIGN KEY (offer_id) references OFFER(offer_id)
);

create table DELIVERY_AGENT(
	agent_id int(10),
	user_id varchar(255) UNIQUE,
	available int(10) default 1,
	PRIMARY KEY (agent_id),
	FOREIGN KEY (user_id) references user(user_id)
);

create table ORDER_AND_DELIVERY_AGENT(
	order_id int(10),
	agent_id int(10),
	delivered int(10) default 0,
	PRIMARY KEY (order_id, agent_id), 
	FOREIGN KEY (agent_id) references DELIVERY_AGENT(agent_id),
	FOREIGN KEY (order_id) references ORDERS(order_id)
);
